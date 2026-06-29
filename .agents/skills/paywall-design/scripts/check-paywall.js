#!/usr/bin/env node
'use strict';

// check-paywall.js — 付费切点合理性验证
// Usage: node check-paywall.js <chapters_index.yaml> <paywall_report.yaml>
// 纯 Node.js 内建模块，无外部依赖。

const fs = require('fs');
const path = require('path');

function main() {
  const chaptersFile = process.argv[2];
  const paywallFile = process.argv[3];

  if (!chaptersFile || !paywallFile) {
    console.error('Usage: node check-paywall.js <chapters_index.yaml> <paywall_report.yaml>');
    process.exit(2);
  }

  let chaptersContent, paywallContent;
  try { chaptersContent = fs.readFileSync(path.resolve(chaptersFile), 'utf8'); }
  catch (err) { console.error(`无法读取 chapters_index: ${err.message}`); process.exit(2); }
  try { paywallContent = fs.readFileSync(path.resolve(paywallFile), 'utf8'); }
  catch (err) { console.error(`无法读取 paywall_report: ${err.message}`); process.exit(2); }

  const findings = [];

  // 提取付费切割章节
  const paywallChapter = extractPaywallChapter(paywallContent);
  if (!paywallChapter) {
    findings.push({ severity: 'blocking', message: '无法提取 paywall_chapter' });
    printResults(findings);
    return;
  }

  // 提取章节张力数据
  const tensions = extractTensions(chaptersContent);
  if (tensions.length === 0) {
    findings.push({ severity: 'advisory', message: '无法提取章节张力数据，跳过检查' });
    printResults(findings);
    return;
  }

  // 检查1：切点章张力是否达标
  const cutTension = tensions[paywallChapter - 1];
  if (cutTension === undefined) {
    findings.push({ severity: 'advisory', message: `第${paywallChapter}章无张力数据` });
  } else if (cutTension < 4) {
    findings.push({ severity: 'blocking', message: `切点章（第${paywallChapter}章）张力 ${cutTension} < 4` });
  }

  // 检查2：切点章张力是否高于均值
  const avgTension = tensions.reduce((s, t) => s + t, 0) / tensions.length;
  if (cutTension !== undefined && cutTension <= avgTension) {
    findings.push({ severity: 'advisory', message: `切点章张力 ${cutTension} 未高于均值 ${avgTension.toFixed(1)}` });
  }

  // 检查3：前一章是否有爽点（张力 ≥ 3）
  const prevTension = tensions[paywallChapter - 2];
  if (prevTension !== undefined && prevTension < 3) {
    findings.push({ severity: 'advisory', message: `前章（第${paywallChapter - 1}章）张力 ${prevTension} < 3，爽点可能不足` });
  }

  printResults(findings);
}

function extractPaywallChapter(content) {
  const match = content.match(/paywall_chapter:\s*(\d+)/);
  return match ? parseInt(match[1]) : null;
}

function extractTensions(content) {
  const tensions = [];
  const pattern = /tension:\s*(\d+)/g;
  let match;
  while ((match = pattern.exec(content)) !== null) {
    tensions.push(parseInt(match[1]));
  }
  return tensions;
}

function printResults(findings) {
  if (findings.length === 0) {
    console.log('✓ 付费切点检查通过');
    process.exit(0);
  }

  const blocking = findings.filter(f => f.severity === 'blocking');
  for (const f of findings) console.log(`[${f.severity}] ${f.message}`);
  console.log(`\n共 ${blocking.length} 个阻塞，${findings.length - blocking.length} 个建议`);
  process.exit(blocking.length > 0 ? 1 : 0);
}

main();
