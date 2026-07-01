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
const VALID_STATUS = new Set(['planned', 'draft', 'written', 'revised']);
const VALID_DENSITY = new Set(['密', '中', '疏']);

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
  
  // 检查是否有 stats
  if (!/stats:\s*\n/.test(content)) {
    findings.push({ severity: 'advisory', msg: '缺少 stats 字段' });
  }
  const chapters = extractChapters(content);

  if (chapters.length === 0) {
    console.error('[blocking] chapters 为空');
    process.exit(1);
  }

  for (const ch of chapters) {
    const num = ch.chapter || '?';

    // 必填字段
    if (ch.legacyKey) findings.push({ severity: 'blocking', msg: `第 ${num} 章使用旧字段 ${ch.legacyKey}，当前标准为 chapter` });
    if (!ch.title) findings.push({ severity: 'blocking', msg: `第 ${num} 章缺少 title` });
    if (!ch.file) findings.push({ severity: 'blocking', msg: `第 ${num} 章缺少 file` });
    else if (!/^content\/chapter_\d{3}\.md$/.test(ch.file)) {
      findings.push({ severity: 'blocking', msg: `第 ${num} 章 file 必须形如 content/chapter_001.md: ${ch.file}` });
    }

    if (!ch.outline_file) findings.push({ severity: 'blocking', msg: `第 ${num} 章缺少 outline_file` });
    else {
      const expectedOutline = `settings/chapter_outlines/chapter_${String(num).padStart(3, '0')}.md`;
      if (ch.outline_file !== expectedOutline) {
        findings.push({ severity: 'blocking', msg: `第 ${num} 章 outline_file 应为 ${expectedOutline}: ${ch.outline_file}` });
      }
    }

    if (!VALID_STATUS.has(ch.status)) findings.push({ severity: 'blocking', msg: `第 ${num} 章 status 非法: ${ch.status}` });
    if (!VALID_DENSITY.has(ch.density)) findings.push({ severity: 'blocking', msg: `第 ${num} 章 density 非法: ${ch.density}` });
    if (ch.words === null) findings.push({ severity: 'blocking', msg: `第 ${num} 章缺少 words` });
    if (!ch.summary) findings.push({ severity: 'blocking', msg: `第 ${num} 章缺少 summary` });
    if (ch.tension === null) findings.push({ severity: 'blocking', msg: `第 ${num} 章缺少 tension` });
    if (ch.words_target === null) findings.push({ severity: 'blocking', msg: `第 ${num} 章缺少 words_target` });

    // 节拍数
    if (ch.beats < MIN_BEATS) findings.push({ severity: 'blocking', msg: `第 ${num} 章节拍数不足: ${ch.beats}` });
    if (ch.beats > MAX_BEATS) findings.push({ severity: 'advisory', msg: `第 ${num} 章节拍数过多: ${ch.beats}` });

    // 字数
    if (ch.words_target !== null && ch.words_target < MIN_WORDS) findings.push({ severity: 'blocking', msg: `第 ${num} 章字数过少: ${ch.words_target}` });
    if (ch.words_target !== null && ch.words_target > MAX_WORDS) findings.push({ severity: 'advisory', msg: `第 ${num} 章字数过多: ${ch.words_target}` });

    // 张力值
    if (ch.tension !== null && (ch.tension < 1 || ch.tension > 5)) findings.push({ severity: 'blocking', msg: `第 ${num} 章张力值越界: ${ch.tension}` });
  }

  // 密度连续性
  for (let i = 0; i <= chapters.length - MAX_SAME_DENSITY; i++) {
    const densities = chapters.slice(i, i + MAX_SAME_DENSITY).map(c => c.density);
    if (densities.every(d => d && d === densities[0])) {
      findings.push({ severity: 'advisory', msg: `第 ${chapters[i].chapter}-${chapters[i + MAX_SAME_DENSITY - 1].chapter} 章连续密度"${densities[0]}"` });
    }
  }

  // 相邻张力差
  for (let i = 1; i < chapters.length; i++) {
    const prev = chapters[i - 1].tension;
    const curr = chapters[i].tension;
    if (prev !== null && curr !== null && Math.abs(curr - prev) > 2) {
      findings.push({ severity: 'advisory', msg: `第 ${chapters[i - 1].chapter}→${chapters[i].chapter} 张力跳变: ${prev}→${curr}` });
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
  const markers = [...content.matchAll(/^\s*-\s+(chapter|number):\s*(\d+)/gm)];
  for (let i = 0; i < markers.length; i++) {
    const marker = markers[i];
    const nextMarker = markers[i + 1];
    const blockStart = marker.index + marker[0].length;
    const blockEnd = nextMarker ? nextMarker.index : content.length;
    const block = content.slice(blockStart, blockEnd);
    const key = marker[1];
    const num = parseInt(marker[2], 10);
    
    const tensionStr = extractValue(block, /tension:\s*(\d+)/);
    const wordsStr = extractValue(block, /words_target:\s*(\d+)/);
    const realWordsStr = extractValue(block, /words:\s*(\d+)/);
    
    chapters.push({
      chapter: num,
      legacyKey: key === 'number' ? key : null,
      title: extractValue(block, /title:\s*["']?([^"'\n]+)/),
      file: extractValue(block, /file:\s*["']?([^"'\n]+)/),
      outline_file: extractValue(block, /outline_file:\s*["']?([^"'\n]+)/),
      status: extractValue(block, /status:\s*["']?([^"'\n]+)/),
      tension: tensionStr ? parseInt(tensionStr) : null,
      words_target: wordsStr ? parseInt(wordsStr) : null,
      words: realWordsStr ? parseInt(realWordsStr) : null,
      density: extractValue(block, /density:\s*["']?([^"'\s\n]+)["']?/),
      summary: /summary:\s*(?:[^\s\n]|\n\s+\w+:)/.test(block),
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
  const beatsMatch = text.match(/beats:\s*\n([\s\S]*?)(?=\n\s*(?:tension|words|words_target|density|title|summary|file|outline_file|status|characters|plotlines|functions):|$)/);
  if (!beatsMatch) return 0;
  const items = beatsMatch[1].match(/^\s*-\s/gm);
  return items ? items.length : 0;
}

main();
