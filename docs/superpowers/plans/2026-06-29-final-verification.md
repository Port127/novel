# Final Verification 执行计划：V4 Skill 体系升级验证

> **执行目标**：验证 9 个 skill 的 V4 升级是否完整、正确、符合设计规范
> **预计耗时**：30 分钟

---

## 验证维度

| 维度 | 验证内容 | 通过标准 |
|------|---------|---------|
| 结构完整性 | 目录和文件数量 | 与 spec 一致 |
| 脚本可用性 | 脚本能正常运行 | exit code 0/1/2 符合预期 |
| 自包含性 | 无外部依赖 | 纯 Node.js 内建模块 |
| SKILL.md 规范 | Phase 化结构完整 | 包含所有必需 section |
| References 索引 | Phase 映射正确 | References 索引表与实际文件匹配 |
| 编码规范 | 中文编写，代码标识符英文 | 抽查无违规 |

---

## 任务 1：结构完整性验证

### 1.1 目录结构验证

检查每个 skill 是否有 `references/` 和 `scripts/` 目录：

```bash
for skill in scout-topic worldbuilding design-character design-outline design-chapters golden-chapters daily-write paywall-design data-diagnosis; do
  echo "=== $skill ==="
  ls -la .agents/skills/$skill/
done
```

**通过标准**：每个 skill 都有 `SKILL.md`、`references/`、`scripts/`

### 1.2 文件数量验证

```bash
# 统计 references 数量
echo "References count per skill:"
for skill in scout-topic worldbuilding design-character design-outline design-chapters golden-chapters daily-write paywall-design data-diagnosis; do
  count=$(ls .agents/skills/$skill/references/*.md 2>/dev/null | wc -l)
  echo "  $skill: $count"
done
echo "Total references: $(find .agents/skills/*/references -name '*.md' | wc -l)"

# 统计 scripts 数量
echo "Scripts count per skill:"
for skill in scout-topic worldbuilding design-character design-outline design-chapters golden-chapters daily-write paywall-design data-diagnosis; do
  count=$(ls .agents/skills/$skill/scripts/*.js 2>/dev/null | wc -l)
  echo "  $skill: $count"
done
echo "Total scripts: $(find .agents/skills/*/scripts -name '*.js' | wc -l)"
```

**通过标准**：
- Total references: 39
- Total scripts: 14

### 1.3 文件清单对比

对比实际文件与 spec Section 5 的设计：

```bash
echo "=== scout-topic (expect: 4 refs, 1 script) ==="
ls .agents/skills/scout-topic/references/ .agents/skills/scout-topic/scripts/

echo "=== worldbuilding (expect: 4 refs, 1 script) ==="
ls .agents/skills/worldbuilding/references/ .agents/skills/worldbuilding/scripts/

# ... 其他 skill 类似
```

---

## 任务 2：脚本可用性验证

### 2.1 脚本可执行性

验证所有脚本可以正常运行（无语法错误）：

```bash
for script in $(find .agents/skills/*/scripts -name '*.js'); do
  echo "Testing: $script"
  node "$script" 2>&1 | head -1
  echo "Exit code: $?"
  echo "---"
done
```

**通过标准**：所有脚本 exit code 为 2（缺少参数）或 0（正常），无 syntax error

### 2.2 脚本功能测试

为每个脚本准备测试数据，验证功能：

| 脚本 | 测试命令 | 预期结果 |
|------|---------|---------|
| check-tags.js | `node scripts/check-tags.js test.yaml` | 正常解析，exit 0/1 |
| check-completeness.js | `node scripts/check-completeness.js scout.yaml world.yaml` | 正常检查，exit 0/1 |
| check-characters.js | `node scripts/check-characters.js scout.yaml chars.yaml` | 正常检查，exit 0/1 |
| check-outline.js | `node scripts/check-outline.js scout.yaml outline.yaml` | 正常检查，exit 0/1 |
| check-pacing.js | `node scripts/check-pacing.js pacing.yaml` | 正常检查，exit 0/1 |
| check-chapters.js | `node scripts/check-chapters.js chapters.yaml` | 正常检查，exit 0/1 |
| check-ai-patterns.js | `node scripts/check-ai-patterns.js test.md` | 正常检测，exit 0/1/2 |
| check-degeneration.js | `node scripts/check-degeneration.js test.md` | 正常检测，exit 0/1/2 |
| normalize-punctuation.js | `node scripts/normalize-punctuation.js test.md` | 正常处理，exit 0 |
| check-golden-structure.js | `node scripts/check-golden-structure.js scout.yaml ch1.md` | 正常检查，exit 0/1 |
| check-paywall.js | `node scripts/check-paywall.js chapters.yaml paywall.yaml` | 正常检查，exit 0/1 |
| analyze-metrics.js | `node scripts/analyze-metrics.js data.csv` | 正常解析，exit 0/1 |

