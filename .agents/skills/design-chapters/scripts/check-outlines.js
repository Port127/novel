#!/usr/bin/env node
'use strict';

// check-outlines.js — 单章细纲 Markdown 质量与字数预算检查
// Usage: node check-outlines.js <chapter_outlines_dir>

const fs = require('fs');
const path = require('path');

function main() {
  const dir = process.argv[2];
  if (!dir) {
    console.error('Usage: node check-outlines.js <chapter_outlines_dir>');
    process.exit(2);
  }

  let files;
  try {
    files = fs.readdirSync(path.resolve(dir)).filter(f => f.endsWith('.md'));
  } catch (err) {
    console.error(`无法读取目录: ${err.message}`);
    process.exit(2);
  }

  if (files.length === 0) {
    console.error('[blocking] 未找到任何 .md 细纲文件');
    process.exit(1);
  }

  const findings = [];

  for (const file of files) {
    const filePath = path.join(dir, file);
    let content;
    try {
      content = fs.readFileSync(filePath, 'utf8');
    } catch (err) {
      findings.push({ severity: 'blocking', msg: `${file}: 无法读取文件` });
      continue;
    }

    // 1. 检查 Frontmatter 是否存在并提取 target_words
    const fmMatch = content.match(/^---\n([\s\S]*?)\n---/);
    if (!fmMatch) {
      findings.push({ severity: 'blocking', msg: `${file}: 缺少 YAML Frontmatter` });
      continue;
    }

    const fm = fmMatch[1];
    const targetMatch = fm.match(/words_target:\s*(\d+)/);
    if (!targetMatch) {
      findings.push({ severity: 'blocking', msg: `${file}: Frontmatter 缺少 words_target 字段` });
      continue;
    }
    const wordsTarget = parseInt(targetMatch[1], 10);

    // 2. 检查 Markdown 核心结构结构
    if (!content.includes('#### 情节细化与字数预算')) {
      findings.push({ severity: 'blocking', msg: `${file}: 缺少 '#### 情节细化与字数预算' 标题` });
    }

    // 3. 字数预算求和与校验
    const budgetMatches = content.matchAll(/\[[^\]]*?·\s*(\d+)\s*字\]/g);
    let totalBudget = 0;
    for (const match of budgetMatches) {
      totalBudget += parseInt(match[1], 10);
    }

    const sumMatch = content.match(/预算合计[：:]\s*(\d+)\s*字/);
    if (!sumMatch) {
      findings.push({ severity: 'blocking', msg: `${file}: 未找到合规的 '预算合计：X字' 声明` });
    } else {
      const declaredSum = parseInt(sumMatch[1], 10);
      if (declaredSum !== totalBudget) {
        findings.push({ severity: 'blocking', msg: `${file}: 数学错误！声明的合计(${declaredSum})与各节点真实求和(${totalBudget})不符` });
      }

      // 允许 15% 的浮动误差
      const minAllowed = wordsTarget * 0.85;
      const maxAllowed = wordsTarget * 1.15;
      
      if (totalBudget === 0) {
        findings.push({ severity: 'blocking', msg: `${file}: 未提取到任何有效字数节点（缺少 [密/疏·X字] 格式）` });
      } else if (totalBudget < minAllowed) {
        findings.push({ severity: 'blocking', msg: `${file}: 实际字数预算求和(${totalBudget}) 严重低于目标字数(${wordsTarget})` });
      } else if (totalBudget > maxAllowed) {
        findings.push({ severity: 'advisory', msg: `${file}: 实际字数预算求和(${totalBudget}) 高出目标字数(${wordsTarget})` });
      }
    }
  }

  if (findings.length === 0) {
    console.log(`✓ 细纲 Markdown 检查通过（共检查 ${files.length} 个文件）`);
    process.exit(0);
  }

  const blocking = findings.filter(f => f.severity === 'blocking');
  for (const f of findings) console.log(`[${f.severity}] ${f.msg}`);
  console.log(`\n共检查 ${files.length} 个文件: ${blocking.length} 个阻塞，${findings.length - blocking.length} 个建议`);
  process.exit(blocking.length > 0 ? 1 : 0);
}

main();
