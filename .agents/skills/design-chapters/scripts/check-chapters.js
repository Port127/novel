#!/usr/bin/env node
'use strict';

// check-chapters.js — 章节计划质量检查
// Usage: node check-chapters.js <chapters_index.yaml>
// 纯 Node.js 内建模块，无外部依赖。

const fs = require('fs');
const path = require('path');

const MIN_BEATS = 3;
const MAX_BEATS = 15;
const MIN_WORDS = 2000;
const MAX_WORDS = 5000;
const MAX_SAME_DENSITY = 3;

function main() {
  const file = process.argv[2];
  if (!file) {
    console.error('Usage: node check-chapters.js <chapters_index.yaml>');
    process.exit(2);
  }

  let content;
  try { content = fs.readFileSync(path.resolve(file), 'utf8'); }
  catch (err) { console.error(`无法读取文件: ${err.message}`); process.exit(2); }

  // 检查是否有 chapters
  if (!/chapters:\s*\n/.test(content)) {
    console.error('[blocking] 缺少 chapters 字段');
    process.exit(1);
  }

  const findings = [];
  const chapters = extractChapters(content);

  if (chapters.length === 0) {
    console.error('[blocking] chapters 为空');
    process.exit(1);
  }

  for (const ch of chapters) {
    const num = ch.number || '?';

    // 必填字段
    if (!ch.title) findings.push({ severity: 'blocking', msg: `第 ${num} 章缺少 title` });
    if (!ch.summary) findings.push({ severity: 'blocking', msg: `第 ${num} 章缺少 summary` });
    if (!ch.tension) findings.push({ severity: 'blocking', msg: `第 ${num} 章缺少 tension` });
    if (!ch.words_target) findings.push({ severity: 'blocking', msg: `第 ${num} 章缺少 words_target` });

    // 节拍数
    if (ch.beats < MIN_BEATS) findings.push({ severity: 'blocking', msg: `第 ${num} 章节拍数不足: ${ch.beats}` });
    if (ch.beats > MAX_BEATS) findings.push({ severity: 'advisory', msg: `第 ${num} 章节拍数过多: ${ch.beats}` });

    // 字数
    if (ch.words_target && ch.words_target < MIN_WORDS) findings.push({ severity: 'blocking', msg: `第 ${num} 章字数过少: ${ch.words_target}` });
    if (ch.words_target && ch.words_target > MAX_WORDS) findings.push({ severity: 'advisory', msg: `第 ${num} 章字数过多: ${ch.words_target}` });

    // 张力值
    if (ch.tension && (ch.tension < 1 || ch.tension > 5)) findings.push({ severity: 'blocking', msg: `第 ${num} 章张力值越界: ${ch.tension}` });
  }

  // 密度连续性
  for (let i = 0; i <= chapters.length - MAX_SAME_DENSITY; i++) {
    const densities = chapters.slice(i, i + MAX_SAME_DENSITY).map(c => c.density);
    if (densities.every(d => d && d === densities[0])) {
      findings.push({ severity: 'advisory', msg: `第 ${chapters[i].number}-${chapters[i + MAX_SAME_DENSITY - 1].number} 章连续密度"${densities[0]}"` });
    }
  }

  // 相邻张力差
  for (let i = 1; i < chapters.length; i++) {
    const prev = chapters[i - 1].tension;
    const curr = chapters[i].tension;
    if (prev && curr && Math.abs(curr - prev) > 2) {
      findings.push({ severity: 'advisory', msg: `第 ${chapters[i - 1].number}→${chapters[i].number} 张力跳变: ${prev}→${curr}` });
    }
  }

  if (findings.length === 0) {
    console.log(`✓ 章节计划检查通过（共 ${chapters.length} 章）`);
    process.exit(0);
  }

  const blocking = findings.filter(f => f.severity === 'blocking');
  for (const f of findings) console.log(`[${f.severity}] ${f.msg}`);
  console.log(`\n共 ${blocking.length} 个阻塞，${findings.length - blocking.length} 个建议`);
  process.exit(blocking.length > 0 ? 1 : 0);
}

function extractChapters(content) {
  const chapters = [];
  // 简单提取: number: N, title: X, tension: N, words_target: N, density: X, beats: [...]
  const chPattern = /^\s*- number:\s*(\d+)/gm;
  let match;
  while ((match = chPattern.exec(content)) !== null) {
    const start = match.index;
    const end = content.indexOf('\n  - number:', start + 1);
    const block = content.slice(start, end === -1 ? undefined : end);

    chapters.push({
      number: parseInt(match[1]),
      title: extractValue(block, /title:\s*["']?([^"'\n]+)/),
      tension: parseInt(extractValue(block, /tension:\s*(\d+)/) || '0'),
      words_target: parseInt(extractValue(block, /words_target:\s*(\d+)/) || '0'),
      density: extractValue(block, /density:\s*(\S+)/),
      summary: /summary:\s*\S/.test(block),
      beats: countBeats(block),
    });
  }
  return chapters;
}

function extractValue(text, pattern) {
  const m = text.match(pattern);
  return m ? m[1].trim() : null;
}

function countBeats(text) {
  const beatsMatch = text.match(/beats:\s*\n([\s\S]*?)(?=\n\s*\w|\n-|$)/);
  if (!beatsMatch) return 0;
  const items = beatsMatch[1].match(/^\s*-\s/gm);
  return items ? items.length : 0;
}

main();
