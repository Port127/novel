#!/usr/bin/env node
'use strict';

// check-tags.js — 标签组合冲突/饱和度检测
// Usage: node check-tags.js <scout_report.yaml>
//
// 只使用 Node.js 内建模块，无外部依赖。
// 通过简单正则提取 YAML 中 recommended_tags.primary 数组。

const fs = require('fs');
const path = require('path');

// 标签冲突表（互斥标签组合）
const CONFLICTS = [
  ['纯爱', '后宫'],
  ['纯爱', '多女主'],
  ['BE', 'HE'],
  ['爽文', '虐文'],
  ['日常', '热血'],
];

function main() {
  const file = process.argv[2];
  if (!file) {
    console.error('Usage: node check-tags.js <scout_report.yaml>');
    process.exit(2);
  }

  const fullPath = path.resolve(file);
  let content;
  try {
    content = fs.readFileSync(fullPath, 'utf8');
  } catch (err) {
    console.error(`无法读取文件: ${file} (${err.message})`);
    process.exit(2);
  }

  const tags = extractPrimaryTags(content);
  if (!tags || tags.length === 0) {
    console.log('⚠ 未找到 recommended_tags.primary，跳过检查');
    process.exit(0);
  }

  const findings = [];

  // 检查冲突
  for (const [a, b] of CONFLICTS) {
    if (tags.includes(a) && tags.includes(b)) {
      findings.push({
        severity: 'blocking',
        type: 'conflict',
        message: `标签冲突: "${a}" 和 "${b}" 互斥`,
      });
    }
  }

  // 检查标签数量
  if (tags.length < 3) {
    findings.push({
      severity: 'advisory',
      type: 'count',
      message: `标签数量不足: ${tags.length} 个（建议 3-6 个）`,
    });
  } else if (tags.length > 6) {
    findings.push({
      severity: 'advisory',
      type: 'count',
      message: `标签过多: ${tags.length} 个（建议 3-6 个）`,
    });
  }

  // 输出结果
  if (findings.length === 0) {
    console.log(`✓ 标签组合无冲突（${tags.length} 个标签）`);
    process.exit(0);
  }

  for (const f of findings) {
    console.log(`[${f.severity}] ${f.message}`);
  }

  const hasBlocking = findings.some(f => f.severity === 'blocking');
  process.exit(hasBlocking ? 1 : 0);
}

/**
 * 从 YAML 内容中提取 recommended_tags.primary 数组
 * 支持两种格式：
 *   1. 内联数组: primary: [标签1, 标签2, 标签3]
 *   2. YAML 列表:
 *        primary:
 *          - 标签1
 *          - 标签2
 */
function extractPrimaryTags(content) {
  // 尝试匹配内联数组格式: primary: [tag1, tag2, ...]
  const inlineMatch = content.match(/primary:\s*\[([^\]]*)\]/);
  if (inlineMatch) {
    return parseTagList(inlineMatch[1]);
  }

  // 尝试匹配 YAML 列表格式
  // 找到 primary: 行，然后收集后续缩进的 - item 行
  const primaryIndex = content.search(/primary:\s*\n/);
  if (primaryIndex === -1) return [];

  const afterPrimary = content.slice(primaryIndex);
  const lines = afterPrimary.split('\n');
  const tags = [];

  // 第一行是 "primary:"，从第二行开始收集列表项
  for (let i = 1; i < lines.length; i++) {
    const line = lines[i];
    const match = line.match(/^\s+-\s+(.+)/);
    if (match) {
      tags.push(match[1].trim().replace(/^["']|["']$/g, ''));
    } else if (line.trim() && !line.match(/^\s*#/)) {
      // 非空、非注释、非列表项 → 列表结束
      break;
    }
  }

  return tags;
}

/**
 * 解析逗号分隔的标签列表
 */
function parseTagList(str) {
  return str
    .split(',')
    .map(s => s.trim().replace(/^["']|["']$/g, ''))
    .filter(Boolean);
}

main();