### 2.3 Exit Code 规范验证

验证每个脚本的 exit code 符合规范：

| Exit Code | 含义 | 验证方式 |
|-----------|------|---------|
| 0 | 通过/无问题 | 传入正确数据，检查通过 |
| 1 | 有问题 | 传入有问题的数据 |
| 2 | 脚本错误 | 不传参数/传错误参数 |

---

## 任务 3：自包含性验证

### 3.1 依赖检查

验证所有脚本只使用 Node.js 内建模块：

```bash
for script in $(find .agents/skills/*/scripts -name '*.js'); do
  echo "=== $script ==="
  # 提取 require/import 语句
  grep -E "^(const|let|var|import).*require\(|^import.*from" "$script" | grep -v "fs\|path\|util\|crypto\|os\|child_process"
done
```

**通过标准**：无外部依赖输出

### 3.2 共享脚本独立性

验证 golden-chapters 和 daily-write 的共享脚本是独立副本：

```bash
echo "Comparing shared scripts..."
diff .agents/skills/_shared/scripts/check-ai-patterns.js .agents/skills/golden-chapters/scripts/check-ai-patterns.js && echo "golden-chapters/check-ai-patterns.js: 相同"
diff .agents/skills/_shared/scripts/check-ai-patterns.js .agents/skills/daily-write/scripts/check-ai-patterns.js && echo "daily-write/check-ai-patterns.js: 相同"
# 其他共享脚本类似
```

**通过标准**：各 skill 持有独立副本，与 _shared 内容一致

---

## 任务 4：SKILL.md 规范验证

### 4.1 必需 Section 检查

验证每个 SKILL.md 包含所有必需 section：

```bash
for skill in scout-topic worldbuilding design-character design-outline design-chapters golden-chapters daily-write paywall-design data-diagnosis; do
  echo "=== $skill ==="
  file=".agents/skills/$skill/SKILL.md"
  
  # 检查必需 section
  grep -q "^## Phase 定义\|^## Phase\|^## 工作流程" "$file" && echo "  ✓ Phase 定义" || echo "  ✗ 缺少 Phase 定义"
  grep -q "^## 质量门禁\|^## 质量" "$file" && echo "  ✓ 质量门禁" || echo "  ✗ 缺少质量门禁"
  grep -q "^## 断点恢复" "$file" && echo "  ✓ 断点恢复" || echo "  ✗ 缺少断点恢复"
  grep -q "^## 输出文件" "$file" && echo "  ✓ 输出文件" || echo "  ✗ 缺少输出文件"
  grep -q "^## References 索引" "$file" && echo "  ✓ References 索引" || echo "  ✗ 缺少 References 索引"
done
```

**通过标准**：所有 SKILL.md 都有完整的 section

### 4.2 Phase 化结构检查

验证 SKILL.md 使用了 Phase 化结构（而非旧式线性流程）：

```bash
for skill in scout-topic worldbuilding design-character design-outline design-chapters golden-chapters daily-write paywall-design data-diagnosis; do
  echo "=== $skill ==="
  file=".agents/skills/$skill/SKILL.md"
  
  # 检查 Phase 数量
  phase_count=$(grep -c "^### Phase [0-9]" "$file")
  echo "  Phase 数量: $phase_count"
  
  # 检查是否有入口/出口条件
  grep -q "入口条件\|入口:\|入口条件：" "$file" && echo "  ✓ 有入口条件" || echo "  ✗ 缺少入口条件"
  grep -q "出口条件\|出口:\|出口条件：" "$file" && echo "  ✓ 有出口条件" || echo "  ✗ 缺少出口条件"
done
```

**通过标准**：每个 SKILL.md 至少有 2 个 Phase，且每个 Phase 有入口/出口条件

---

## 任务 5：References 索引验证

### 5.1 References 索引表完整性

验证 SKILL.md 的 References 索引表覆盖了所有 references 文件：

```bash
for skill in scout-topic worldbuilding design-character design-outline design-chapters golden-chapters daily-write paywall-design data-diagnosis; do
  echo "=== $skill ==="
  
  # 提取索引表中提到的文件
  indexed=$(grep -o "[a-z-]*\.md" ".agents/skills/$skill/SKILL.md" | sort -u)
  
  # 提取实际存在的文件
  actual=$(ls ".agents/skills/$skill/references/" 2>/dev/null | sed 's/\.md$//' | sort -u)
  
  echo "  索引中: $(echo $indexed | tr '\n' ' ')"
  echo "  实际有: $(echo $actual | tr '\n' ' ')"
done
```

**通过标准**：索引表与实际文件匹配（允许索引中提到 Phase 为"—"的无文件情况）

### 5.2 Phase 映射正确性

验证 References 索引表中的 Phase 编号与实际 SKILL.md 的 Phase 定义匹配：

