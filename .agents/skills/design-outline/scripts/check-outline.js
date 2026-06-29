#!/usr/bin/env node
'use strict';

// check-outline.js — 大纲结构完整性检查（品类感知）
// Usage: node check-outline.js <scout_report.yaml> <outline.yaml>
// 纯 Node.js 内建模块，无外部依赖。

const fs = require('fs');
const path = require('path');

function main() {
  const scoutFile = process.argv[2];
  const outlineFile = process.argv[3];

  if (!scoutFile || !outlineFile) {
    console.error('Usage: node check-outline.js <scout_report.yaml> <outline.yaml>');
    process.exit(2);
  }

  let scoutContent, outlineContent;
  try { scoutContent = fs.readFileSync(path.resolve(scoutFile), 'utf8'); }
  catch (err) { console.error(`无法读取 scout_report: ${err.message}`); process.exit(2); }
  try { outlineContent = fs.readFileSync(path.resolve(outlineFile), 'utf8'); }
  catch (err) { console.error(`无法读取 outline: ${err.message}`); process.exit(2); }

  const findings = [];
  const structureType = extractField(scoutContent, /type:\s*(\S+)/, '三幕式');

  // 1. 前提检查
  if (!/premise:\s*\S/.test(outlineContent)) {
    findings.push({ severity: 'blocking', message: '缺少 premise（核心前提）' });
  }

  // 2. 幕结构检查
  if (!/acts:\s*\n/.test(outlineContent)) {
    findings.push({ severity: 'blocking', message: '缺少 acts（幕结构）' });
  } else {
    const actCount = countOccurrences(outlineContent, /^\s*act_number:\s*\d+/m);
    const expectedActs = getExpectedActCount(structureType);
    if (actCount < expectedActs.min) {
      findings.push({
        severity: 'blocking',
        message: `${structureType}结构至少需要 ${expectedActs.min} 幕，当前检测到 ${actCount} 幕`,
      });
    }
  }

  // 3. 主题标签检查
  if (!/themes?:\s*[\n\[]/.test(outlineContent)) {
    findings.push({ severity: 'advisory', message: '缺少 themes（主题标签）' });
  }

  // 输出结果
  if (findings.length === 0) {
    console.log('✓ 大纲结构完整性检查通过');
    process.exit(0);
  }

  const blocking = findings.filter(f => f.severity === 'blocking');
  for (const f of findings) {
    console.log(`[${f.severity}] ${f.message}`);
  }
  console.log(`\n总计: ${findings.length} 项 (${blocking.length} blocking)`);
  process.exit(blocking.length > 0 ? 1 : 0);
}

function extractField(content, pattern, defaultVal) {
  const match = content.match(pattern);
  return match ? match[1] : defaultVal;
}

function countOccurrences(content, pattern) {
  const matches = content.match(new RegExp(pattern, 'gm'));
  return matches ? matches.length : 0;
}

function getExpectedActCount(structureType) {
  switch (structureType) {
    case '三幕式': return { min: 3 };
    case '起承转合': return { min: 4 };
    case '英雄之旅': return { min: 3 };
    default: return { min: 3 };
  }
}

main();
