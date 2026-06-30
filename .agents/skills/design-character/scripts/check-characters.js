#!/usr/bin/env node
'use strict';

// check-characters.js — 人设完整性检查（品类感知）
// Usage: node check-characters.js <scout_report.yaml> <characters.yaml>
//
// 纯 Node.js 内建模块，无外部依赖。
// 通过行解析提取 YAML 中的角色信息。

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

  // 0. Ensure the file has 'characters:' section
  if (!/^characters:/m.test(charContent)) {
    findings.push({ severity: 'blocking', message: '缺少顶级键 characters:（必须遵循 schema 的列表结构）' });
    printFindings(findings);
    return;
  }

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

  printFindings(findings);
}

function printFindings(findings) {
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

function getCharactersSection(content) {
  const lines = content.split('\n');
  let inChars = false;
  let section = [];
  for (const line of lines) {
    if (line.match(/^characters:/)) {
      inChars = true;
      continue;
    }
    if (inChars) {
      if (line.match(/^[A-Za-z_-]+:/)) {
        break; // Reached another top-level key
      }
      section.push(line);
    }
  }
  return section.join('\n');
}

function extractRoleBlock(content, role) {
  const charsSection = getCharactersSection(content);
  if (!charsSection) return null;

  const items = charsSection.split(/\n(?=\s*-\s+name:|\s*-\s+role:)/);
  for (const item of items) {
    if (new RegExp(`role:\\s*${role}\\b`).test(item)) {
      return [item];
    }
  }
  return null;
}

function checkRoleDepth(content, role, findings) {
  const match = extractRoleBlock(content, role);
  if (!match) return;

  const block = match[0];

  if (!/name:\s*\S/.test(block)) {
    findings.push({ severity: 'blocking', message: `${role}: 缺少 name 字段` });
  }

  if (!/traits:\s*[\n-]/.test(block) && !/traits:\s*\[/.test(block)) {
    findings.push({ severity: 'blocking', message: `${role}: 缺少性格特征 (traits)` });
  }

  if (!/psychology:\s*\n/.test(block)) {
    findings.push({ severity: 'blocking', message: `${role}: 缺少心理维度 (psychology)` });
  }

  if (!/arc:\s*\n/.test(block)) {
    findings.push({ severity: 'blocking', message: `${role}: 缺少人物弧线 (arc)` });
  } else {
    // We just check if start/end exist anywhere in the block, which is generally safe
    // as long as they are not used elsewhere in the same character block.
    if (!/start:\s*\S/.test(block)) {
      findings.push({ severity: 'blocking', message: `${role}: arc 缺少 start` });
    }
    if (!/end:\s*\S/.test(block)) {
      findings.push({ severity: 'blocking', message: `${role}: arc 缺少 end` });
    }
  }
}

function hasRole(content, role) {
  const charsSection = getCharactersSection(content);
  return new RegExp(`role:\\s*${role}\\b`, 'm').test(charsSection);
}

function countRole(content, role) {
  const charsSection = getCharactersSection(content);
  const matches = charsSection.match(new RegExp(`role:\\s*${role}\\b`, 'gm'));
  return matches ? matches.length : 0;
}

function hasRelationshipType(content, type) {
  return new RegExp(`type:\\s*${type}`, 'm').test(content);
}

function extractRequiredCharacters(content) {
  const types = [];
  const charMatch = content.match(/characters:\s*\n([\s\S]*?)(?=\n[A-Za-z_]+:|$)/m);
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
