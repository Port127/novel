#!/usr/bin/env node
'use strict';

// check-golden-structure.js — 黄金三章结构检查（品类感知）
// Usage: node check-golden-structure.js <scout_report.yaml> <chapter_001.md> [chapter_002.md] [chapter_003.md]
// 纯 Node.js 内建模块，无外部依赖。

const fs = require('fs');
const path = require('path');

function main() {
  const scoutFile = process.argv[2];
  const ch1File = process.argv[3];
  const ch2File = process.argv[4];
  const ch3File = process.argv[5];

  if (!scoutFile || !ch1File) {
    console.error('Usage: node check-golden-structure.js <scout_report.yaml> <chapter_001.md> [ch2] [ch3]');
    process.exit(2);
  }

  let scoutContent, ch1Content;
  try { scoutContent = fs.readFileSync(path.resolve(scoutFile), 'utf8'); }
  catch (err) { console.error(`无法读取 scout_report: ${err.message}`); process.exit(2); }
  try { ch1Content = fs.readFileSync(path.resolve(ch1File), 'utf8'); }
  catch (err) { console.error(`无法读取第1章: ${err.message}`); process.exit(2); }

  const findings = [];

  // 提取开篇钩子类型
  const hookType = extractOpeningHookType(scoutContent);

  // === 第1章检查 ===
  findings.push(...checkChapter1(ch1Content, hookType));

  // === 第2章检查（如提供）===
  if (ch2File) {
    let ch2Content;
    try { ch2Content = fs.readFileSync(path.resolve(ch2File), 'utf8'); }
    catch (err) { console.error(`无法读取第2章: ${err.message}`); process.exit(2); }
    findings.push(...checkChapter2(ch2Content, hookType));
  }

  // === 第3章检查（如提供）===
  if (ch3File) {
    let ch3Content;
    try { ch3Content = fs.readFileSync(path.resolve(ch3File), 'utf8'); }
    catch (err) { console.error(`无法读取第3章: ${err.message}`); process.exit(2); }
    findings.push(...checkChapter3(ch3Content));
  }

  // 输出结果
  if (findings.length === 0) {
    console.log('✓ 黄金三章结构检查通过');
    process.exit(0);
  }

  const blocking = findings.filter(f => f.severity === 'blocking');
  for (const f of findings) console.log(`[${f.severity}] ${f.message}`);
  console.log(`\n共 ${blocking.length} 个阻塞，${findings.length - blocking.length} 个建议`);
  process.exit(blocking.length > 0 ? 1 : 0);
}

function extractOpeningHookType(content) {
  const match = content.match(/type:\s*(golden_finger|reborn_advantage|meet_cute|mystery_hook|conflict)/);
  return match ? match[1] : 'conflict';
}

function checkChapter1(content, hookType) {
  const findings = [];
  const first300 = content.slice(0, 600); // 约300中文字符

  // 检查1：前300字是否有冲突/钩子
  const hasConflict = checkConflict(first300, hookType);
  if (!hasConflict) {
    findings.push({ severity: 'blocking', message: `第1章前300字未检测到${hookType}类型的开篇钩子` });
  }

  // 检查2：是否有主角出现
  if (!hasProtagonist(content)) {
    findings.push({ severity: 'blocking', message: '第1章未检测到主角' });
  }

  // 检查3：字数检查
  const wordCount = content.length;
  if (wordCount < 2000) {
    findings.push({ severity: 'advisory', message: `第1章字数 ${wordCount} 偏少（建议 3000-4000）` });
  }

  return findings;
}

function checkChapter2(content, hookType) {
  const findings = [];

  // 检查：是否展示了核心优势/金手指
  const hasReveal = checkGoldenFingerReveal(content, hookType);
  if (!hasReveal) {
    findings.push({ severity: 'blocking', message: `第2章未检测到${hookType}类型的核心优势展示` });
  }

  return findings;
}

function checkChapter3(content) {
  const findings = [];

  // 检查：是否有高潮/爽点
  const hasClimax = checkClimax(content);
  if (!hasClimax) {
    findings.push({ severity: 'advisory', message: '第3章未检测到明显的高潮/爽点标记' });
  }

  return findings;
}

function checkConflict(text, hookType) {
  const patterns = {
    golden_finger: [/系统|觉醒|传承|金手指|修炼|灵力|异能/],
    reborn_advantage: [/重生|回到|前世|记忆|未来|先知/],
    meet_cute: [/撞见|意外|相遇|尴尬|心跳|脸红/],
    mystery_hook: [/奇怪|异常|神秘|发现|尸体|线索|疑/],
    conflict: [/冲突|争吵|打架|威胁|挑战|辱|怒|恨/],
  };

  const pats = patterns[hookType] || patterns.conflict;
  return pats.some(p => p.test(text));
}

function hasProtagonist(content) {
  // 简单检查：是否有角色名字（连续2-4个汉字）
  const namePattern = /[\u4e00-\u9fa5]{2,4}/g;
  const matches = content.match(namePattern);
  return matches && matches.length > 10; // 有足够的名字出现
}

function checkGoldenFingerReveal(content, hookType) {
  const patterns = {
    golden_finger: [/系统|能力|功法|传承|觉醒|突破|力量/],
    reborn_advantage: [/先知|预知|未来|信息差|抢先|布局|机会/],
    meet_cute: [/心动|暧昧|火花|感觉|特别|不同|在意/],
    mystery_hook: [/线索|发现|真相|秘密|推理|分析/],
    conflict: [/反击|碾压|震惊|打脸|实力|展示/],
  };

  const pats = patterns[hookType] || patterns.conflict;
  return pats.some(p => p.test(content));
}

function checkClimax(content) {
  const climaxPatterns = [/击败|胜利|成功|突破|逆转|翻盘|碾压|震惊|喝彩|欢呼/];
  return climaxPatterns.some(p => p.test(content));
}

main();
