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

  const paywallChapter = extractPaywallChapter(paywallContent);
  validatePaywallFields(paywallContent, findings, paywallChapter);

  if (!paywallChapter) {
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

  // 检查4：前期平淡期预警 (Pacing Warning)
  let flatStreak = 0;
  for (let i = Math.max(0, paywallChapter - 6); i < paywallChapter - 1; i++) {
    if (tensions[i] !== undefined && tensions[i] < 3) {
      flatStreak++;
    } else {
      flatStreak = 0;
    }
    if (flatStreak >= 4) {
      findings.push({ severity: 'advisory', message: `付费切点前存在连续 ${flatStreak} 章的平淡期（张力 < 3），读者可能在到达切点前流失，建议压缩无关剧情。` });
      break; // Only warn once
    }
  }

  printResults(findings);
}

function extractPaywallChapter(content) {
  const match = content.match(/paywall_chapter:\s*(\d+)/);
  return match ? parseInt(match[1]) : null;
}

function extractNumber(content, pattern) {
  const match = content.match(pattern);
  return match ? parseInt(match[1], 10) : null;
}

function validatePaywallFields(paywallContent, findings, paywallChapter) {
  const requiredPatterns = [
    [/paywall_chapter:\s*\d+/, '缺少 paywall_chapter'],
    [/strategy:\s*\n[\s\S]*?platform:\s*["']?[^"'\n]+/, '缺少 strategy.platform'],
    [/strategy:\s*\n[\s\S]*?target_free_chapters:\s*\d+/, '缺少 strategy.target_free_chapters'],
    [/strategy:\s*\n[\s\S]*?reason:\s*["']?[^"'\n]+/, '缺少 strategy.reason'],
    [/candidate_cuts:\s*\n\s*-\s+chapter:\s*\d+/, '缺少 candidate_cuts'],
    [/final_cut:\s*\n[\s\S]*?chapter:\s*\d+/, '缺少 final_cut.chapter'],
    [/final_cut:\s*\n[\s\S]*?free_last_chapter:\s*\d+/, '缺少 final_cut.free_last_chapter'],
    [/final_cut:\s*\n[\s\S]*?paid_first_chapter:\s*\d+/, '缺少 final_cut.paid_first_chapter'],
    [/final_cut:\s*\n[\s\S]*?cliffhanger:\s*["']?[^"'\n]+/, '缺少 final_cut.cliffhanger'],
    [/final_cut:\s*\n[\s\S]*?payoff_promise:\s*["']?[^"'\n]+/, '缺少 final_cut.payoff_promise'],
    [/commercial_review:\s*\n[\s\S]*?verdict:\s*["']?(pass|rework)/, '缺少 commercial_review.verdict'],
    [/commercial_review:\s*\n[\s\S]*?notes:\s*["']?[^"'\n]+/, '缺少 commercial_review.notes'],
  ];

  for (const [pattern, message] of requiredPatterns) {
    if (!pattern.test(paywallContent)) findings.push({ severity: 'blocking', message });
  }

  const finalChapter = extractNumber(paywallContent, /final_cut:\s*\n[\s\S]*?chapter:\s*(\d+)/);
  if (finalChapter !== null && finalChapter <= 0) {
    findings.push({ severity: 'blocking', message: `final_cut.chapter 必须大于 0: ${finalChapter}` });
  }
  if (finalChapter && paywallChapter && finalChapter !== paywallChapter) {
    findings.push({ severity: 'blocking', message: `final_cut.chapter (${finalChapter}) 必须等于 paywall_chapter (${paywallChapter})` });
  }
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
