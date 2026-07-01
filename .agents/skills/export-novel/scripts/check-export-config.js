#!/usr/bin/env node
'use strict';

// check-export-config.js — 导出配置结构验证
// Usage: node check-export-config.js <export_config.yaml>
// 纯 Node.js 内建模块，无外部依赖。

const fs = require('fs');
const path = require('path');

function main() {
  const configFile = process.argv[2];
  if (!configFile) {
    console.error('Usage: node check-export-config.js <export_config.yaml>');
    process.exit(2);
  }

  let content;
  try { content = fs.readFileSync(path.resolve(configFile), 'utf8'); }
  catch (err) { console.error(`无法读取文件: ${err.message}`); process.exit(2); }

  const findings = [];

  // 检查 1: format 必填且为枚举值
  const formatMatch = content.match(/^format:\s*["']?(\w+)["']?\s*$/m);
  if (!formatMatch) {
    findings.push({ severity: 'blocking', message: '缺少 format 字段' });
  } else {
    const validFormats = ['txt', 'markdown', 'epub'];
    if (!validFormats.includes(formatMatch[1])) {
      findings.push({ severity: 'blocking', message: `format "${formatMatch[1]}" 不在允许值中 (txt/markdown/epub)` });
    }
  }

  // 检查 2: chapter_range.start >= 1
  const startMatch = content.match(/^\s+start:\s*(\d+)/m);
  if (startMatch && parseInt(startMatch[1]) < 1) {
    findings.push({ severity: 'blocking', message: `chapter_range.start (${startMatch[1]}) 必须 >= 1` });
  }

  // 检查 3: chapter_range.end >= start
  const endMatch = content.match(/^\s+end:\s*(\d+)/m);
  if (startMatch && endMatch) {
    const s = parseInt(startMatch[1]);
    const e = parseInt(endMatch[1]);
    if (e < s) {
      findings.push({ severity: 'blocking', message: `chapter_range.end (${e}) < start (${s})` });
    }
  }

  // 检查 4: encoding (advisory)
  const encMatch = content.match(/^encoding:\s*["']?([\w-]+)["']?\s*$/m);
  if (encMatch && encMatch[1].toLowerCase() !== 'utf-8') {
    findings.push({ severity: 'advisory', message: `encoding "${encMatch[1]}" 非标准，推荐 utf-8` });
  }

  // 检查 5: file_naming (advisory)
  const namingMatch = content.match(/^file_naming:\s*["']?(\w+)["']?\s*$/m);
  if (namingMatch) {
    const validNaming = ['sequential', 'by_title'];
    if (!validNaming.includes(namingMatch[1])) {
      findings.push({ severity: 'advisory', message: `file_naming "${namingMatch[1]}" 不在推荐值中 (sequential/by_title)` });
    }
  }

  printResults(findings);
}

function printResults(findings) {
  if (findings.length === 0) {
    console.log('✓ 导出配置检查通过');
    process.exit(0);
  }

  const blocking = findings.filter(f => f.severity === 'blocking');
  for (const f of findings) console.log(`[${f.severity}] ${f.message}`);
  console.log(`\n共 ${blocking.length} 个阻塞，${findings.length - blocking.length} 个建议`);
  process.exit(blocking.length > 0 ? 1 : 0);
}

main();
