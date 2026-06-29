#!/usr/bin/env node
'use strict';

// analyze-metrics.js — CSV 数据解析与指标计算
// Usage: node analyze-metrics.js <csv_file>
// 纯 Node.js 内建模块，无外部依赖。

const fs = require('fs');
const path = require('path');

function main() {
  const csvFile = process.argv[2];
  if (!csvFile) {
    console.error('Usage: node analyze-metrics.js <csv_file>');
    process.exit(2);
  }

  let content;
  try { content = fs.readFileSync(path.resolve(csvFile), 'utf8'); }
  catch (err) { console.error(`无法读取文件: ${err.message}`); process.exit(2); }

  const data = parseCSV(content);
  if (data.length === 0) {
    console.error('无法解析 CSV 数据');
    process.exit(1);
  }

  const metrics = calculateMetrics(data);
  displayResults(metrics);
}

function parseCSV(content) {
  const lines = content.trim().split('\n');
  if (lines.length < 2) return [];

  const headers = lines[0].split(',').map(h => h.trim().toLowerCase());
  const data = [];

  for (let i = 1; i < lines.length; i++) {
    const values = lines[i].split(',').map(v => v.trim());
    if (values.length !== headers.length) continue;

    const row = {};
    headers.forEach((h, idx) => {
      row[h] = isNaN(values[idx]) ? values[idx] : parseFloat(values[idx]);
    });
    data.push(row);
  }

  return data;
}

function calculateMetrics(data) {
  const metrics = {
    total_chapters: data.length,
    chapters: [],
    overall: {},
    anomalies: [],
  };

  let totalRetention = 0;
  let totalCompletion = 0;
  let totalEngagement = 0;

  for (let i = 0; i < data.length; i++) {
    const row = data[i];
    const chapter = {
      number: row.chapter || row['章节'] || (i + 1),
      title: row.title || row['标题'] || '',
      reads: row.reads || row['阅读'] || 0,
      retention_rate: row.retention || row['追读率'] || 0,
      completion_rate: row.completion || row['完读率'] || 0,
      engagement_rate: row.engagement || row['互动率'] || 0,
    };

    // 转换为百分比（如果是小数）
    if (chapter.retention_rate < 1) chapter.retention_rate *= 100;
    if (chapter.completion_rate < 1) chapter.completion_rate *= 100;
    if (chapter.engagement_rate < 1) chapter.engagement_rate *= 100;

    metrics.chapters.push(chapter);

    totalRetention += chapter.retention_rate;
    totalCompletion += chapter.completion_rate;
    totalEngagement += chapter.engagement_rate;

    // 异常检测
    if (i > 0) {
      const prev = data[i - 1];
      const prevRetention = (prev.retention || prev['追读率'] || 0) * ((prev.retention || prev['追读率'] || 0) < 1 ? 100 : 1);
      const drop = prevRetention - chapter.retention_rate;

      if (drop > 15) {
        metrics.anomalies.push({
          chapter: chapter.number,
          type: '追读率骤降',
          severity: drop > 25 ? 'P0' : 'P1',
          drop: drop.toFixed(1) + '%',
        });
      }
    }

    if (chapter.completion_rate < 60) {
      metrics.anomalies.push({
        chapter: chapter.number,
        type: '完读率偏低',
        severity: chapter.completion_rate < 50 ? 'P1' : 'P2',
        value: chapter.completion_rate.toFixed(1) + '%',
      });
    }
  }

  metrics.overall = {
    avg_retention_rate: (totalRetention / data.length).toFixed(1) + '%',
    avg_completion_rate: (totalCompletion / data.length).toFixed(1) + '%',
    avg_engagement_rate: (totalEngagement / data.length).toFixed(1) + '%',
  };

  return metrics;
}

function displayResults(metrics) {
  console.log('== 数据解析结果 ==\n');
  console.log(`总章数: ${metrics.total_chapters}`);
  console.log(`\n总体指标:`);
  console.log(`  平均追读率: ${metrics.overall.avg_retention_rate}`);
  console.log(`  平均完读率: ${metrics.overall.avg_completion_rate}`);
  console.log(`  平均互动率: ${metrics.overall.avg_engagement_rate}`);

  if (metrics.anomalies.length > 0) {
    console.log(`\n异常章节 (${metrics.anomalies.length} 个):`);
    for (const a of metrics.anomalies) {
      console.log(`  [${a.severity}] 第${a.chapter}章: ${a.type} (${a.drop || a.value})`);
    }
  } else {
    console.log('\n未发现明显异常');
  }
}

main();
