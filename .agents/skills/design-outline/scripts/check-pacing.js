#!/usr/bin/env node
'use strict';

// check-pacing.js — 节奏问题检测
// Usage: node check-pacing.js <pacing.yaml>
// 纯 Node.js 内建模块，无外部依赖。

const fs = require('fs');
const path = require('path');

function main() {
  const pacingFile = process.argv[2];
  if (!pacingFile) {
    console.error('Usage: node check-pacing.js <pacing.yaml>');
    process.exit(2);
  }

  let content;
  try { content = fs.readFileSync(path.resolve(pacingFile), 'utf8'); }
  catch (err) { console.error(`无法读取文件: ${err.message}`); process.exit(2); }

  const tensionData = extractTensionData(content);
  if (tensionData.length === 0) {
    console.log('⚠ 无法提取张力数据，跳过节奏检测');
    process.exit(0);
  }

  const findings = [];

  // 0. 张力范围检测
  for (const item of tensionData) {
    if (item.tension < 1 || item.tension > 5) {
      findings.push({
        severity: 'blocking',
        message: `第${item.ch}章张力值越界：${item.tension}，必须在 1-5`,
      });
    }
  }

  // 1. 连续慢章检测
  const slowGroups = findConsecutiveBy(tensionData, t => t <= 2, 3);
  for (const group of slowGroups) {
    findings.push({
      severity: 'blocking',
      message: `连续 ${group.length} 章慢节奏（第${group[0].ch}-${group[group.length-1].ch}章），张力 ≤ 2`,
    });
  }

  // 2. 高潮间距检测
  const climaxChapters = tensionData.filter(t => t.tension >= 4);
  if (climaxChapters.length > 1) {
    for (let i = 1; i < climaxChapters.length; i++) {
      const gap = climaxChapters[i].ch - climaxChapters[i-1].ch;
      if (gap > 15) {
        findings.push({
          severity: 'blocking',
          message: `高潮间距过大：第${climaxChapters[i-1].ch}章→第${climaxChapters[i].ch}章（间距${gap}章）`,
        });
      }
    }
  }

  // 3. 黄金三章检测
  const first3 = tensionData.slice(0, 3);
  if (first3.length >= 3) {
    const avg = first3.reduce((s, t) => s + t.tension, 0) / 3;
    if (avg < 3) {
      findings.push({ severity: 'blocking', message: `黄金三章平均张力 ${avg.toFixed(1)} < 3` });
    }
  }

  // 4. 高潮密集检测
  const denseGroups = findConsecutiveBy(tensionData, t => t >= 4, 5);
  for (const group of denseGroups) {
    findings.push({
      severity: 'advisory',
      message: `连续 ${group.length} 章高张力（第${group[0].ch}-${group[group.length-1].ch}章），读者可能疲劳`,
    });
  }

  // 输出
  if (findings.length === 0) {
    console.log(`✓ 节奏检测通过（${tensionData.length} 个数据点）`);
    process.exit(0);
  }

  const blocking = findings.filter(f => f.severity === 'blocking');
  for (const f of findings) console.log(`[${f.severity}] ${f.message}`);
  console.log(`\n总计: ${findings.length} 项 (${blocking.length} blocking)`);
  process.exit(blocking.length > 0 ? 1 : 0);
}

function extractTensionData(content) {
  const data = [];
  // 匹配 "- chapter: N\n    tension: N" 格式
  const pattern = /chapter:\s*(\d+)\s*\n\s*tension:\s*(\d+)/g;
  let match;
  while ((match = pattern.exec(content)) !== null) {
    data.push({ ch: parseInt(match[1]), tension: parseInt(match[2]) });
  }
  data.sort((a, b) => a.ch - b.ch);
  return data;
}

function findConsecutiveBy(data, predicate, minLength) {
  const groups = [];
  let current = [];
  for (const item of data) {
    if (predicate(item.tension)) {
      current.push(item);
    } else {
      if (current.length >= minLength) groups.push([...current]);
      current = [];
    }
  }
  if (current.length >= minLength) groups.push(current);
  return groups;
}

main();
