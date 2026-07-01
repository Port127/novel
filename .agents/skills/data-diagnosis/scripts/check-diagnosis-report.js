#!/usr/bin/env node
'use strict';

// check-diagnosis-report.js — 数据诊断报告结构验证
// Usage: node check-diagnosis-report.js <data_diagnosis_report.yaml>
// 纯 Node.js 内建模块，无外部依赖。

const fs = require('fs');
const path = require('path');

function main() {
  const reportFile = process.argv[2];
  if (!reportFile) {
    console.error('Usage: node check-diagnosis-report.js <data_diagnosis_report.yaml>');
    process.exit(2);
  }

  let content;
  try { content = fs.readFileSync(path.resolve(reportFile), 'utf8'); }
  catch (err) { console.error(`无法读取文件: ${err.message}`); process.exit(2); }

  const meaningfulLines = content.split('\n').filter(l => l.trim() && !l.trim().startsWith('#'));
  if (meaningfulLines.length === 0) {
    console.log('[advisory] 报告文件为空');
    console.log('\n共 0 个阻塞，1 个建议');
    process.exit(0);
  }

  const findings = [];

  // 检查 1: report_date (YYYY-MM-DD)
  if (!/^report_date:\s*["']?\d{4}-\d{2}-\d{2}["']?\s*$/m.test(content)) {
    findings.push({ severity: 'blocking', message: '缺少 report_date 或格式不正确 (YYYY-MM-DD)' });
  }

  // 检查 2: platform
  if (!/^platform:\s*["']?[^\s"']+["']?\s*$/m.test(content)) {
    findings.push({ severity: 'blocking', message: '缺少 platform' });
  }

  // 检查 3: project_id
  if (!/^project_id:\s*["']?[^\s"']+["']?\s*$/m.test(content)) {
    findings.push({ severity: 'blocking', message: '缺少 project_id' });
  }

  // 检查 4: anomalies severity 枚举
  const anomaliesSection = extractSection(content, 'anomalies');
  if (anomaliesSection) {
    const entries = anomaliesSection.split(/^\s*-\s+/m).filter(s => s.trim());
    const validSeverities = ['P0', 'P1', 'P2'];
    for (let i = 0; i < entries.length; i++) {
      const sevMatch = entries[i].match(/severity:\s*["']?(\w+)["']?/);
      if (sevMatch && !validSeverities.includes(sevMatch[1])) {
        findings.push({ severity: 'advisory', message: `anomalies[${i + 1}] severity "${sevMatch[1]}" 不在允许值中 (P0/P1/P2)` });
      }
    }
  }

  // 检查 5: recommendations priority
  const recsSection = extractSection(content, 'recommendations');
  if (recsSection) {
    const entries = recsSection.split(/^\s*-\s+/m).filter(s => s.trim());
    for (let i = 0; i < entries.length; i++) {
      if (!/priority:\s*/.test(entries[i])) {
        findings.push({ severity: 'advisory', message: `recommendations[${i + 1}] 缺少 priority` });
      }
    }
  }

  printResults(findings);
}

function extractSection(content, key) {
  const lines = content.split('\n');
  const startIdx = lines.findIndex(l => new RegExp(`^${key}:\\s*`).test(l));
  if (startIdx === -1) return '';

  const section = [];
  for (let i = startIdx + 1; i < lines.length; i++) {
    if (lines[i].trim() === '' || lines[i].trim().startsWith('#')) continue;
    if (/^[A-Za-z_][\w-]*:\s*/.test(lines[i])) break;
    section.push(lines[i]);
  }
  return section.join('\n');
}

function printResults(findings) {
  if (findings.length === 0) {
    console.log('✓ 数据诊断报告结构检查通过');
    process.exit(0);
  }

  const blocking = findings.filter(f => f.severity === 'blocking');
  for (const f of findings) console.log(`[${f.severity}] ${f.message}`);
  console.log(`\n共 ${blocking.length} 个阻塞，${findings.length - blocking.length} 个建议`);
  process.exit(blocking.length > 0 ? 1 : 0);
}

main();
