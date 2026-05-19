"""
完善度检查工具

读取 completeness.schema.yaml，计算设定文件完善度，判断是否可进入下一阶段。
支持模块化目录结构。
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


def load_yaml(file_path: Path) -> Dict:
    """加载 YAML 文件"""
    if not file_path.exists():
        return {}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            return data if data else {}
    except yaml.YAMLError as e:
        print(f"警告: {file_path} 解析错误: {e}")
        return {}


def get_settings_dir(project_id: str) -> Path:
    """获取设定目录"""
    return Path(__file__).parent.parent.parent / "novels" / project_id / "settings"


def check_field_exists(data: Dict, field_path: str) -> Tuple[bool, Optional[str]]:
    """检查字段是否存在且有效"""
    parts = field_path.split('.')
    current = data

    for part in parts:
        if part.endswith('[]'):
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

    if current is None:
        return False, f"字段 {field_path} 为 null"
    if isinstance(current, str) and current.strip() == '':
        return False, f"字段 {field_path} 为空字符串"
    if isinstance(current, list) and len(current) == 0:
        return False, f"列表 {field_path} 为空"

    return True, None


def check_worldbuilding_completeness(project_id: str) -> Dict:
    """检查世界观完善度（模块化结构）"""
    schema = load_completeness_schema()
    wb_config = schema.get('worldbuilding', {})
    wb_dir = get_settings_dir(project_id) / "worldbuilding"

    threshold = wb_config.get('completeness_threshold', 80)
    checked_fields = []
    missing_fields = []

    # 检查力量体系
    power_system = load_yaml(wb_dir / "power_system.yaml")
    power_checks = [
        ('name', '力量体系名称'),
        ('type', '力量体系类型'),
        ('levels', '等级划分'),
    ]
    for field, desc in power_checks:
        exists, reason = check_field_exists(power_system, field)
        checked_fields.append({
            'path': f'power_system.{field}',
            'exists': exists,
            'reason': reason,
            'description': desc
        })
        if not exists:
            missing_fields.append(f'power_system.{field}')

    # 检查势力
    factions_index = load_yaml(wb_dir / "factions" / "_index.yaml")
    factions = factions_index.get("factions", [])
    factions_exists = len(factions) >= 3
    checked_fields.append({
        'path': 'factions/_index.yaml',
        'exists': factions_exists,
        'reason': None if factions_exists else '势力少于3个',
        'description': '势力列表'
    })
    if not factions_exists:
        missing_fields.append('factions (需≥3个)')

    # 检查地点
    locations_index = load_yaml(wb_dir / "locations" / "_index.yaml")
    locations = locations_index.get("locations", [])
    locations_exists = len(locations) >= 1
    checked_fields.append({
        'path': 'locations/_index.yaml',
        'exists': locations_exists,
        'reason': None if locations_exists else '地点为空',
        'description': '地点列表'
    })
    if not locations_exists:
        missing_fields.append('locations (需≥1个)')

    # 计算完善度
    total_checks = len(checked_fields)
    filled_count = total_checks - len(missing_fields)
    completeness = (filled_count / total_checks) * 100 if total_checks > 0 else 0

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
    """检查人物完善度（模块化结构）"""
    schema = load_completeness_schema()
    chars_config = schema.get('characters', {})
    chars_dir = get_settings_dir(project_id) / "characters"

    threshold = chars_config.get('completeness_threshold', 70)
    checked_fields = []
    missing_fields = []

    # 检查主角
    protagonist = load_yaml(chars_dir / "protagonist" / "protagonist.yaml")
    protagonist_checks = [
        ('name', '主角姓名'),
        ('traits', '性格特征'),
        ('psychology.fatal_flaw', '关键缺陷'),
        ('arc.type', '弧线类型'),
    ]
    for field, desc in protagonist_checks:
        exists, reason = check_field_exists(protagonist, field)
        checked_fields.append({
            'path': f'protagonist.{field}',
            'exists': exists,
            'reason': reason,
            'description': desc
        })
        if not exists:
            missing_fields.append(f'protagonist.{field}')

    # 检查反派
    antagonist_index = load_yaml(chars_dir / "antagonist" / "_index.yaml")
    antagonists = antagonist_index.get("antagonists", [])
    antagonists_exists = len(antagonists) >= 1
    checked_fields.append({
        'path': 'antagonist/_index.yaml',
        'exists': antagonists_exists,
        'reason': None if antagonists_exists else '无反派',
        'description': '反派列表'
    })
    if not antagonists_exists:
        missing_fields.append('antagonists (需≥1个)')

    # 检查配角
    supporting_index = load_yaml(chars_dir / "supporting" / "_index.yaml")
    supporting = supporting_index.get("supporting_characters", [])
    supporting_exists = len(supporting) >= 3
    checked_fields.append({
        'path': 'supporting/_index.yaml',
        'exists': supporting_exists,
        'reason': None if supporting_exists else '配角少于3个',
        'description': '配角列表'
    })
    if not supporting_exists:
        missing_fields.append('supporting (需≥3个)')

    # 计算完善度
    total_checks = len(checked_fields)
    filled_count = total_checks - len(missing_fields)
    completeness = (filled_count / total_checks) * 100 if total_checks > 0 else 0

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
    """检查大纲完善度（模块化结构）"""
    schema = load_completeness_schema()
    outline_config = schema.get('outline', {})
    outline_dir = get_settings_dir(project_id) / "outline"

    threshold = outline_config.get('completeness_threshold', 85)
    checked_fields = []
    missing_fields = []

    # 检查 premise
    premise = load_yaml(outline_dir / "premise.yaml")
    premise_statement = premise.get("premise_statement", "")
    premise_exists = len(premise_statement) >= 50
    checked_fields.append({
        'path': 'premise.premise_statement',
        'exists': premise_exists,
        'reason': None if premise_exists else 'premise不足50字',
        'description': '核心设定'
    })
    if not premise_exists:
        missing_fields.append('premise (需≥50字)')

    # 检查 acts
    acts_index = load_yaml(outline_dir / "acts" / "_index.yaml")
    acts = acts_index.get("acts", [])
    acts_exists = len(acts) >= 3
    checked_fields.append({
        'path': 'acts/_index.yaml',
        'exists': acts_exists,
        'reason': None if acts_exists else '幕少于3个',
        'description': '幕结构'
    })
    if not acts_exists:
        missing_fields.append('acts (需≥3幕)')

    # 检查每幕是否有节拍
    beats_count = 0
    for act_info in acts:
        act_file = outline_dir / "acts" / act_info.get("path", "")
        if act_file.exists():
            act_data = load_yaml(act_file)
            for seq in act_data.get("sequences", []):
                beats_count += len(seq.get("beats", []))

    beats_exists = beats_count >= 15  # 至少15个节拍
    checked_fields.append({
        'path': 'acts[].beats',
        'exists': beats_exists,
        'reason': None if beats_exists else '节拍少于15个',
        'description': '节拍总数'
    })
    if not beats_exists:
        missing_fields.append('beats (需≥15个)')

    # 计算完善度
    total_checks = len(checked_fields)
    filled_count = total_checks - len(missing_fields)
    completeness = (filled_count / total_checks) * 100 if total_checks > 0 else 0

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
    """检查设定文件完善度"""
    if setting_type == 'worldbuilding':
        return check_worldbuilding_completeness(project_id)
    elif setting_type == 'characters':
        return check_characters_completeness(project_id)
    elif setting_type == 'outline':
        return check_outline_completeness(project_id)
    else:
        raise ValueError(f"未知的设定类型: {setting_type}")


def check_all_dependencies(project_id: str) -> Dict:
    """检查所有前置依赖完善度"""
    worldbuilding_result = check_completeness(project_id, 'worldbuilding')
    characters_result = check_completeness(project_id, 'characters')
    outline_result = check_completeness(project_id, 'outline')

    blockers = []

    can_generate_outline = worldbuilding_result['is_complete'] and characters_result['is_complete']
    if not worldbuilding_result['is_complete']:
        blockers.append(f"世界观完善度不足: {worldbuilding_result['completeness']}% (需 ≥ {worldbuilding_result['threshold']}%)")
    if not characters_result['is_complete']:
        blockers.append(f"人物完善度不足: {characters_result['completeness']}% (需 ≥ {characters_result['threshold']}%)")

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
        'can_write_content': True,
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