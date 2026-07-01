#!/usr/bin/env node
'use strict';

// check-notes.js — notes.yaml 结构验证
// Usage: node check-notes.js <notes.yaml>
// 纯 Node.js 内建模块，无外部依赖。

const fs = require('fs');
const path = require('path');

function main() {
  const notesFile = process.argv[2];
  if (!notesFile) {
    console.error('Usage: node check-notes.js <notes.yaml>');
    process.exit(2);
  }

  let content;
  try { content = fs.readFileSync(path.resolve(notesFile), 'utf8'); }
  catch (err) { console.error(`无法读取文件: ${err.message}`); process.exit(2); }

  // 跳过纯注释或空文件
  const meaningfulLines = content.split('\n').filter(l => l.trim() && !l.trim().startsWith('#'));
  if (meaningfulLines.length === 0) {
    console.log('[advisory] notes.yaml 为空，无结构化数据');
    console.log('\n共 0 个阻塞，1 个建议');
    process.exit(0);
  }

  const findings = [];

  // 检查 1: version 字段
  if (!/^version:\s*\d+/m.test(content)) {
    findings.push({ severity: 'blocking', message: '缺少 version 字段（必须为整数）' });
  }

  // 检查 2: tracking 节点
  if (!/^tracking:\s*$/m.test(content)) {
    findings.push({ severity: 'blocking', message: '缺少 tracking 节点' });
  } else {
    const trackingFields = ['recent_chapters', 'ten_chapter_summaries', 'volume_overview', 'character_states', 'foreshadowing'];
    for (const field of trackingFields) {
      if (!new RegExp(`^\\s+${field}:\\s*`, 'm').test(content)) {
        findings.push({ severity: 'blocking', message: `tracking 缺少 ${field} 字段` });
      }
    }
  }

  // 检查 3: foreshadowing status 枚举
  const foreshadowingSection = extractSection(content, 'foreshadowing');
  if (foreshadowingSection) {
    const statuses = [];
    const pattern = /^\s+status:\s*["']?(\w+)["']?/gm;
    let m;
    while ((m = pattern.exec(foreshadowingSection)) !== null) statuses.push(m[1]);
    const valid = ['open', 'resolved', 'dropped'];
    for (const s of statuses) {
      if (!valid.includes(s)) {
        findings.push({ severity: 'blocking', message: `foreshadowing.status "${s}" 不在允许值中 (open/resolved/dropped)` });
      }
    }

    // 检查 planted_chapter
    const entries = foreshadowingSection.split(/^\s*-\s+/m).filter(s => s.trim());
    for (let i = 0; i < entries.length; i++) {
      if (!/planted_chapter:\s*\d+/.test(entries[i])) {
        findings.push({ severity: 'blocking', message: `foreshadowing 第 ${i + 1} 项缺少 planted_chapter` });
      }
    }
  }

  // 检查 4: character_states name 非空
  const charSection = extractSection(content, 'character_states');
  if (charSection) {
    const entries = charSection.split(/^\s*-\s+/m).filter(s => s.trim());
    for (let i = 0; i < entries.length; i++) {
      if (!/name:\s*["']?[^\s"']+/.test(entries[i])) {
        findings.push({ severity: 'blocking', message: `character_states 第 ${i + 1} 项缺少 name` });
      }
    }
  }

  // 检查 5: preferences 节点 (advisory)
  if (!/^preferences:\s*$/m.test(content)) {
    findings.push({ severity: 'advisory', message: '缺少 preferences 节点（style_notes / banned_settings / pending_confirmations）' });
  }

  printResults(findings);
}

function extractSection(content, key) {
  const lines = content.split('\n');
  const startIdx = lines.findIndex(l => new RegExp(`^\\s+${key}:\\s*`).test(l));
  if (startIdx === -1) return '';

  const section = [];
  const indent = lines[startIdx].match(/^(\s*)/)[1].length;
  for (let i = startIdx + 1; i < lines.length; i++) {
    if (lines[i].trim() === '' || lines[i].trim().startsWith('#')) continue;
    const currentIndent = lines[i].match(/^(\s*)/)[1].length;
    if (currentIndent <= indent && lines[i].trim()) break;
    section.push(lines[i]);
  }
  return section.join('\n');
}

function printResults(findings) {
  if (findings.length === 0) {
    console.log('✓ notes.yaml 结构检查通过');
    process.exit(0);
  }

  const blocking = findings.filter(f => f.severity === 'blocking');
  for (const f of findings) console.log(`[${f.severity}] ${f.message}`);
  console.log(`\n共 ${blocking.length} 个阻塞，${findings.length - blocking.length} 个建议`);
  process.exit(blocking.length > 0 ? 1 : 0);
}

main();
