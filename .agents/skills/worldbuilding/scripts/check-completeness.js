#!/usr/bin/env node
'use strict';

// check-completeness.js — 世界观完整性检查
// Usage: node check-completeness.js <scout_report.yaml> <worldbuilding.yaml>
//
// 读取 scout_report.yaml 中 required_elements.worldbuilding.required，
// 检查 worldbuilding.yaml 中对应元素是否存在且非空。
// 纯 Node.js 内建模块，无外部依赖。

const fs = require('fs');
const path = require('path');

function main() {
  const scoutFile = process.argv[2];
  const worldFile = process.argv[3];

  if (!scoutFile || !worldFile) {
    console.error('Usage: node check-completeness.js <scout_report.yaml> <worldbuilding.yaml>');
    process.exit(2);
  }

  const scoutPath = path.resolve(scoutFile);
  const worldPath = path.resolve(worldFile);

  let scoutContent, worldContent;
  try {
    scoutContent = fs.readFileSync(scoutPath, 'utf8');
  } catch (err) {
    console.error(`无法读取 scout_report: ${scoutFile} (${err.message})`);
    process.exit(2);
  }
  try {
    worldContent = fs.readFileSync(worldPath, 'utf8');
  } catch (err) {
    console.error(`无法读取 worldbuilding: ${worldFile} (${err.message})`);
    process.exit(2);
  }

  // 从 scout_report 中提取 required_elements.worldbuilding.required 列表
  const required = extractRequiredElements(scoutContent);
  if (required.length === 0) {
    console.log('⚠ 未声明 required_elements.worldbuilding.required，跳过检查');
    process.exit(0);
  }

  // 检查 worldbuilding.yaml 中每个必需元素是否存在
  const findings = [];
  for (const elem of required) {
    if (!hasElement(worldContent, elem)) {
      findings.push({
        severity: 'blocking',
        element: elem,
        message: `缺少必需的世界观元素: ${elem}`,
      });
    }
  }

  // 输出结果
  if (findings.length === 0) {
    console.log(`✓ 世界观完整性检查通过（${required.length} 个必需元素）`);
    process.exit(0);
  }

  for (const f of findings) {
    console.log(`[${f.severity}] ${f.message}`);
  }
  process.exit(1);
}

/**
 * 从 YAML 内容中提取 required_elements.worldbuilding.required 列表
 * 支持格式：
 *   required_elements:
 *     worldbuilding:
 *       required:
 *         - elem1
 *         - elem2
 */
function extractRequiredElements(content) {
  const elements = [];

  // 查找 required: 在 worldbuilding: 下面的位置
  const worldbuildingMatch = content.match(/worldbuilding:\s*\n([\s\S]*?)(?=\n\s*\w|\n\s*#|$)/);
  if (!worldbuildingMatch) return elements;

  const worldbuildingSection = worldbuildingMatch[1];
  const requiredMatch = worldbuildingSection.match(/required:\s*\n([\s\S]*?)(?=\n\s*\w|\n\s*#|$)/);
  if (!requiredMatch) return elements;

  const requiredSection = requiredMatch[1];
  const lines = requiredSection.split('\n');

  for (const line of lines) {
    const match = line.match(/^\s+-\s+(.+)/);
    if (match) {
      elements.push(match[1].trim().replace(/^["']|["']$/g, ''));
    }
  }

  return elements;
}

/**
 * 检查 YAML 内容中是否存在指定顶级元素且非空
 */
function hasElement(content, element) {
  // 匹配顶级 key（无缩进或只有注释前缀）
  // 检查 key 是否存在且后面有内容（不是空值或空数组）
  const patterns = [
    // key: value (非空值)
    new RegExp(`^${element}:\\s+\\S`, 'm'),
    // key:\n  - item (非空数组)
    new RegExp(`^${element}:\\s*\\n\\s+-\\s`, 'm'),
    // key:\n  subkey: value (非空对象)
    new RegExp(`^${element}:\\s*\\n\\s+\\w+:`, 'm'),
  ];

  return patterns.some(p => p.test(content));
}

main();