```bash
# 抽查示例
echo "=== scout-topic ==="
grep -A 10 "^## References 索引" .agents/skills/scout-topic/SKILL.md
```

**通过标准**：每个 Reference 都标注了正确的加载 Phase

---

## 任务 6：编码规范验证

### 6.1 中文编写检查

抽查 References 文件是否为中文编写：

```bash
for skill in scout-topic worldbuilding design-character; do
  echo "=== $skill ==="
  for ref in .agents/skills/$skill/references/*.md; do
    echo "  检查: $(basename $ref)"
    # 统计中文字符数
    cn_chars=$(grep -o '[\u4e00-\u9fa5]' "$ref" | wc -l)
    total_chars=$(wc -c < "$ref")
    echo "    中文字符: $cn_chars / 总字符: $total_chars"
  done
done
```

**通过标准**：中文内容占主体（>50%）

### 6.2 代码标识符英文检查

抽查 YAML 模板和代码示例中的标识符是否为英文：

```bash
grep -r "^[a-z_]*:" .agents/skills/*/references/*.md | head -20
```

**通过标准**：字段名、变量名使用英文

---

## 任务 7：整合验证

### 7.1 Skill 链路完整性

验证 skill 之间的衔接是否正确：

| 前置 Skill | 输出文件 | 后续 Skill | 入口条件 |
|------------|---------|------------|---------|
| scout-topic | scout_report.yaml | worldbuilding | scout_report.yaml 存在 |
| worldbuilding | worldbuilding.yaml | design-character | worldbuilding.yaml 存在 |
| design-character | characters.yaml | design-outline | characters.yaml 存在 |
| design-outline | outline.yaml | design-chapters | outline.yaml 存在 |
| design-chapters | chapters_index.yaml | golden-chapters | chapters_index.yaml 存在 |
| golden-chapters | chapter_001-003.md | daily-write | chapters_index.yaml 存在 |
| daily-write | chapter_XXX.md | — | — |
| paywall-design | paywall_report.yaml | — | — |
| data-diagnosis | data_diagnosis_report.yaml | — | — |

```bash
# 检查每个 SKILL.md 的前置条件描述
for skill in scout-topic worldbuilding design-character design-outline design-chapters golden-chapters daily-write paywall-design data-diagnosis; do
  echo "=== $skill ==="
  grep -A 3 "前置条件\|前置依赖" ".agents/skills/$skill/SKILL.md" | head -5
done
```

### 7.2 输出文件一致性

验证 SKILL.md 中声明的输出文件与实际模板一致：

```bash
# 检查模板文件
ls templates/default/settings/*.yaml
```

---

## 任务 8：生成验证报告

### 8.1 报告模板

```yaml
final_verification_report:
  date: 2026-06-29
  verifier: ZCode Agent
  
  structure_check:
    total_skills: 9
    total_references: 39
    total_scripts: 14
    status: PASS/FAIL
    details: [...]
  
  script_check:
    total_scripts: 14
    executable: 14
    exit_code_compliant: 14
    no_external_deps: 14
    status: PASS/FAIL
    details: [...]
  
  skill_md_check:
    total_skills: 9
    has_phase_structure: 9
    has_quality_gates: 9
    has_progress_tracking: 9
    has_references_index: 9
    status: PASS/FAIL
    details: [...]
  
  references_check:
    total_files: 39
    chinese_content: 39
    indexed_correctly: 39
    status: PASS/FAIL
    details: [...]
  
  integration_check:
    skill_chain_complete: true
    output_files_consistent: true
    status: PASS/FAIL
    details: [...]
  
  overall_status: PASS/FAIL
  issues_found: []
  recommendations: []
```

### 8.2 执行命令

```bash
# 生成完整验证报告
./scripts/final-verification.sh > verification_report.yaml
```

---

## 执行顺序

1. 任务 1：结构完整性验证（5 分钟）
2. 任务 2：脚本可用性验证（10 分钟）
3. 任务 3：自包含性验证（3 分钟）
4. 任务 4：SKILL.md 规范验证（5 分钟）
5. 任务 5：References 索引验证（3 分钟）
6. 任务 6：编码规范验证（2 分钟）
7. 任务 7：整合验证（2 分钟）
8. 任务 8：生成验证报告（5 分钟）

---

## 通过标准

| 维度 | 通过条件 |
|------|---------|
| 结构完整性 | references = 39, scripts = 14 |
| 脚本可用性 | 所有脚本可执行，exit code 符合规范 |
| 自包含性 | 无外部依赖，共享脚本为独立副本 |
| SKILL.md 规范 | 所有必需 section 完整 |
| References 索引 | 索引与实际文件匹配 |
| 编码规范 | 中文为主，标识符英文 |
| 整合验证 | Skill 链路完整，输出文件一致 |

**总评**：所有维度通过 = V4 升级完成；任一维度失败 = 需要修复
