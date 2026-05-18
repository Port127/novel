"""
完善度检查工具

读取 completeness.schema.yaml，计算设定文件完善度，判断是否可进入下一阶段。
"""

import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple


def load_completeness_schema() -> Dict:
    """加载完善度标准定义"""
    schema_path = Path(__file__).parent.parent.parent / "data" / "schemas" / "completeness.schema.yaml"
    if not schema_path.exists():
        raise FileNotFoundError(f"完善度标准文件不存在: {schema_path}")

    with open(schema_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_setting_file(project_id: str, setting_type: str) -> Dict:
    """加载设定文件"""
    setting_path = Path(__file__).parent.parent.parent / "novels" / project_id / "settings" / f"{setting_type}.yaml"
    if not setting_path.exists():
        return {}

    try:
        with open(setting_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data if data else {}
    except yaml.YAMLError as e:
        print(f"警告: {setting_type}.yaml 解析错误: {e}")
        return {}


def check_field_exists(data: Dict, field_path: str) -> Tuple[bool, Optional[str]]:
    """
    检查字段是否存在且有效

    Args:
        data: 设定数据
        field_path: 字段路径（如 power_system.name）

    Returns:
        (是否存在, 缺失原因)
    """
    parts = field_path.split('.')
    current = data

    for part in parts:
        if part.endswith('[]'):
            # 列表字段
            list_name = part[:-2]
            if list_name not in current:
                return False, f"字段 {list_name} 不存在"
            if not isinstance(current[list_name], list):
                return False, f"字段 {list_name} 不是列表"
            if len(current[list_name]) == 0:
                return False, f"列表 {list_name} 为空"
            current = current[list_name]
        else:
            if part not in current:
                return False, f"字段 {part} 不存在"
            current = current[part]

    # 检查值是否有效
    if current is None:
        return False, f"字段 {field_path} 为 null"
    if isinstance(current, str) and current.strip() == '':
        return False, f"字段 {field_path} 为空字符串"
    if isinstance(current, list) and len(current) == 0:
        return False, f"列表 {field_path} 为空"

    return True, None


def check_worldbuilding_completeness(project_id: str) -> Dict:
    """检查世界观完善度"""
    schema = load_completeness_schema()
    worldbuilding_config = schema.get('worldbuilding', {})
    setting_data = load_setting_file(project_id, 'worldbuilding')

    required_fields = worldbuilding_config.get('required_fields', [])
    threshold = worldbuilding_config.get('completeness_threshold', 80)

    checked_fields = []
    missing_fields = []

    for field_def in required_fields:
        field_path = field_def['path']
        exists, reason = check_field_exists(setting_data, field_path)

        checked_fields.append({
            'path': field_path,
            'exists': exists,
            'reason': reason,
            'description': field_def.get('description', '')
        })

        if not exists:
            missing_fields.append(field_path)

    # 计算完善度
    total_required = len(required_fields)
    filled_count = total_required - len(missing_fields)
    completeness = (filled_count / total_required) * 100 if total_required > 0 else 0

    return {
        'setting_type': 'worldbuilding',
        'completeness': round(completeness, 1),
        'threshold': threshold,
        'is_complete': completeness >= threshold,
        'checked_fields': checked_fields,
        'missing_fields': missing_fields,
        'summary': f"世界观完善度: {completeness:.1f}% (阈值: {threshold}%)"
    }


def check_characters_completeness(project_id: str) -> Dict:
    """检查人物完善度"""
    schema = load_completeness_schema()
    characters_config = schema.get('characters', {})
    setting_data = load_setting_file(project_id, 'characters')

    threshold = characters_config.get('completeness_threshold', 70)

    # 检查人物列表是否存在
    if 'characters' not in setting_data or not setting_data['characters']:
        return {
            'setting_type': 'characters',
            'completeness': 0,
            'threshold': threshold,
            'is_complete': False,
            'checked_fields': [],
            'missing_fields': ['characters'],
            'summary': f"人物完善度: 0% (阈值: {threshold}%) - 人物列表为空"
        }

    characters_list = setting_data['characters']
    checked_fields = []
    missing_fields = []

    # 检查主角
    protagonist = None
    for char in characters_list:
        if char.get('role') == 'protagonist':
            protagonist = char
            break

    if not protagonist:
        missing_fields.append('characters[].role=protagonist')
        checked_fields.append({
            'path': 'characters[].role=protagonist',
            'exists': False,
            'reason': '不存在主角',
            'description': '必须有主角'
        })
    else:
        # 检查主角必填字段
        required_for_protagonist = ['name', 'traits', 'arc']
        for field in required_for_protagonist:
            exists, reason = check_field_exists({'character': protagonist}, f'character.{field}')
            checked_fields.append({
                'path': f'protagonist.{field}',
                'exists': exists,
                'reason': reason,
                'description': f'主角必填: {field}'
            })
            if not exists:
                missing_fields.append(f'protagonist.{field}')

    # 计算完善度（角色权重）
    total_required = 5  # characters列表 + protagonist.name + traits + arc + role
    filled_count = total_required - len(missing_fields)
    completeness = (filled_count / total_required) * 100

    return {
        'setting_type': 'characters',
        'completeness': round(completeness, 1),
        'threshold': threshold,
        'is_complete': completeness >= threshold,
        'checked_fields': checked_fields,
        'missing_fields': missing_fields,
        'summary': f"人物完善度: {completeness:.1f}% (阈值: {threshold}%)"
    }


def check_outline_completeness(project_id: str) -> Dict:
    """检查大纲完善度"""
    schema = load_completeness_schema()
    outline_config = schema.get('outline', {})
    setting_data = load_setting_file(project_id, 'outline')

    threshold = outline_config.get('completeness_threshold', 85)

    # 检查 premise
    checked_fields = []
    missing_fields = []

    premise_exists = 'premise' in setting_data and setting_data['premise'] and len(setting_data['premise']) >= 20
    checked_fields.append({
        'path': 'premise',
        'exists': premise_exists,
        'reason': None if premise_exists else 'premise不存在或长度不足20',
        'description': '故事核心设定'
    })
    if not premise_exists:
        missing_fields.append('premise')

    # 检查 acts
    acts_exists = 'acts' in setting_data and isinstance(setting_data['acts'], list) and len(setting_data['acts']) >= 3
    checked_fields.append({
        'path': 'acts',
        'exists': acts_exists,
        'reason': None if acts_exists else 'acts不存在或少于3幕',
        'description': '幕结构'
    })
    if not acts_exists:
        missing_fields.append('acts')

    # 计算完善度
    total_required = 2  # premise + acts（简化计算）
    filled_count = total_required - len(missing_fields)
    completeness = (filled_count / total_required) * 100

    return {
        'setting_type': 'outline',
        'completeness': round(completeness, 1),
        'threshold': threshold,
        'is_complete': completeness >= threshold,
        'checked_fields': checked_fields,
        'missing_fields': missing_fields,
        'summary': f"大纲完善度: {completeness:.1f}% (阈值: {threshold}%)"
    }


def check_completeness(project_id: str, setting_type: str) -> Dict:
    """
    检查设定文件完善度

    Args:
        project_id: 项目ID
        setting_type: worldbuilding/characters/outline

    Returns:
        {
            'setting_type': str,
            'completeness': float,
            'threshold': int,
            'is_complete': bool,
            'checked_fields': list,
            'missing_fields': list,
            'summary': str
        }
    """
    if setting_type == 'worldbuilding':
        return check_worldbuilding_completeness(project_id)
    elif setting_type == 'characters':
        return check_characters_completeness(project_id)
    elif setting_type == 'outline':
        return check_outline_completeness(project_id)
    else:
        raise ValueError(f"未知的设定类型: {setting_type}")


def check_all_dependencies(project_id: str) -> Dict:
    """
    检查所有前置依赖完善度

    Returns:
        {
            'project_id': str,
            'worldbuilding': dict,
            'characters': dict,
            'outline': dict,
            'can_generate_outline': bool,
            'can_generate_chapter': bool,
            'can_write_content': bool,
            'blockers': list
        }
    """
    worldbuilding_result = check_completeness(project_id, 'worldbuilding')
    characters_result = check_completeness(project_id, 'characters')
    outline_result = check_completeness(project_id, 'outline')

    blockers = []

    # 检查是否可以生成大纲
    can_generate_outline = worldbuilding_result['is_complete'] and characters_result['is_complete']
    if not worldbuilding_result['is_complete']:
        blockers.append(f"世界观完善度不足: {worldbuilding_result['completeness']}% (需 ≥ {worldbuilding_result['threshold']}%)")
    if not characters_result['is_complete']:
        blockers.append(f"人物完善度不足: {characters_result['completeness']}% (需 ≥ {characters_result['threshold']}%)")

    # 检查是否可以生成章节
    can_generate_chapter = outline_result['is_complete']
    if not outline_result['is_complete']:
        blockers.append(f"大纲完善度不足: {outline_result['completeness']}% (需 ≥ {outline_result['threshold']}%)")

    return {
        'project_id': project_id,
        'worldbuilding': worldbuilding_result,
        'characters': characters_result,
        'outline': outline_result,
        'can_generate_outline': can_generate_outline,
        'can_generate_chapter': can_generate_chapter,
        'can_write_content': True,  # 正文只检查目标章节
        'blockers': blockers
    }


def print_result(result: Dict):
    """打印检查结果"""
    print(f"\n{'='*50}")
    print(f"设定类型: {result['setting_type']}")
    print(f"完善度: {result['completeness']}%")
    print(f"阈值: {result['threshold']}%")
    print(f"状态: {'✅ 完善' if result['is_complete'] else '❌ 不完善'}")

    if result['missing_fields']:
        print(f"\n缺失字段:")
        for field in result['missing_fields']:
            print(f"  - {field}")

    print(f"\n{result['summary']}")
    print(f"{'='*50}\n")


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("用法: python completeness_check.py <project_id> [setting_type]")
        print("setting_type: worldbuilding / characters / outline / all")
        sys.exit(1)

    project_id = sys.argv[1]
    setting_type = sys.argv[2] if len(sys.argv) > 2 else 'all'

    if setting_type == 'all':
        result = check_all_dependencies(project_id)
        print(f"\n项目: {project_id}")
        print_result(result['worldbuilding'])
        print_result(result['characters'])
        print_result(result['outline'])

        print(f"\n前置依赖状态:")
        print(f"  可生成大纲: {'✅' if result['can_generate_outline'] else '❌'}")
        print(f"  可生成章节: {'✅' if result['can_generate_chapter'] else '❌'}")

        if result['blockers']:
            print(f"\n阻塞原因:")
            for blocker in result['blockers']:
                print(f"  - {blocker}")
    else:
        result = check_completeness(project_id, setting_type)
        print_result(result)