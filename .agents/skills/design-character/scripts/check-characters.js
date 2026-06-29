#!/usr/bin/env node
'use strict';

// check-characters.js — 人设完整性检查（品类感知）
// Usage: node check-characters.js <scout_report.yaml> <characters.yaml>
//
// 纯 Node.js 内建模块，无外部依赖。
// 通过简单正则提取 YAML 中的角色信息。

const fs = require('fs');
const path = require('path');

function main() {
  const scoutFile = process.argv[2];
  const charFile = process.argv[3];

  if (!scoutFile || !charFile) {
    console.error('Usage: node check-characters.js <scout_report.yaml> <characters.yaml>');
    process.exit(2);
  }

  const scoutPath = path.resolve(scoutFile);
  const charPath = path.resolve(charFile);

  let scoutContent, charContent;
  try {
    scoutContent = fs.readFileSync(scoutPath, 'utf8');
  } catch (err) {
    console.error(`无法读取 scout_report: ${scoutFile} (${err.message})`);
    process.exit(2);
  }
  try {
    charContent = fs.readFileSync(charPath, 'utf8');
  } catch (err) {
    console.error(`无法读取 characters: ${charFile} (${err.message})`);
    process.exit(2);
  }

  const findings = [];

  // 1. 检查是否有主角
  if (!hasRole(charContent, 'protagonist')) {
    findings.push({ severity: 'blocking', message: '缺少主角 (role: protagonist)' });
  }

  // 2. 检查主角深度
  checkRoleDepth(charContent, 'protagonist', findings);

  // 3. 检查反派（如果存在）
  if (hasRole(charContent, 'antagonist')) {
    checkRoleDepth(charContent, 'antagonist', findings);
  }

  // 4. 检查必需角色类型（从 scout_report 提取）
  const requiredTypes = extractRequiredCharacters(scoutContent);
  for (const type of requiredTypes) {
    if (type === 'protagonist') continue; // 已检查
    if (type === 'villain' || type === 'antagonist') {
      if (!hasRole(charContent, 'antagonist')) {
        findings.push({ severity: 'blocking', message: `缺少必需的角色类型: ${type}` });
      }
    } else if (type === 'love_interest') {
      // love_interest 可以通过 relationship type 判断
      if (!hasRelationshipType(charContent, '恋人') && !hasRelationshipType(charContent, 'love_interest')) {
        findings.push({ severity: 'blocking', message: '缺少恋爱对象 (love_interest)' });
      }
    } else if (type === 'supporting_cast') {
      if (!hasRole(charContent, 'supporting')) {
        findings.push({ severity: 'blocking', message: '缺少配角 (role: supporting)' });
      }
    }
  }

  // 5. 检查配角数量
  const supportingCount = countRole(charContent, 'supporting');
  if (supportingCount > 0 && supportingCount < 3) {
    findings.push({ severity: 'advisory', message: `配角数量 ${supportingCount}，建议 ≥ 3 个` });
  }

  // 输出结果
  if (findings.length === 0) {
    console.log('✓ 人设完整性检查通过');
    process.exit(0);
  }

  const blocking = findings.filter(f => f.severity === 'blocking');
  const advisory = findings.filter(f => f.severity !== 'blocking');

  for (const f of findings) {
    console.log(`[${f.severity}] ${f.message}`);
  }
  console.log(`\n共 ${blocking.length} 个阻塞问题，${advisory.length} 个建议`);
  process.exit(blocking.length > 0 ? 1 : 0);
}

/**
 * 提取指定 role 的角色块（YAML 列表项）
 */
function extractRoleBlock(content, role) {
  // 找到 characters: 部分
  const charsMatch = content.match(/characters:\s*\n([\s\S]*)/);
  if (!charsMatch) return null;
  const charsSection = charsMatch[1];

  // 分割成各个角色项（以 "  - " 开头的行，即2空格缩进）
  // 注意：traits 等内部列表是 6 空格缩进，不应分割
  const items = charsSection.split(/\n(?=  - )/);

  for (const item of items) {
    if (new RegExp(`role:\\s*${role}\\b`).test(item)) {
      return [item];
    }
  }
  return null;
}

/**
 * 检查指定 role 是否有足够的深度（traits, psychology, arc）
 */
function checkRoleDepth(content, role, findings) {
  const match = extractRoleBlock(content, role);
  if (!match) return;

  const block = match[0];

  // 检查 name
  if (!/name:\s*\S/.test(block)) {
    findings.push({ severity: 'blocking', message: `${role}: 缺少 name 字段` });
  }

  // 检查 traits
  if (!/traits:\s*[\n-]/.test(block) && !/traits:\s*\[/.test(block)) {
    findings.push({ severity: 'blocking', message: `${role}: 缺少性格特征 (traits)` });
  }

  // 检查 psychology（主角/反派需要）
  if (!/psychology:\s*\n/.test(block)) {
    findings.push({ severity: 'blocking', message: `${role}: 缺少心理维度 (psychology)` });
  }

  // 检查 arc
  if (!/arc:\s*\n/.test(block)) {
    findings.push({ severity: 'blocking', message: `${role}: 缺少人物弧线 (arc)` });
  } else {
    // 检查 arc 是否有 start 和 end
    // 取 arc: 后直到块末尾的所有内容
    const arcMatch = block.match(/arc:\s*\n([\s\S]*)/);
    if (arcMatch) {
      const arcBlock = arcMatch[1];
      if (!/start:\s*\S/.test(arcBlock)) {
        findings.push({ severity: 'blocking', message: `${role}: arc 缺少 start` });
      }
      if (!/end:\s*\S/.test(arcBlock)) {
        findings.push({ severity: 'blocking', message: `${role}: arc 缺少 end` });
      }
    }
  }
}

/**
 * 检查是否存在指定 role
 */
function hasRole(content, role) {
  return new RegExp(`role:\\s*${role}\\b`, 'm').test(content);
}

/**
 * 统计指定 role 的数量
 */
function countRole(content, role) {
  const matches = content.match(new RegExp(`role:\\s*${role}\\b`, 'gm'));
  return matches ? matches.length : 0;
}

/**
 * 检查是否存在指定类型的 relationship
 */
function hasRelationshipType(content, type) {
  return new RegExp(`type:\\s*${type}`, 'm').test(content);
}

/**
 * 从 scout_report 提取必需的字符类型
 */
function extractRequiredCharacters(content) {
  const types = [];
  const charMatch = content.match(/characters:\s*\n([\s\S]*?)(?=\n\s*\w|\n\s*#|$)/);
  if (!charMatch) return types;

  const charSection = charMatch[1];
  const lines = charSection.split('\n');

  for (const line of lines) {
    const match = line.match(/^\s+(\w+):\s*required/);
    if (match) {
      types.push(match[1]);
    }
  }

  return types;
}

main();
