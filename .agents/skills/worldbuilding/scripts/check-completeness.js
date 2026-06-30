#!/usr/bin/env node
'use strict';

// check-completeness.js — 世界观完整性检查
// Usage: node check-completeness.js <scout_report.yaml> <worldbuilding.yaml>
//
// 读取 scout_report.yaml 中 required_elements.worldbuilding.required，
// 检查 worldbuilding.yaml 中对应元素是否存在且非空。
// 纯 Node.js 内建模块，无外部依赖。支持嵌套路径检查（如 lore.history）。

const fs = require('fs');
const path = require('path');

function main() {
  const scoutFile = process.argv[2];
  const worldFile = process.argv[3];

  if (!scoutFile || !worldFile) {
    console.error('Usage: node check-completeness.js <scout_report.yaml> <worldbuilding.yaml>');
    process.exit(2);
  }

  const scoutPath = path.resolve(scoutFile);
  const worldPath = path.resolve(worldFile);

  let scoutContent, worldContent;
  try {
    scoutContent = fs.readFileSync(scoutPath, 'utf8');
  } catch (err) {
    console.error(`无法读取 scout_report: ${scoutFile} (${err.message})`);
    process.exit(2);
  }
  try {
    worldContent = fs.readFileSync(worldPath, 'utf8');
  } catch (err) {
    console.error(`无法读取 worldbuilding: ${worldFile} (${err.message})`);
    process.exit(2);
  }

  // 从 scout_report 中提取 required_elements.worldbuilding.required 列表
  const required = extractRequiredElements(scoutContent);
  if (required.length === 0) {
    console.log('⚠ 未声明 required_elements.worldbuilding.required，跳过检查');
    process.exit(0);
  }

  // 检查 worldbuilding.yaml 中每个必需元素是否存在
  const findings = [];
  for (const elem of required) {
    if (!hasElement(worldContent, elem)) {
      findings.push({
        severity: 'blocking',
        element: elem,
        message: `缺少必需的世界观元素 (或该元素为空): ${elem}`,
      });
    }
  }

  // 输出结果
  if (findings.length === 0) {
    console.log(`✓ 世界观完整性检查通过（${required.length} 个必需元素）`);
    process.exit(0);
  }

  for (const f of findings) {
    console.log(`[${f.severity}] ${f.message}`);
  }
  process.exit(1);
}

function extractRequiredElements(content) {
  const elements = [];
  const worldbuildingMatch = content.match(/worldbuilding:\s*\n([\s\S]*?)(?=\n\s*\w|\n\s*#|$)/);
  if (!worldbuildingMatch) return elements;

  const worldbuildingSection = worldbuildingMatch[1];
  const requiredMatch = worldbuildingSection.match(/required:\s*\n([\s\S]*?)(?=\n\s*\w|\n\s*#|$)/);
  if (!requiredMatch) return elements;

  const requiredSection = requiredMatch[1];
  const lines = requiredSection.split('\n');

  for (const line of lines) {
    const match = line.match(/^\s+-\s+(.+)/);
    if (match) {
      elements.push(match[1].trim().replace(/^["']|["']$/g, ''));
    }
  }
  return elements;
}

/**
 * 检查 YAML 内容中是否存在指定的路径元素（支持点分隔的嵌套路径，例如 lore.history）
 * 并且该元素不能为空（即包含有效的值或子节点）
 */
function hasElement(content, elementPath) {
  const parts = elementPath.split('.');
  const lines = content.split('\n');
  
  let currentPartIndex = 0;
  let currentExpectedIndent = 0; // The minimum indent we expect for the current part
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    // 去除整行注释和空行
    if (line.trim().startsWith('#') || line.trim() === '') continue;
    
    // 匹配 key
    const match = line.match(/^(\s*)([\w_]+):(.*)/);
    if (!match) continue;
    
    const indent = match[1].length;
    const key = match[2];
    let rest = match[3].trim();
    // 剥离行内注释
    if (rest.includes('#')) {
      rest = rest.split('#')[0].trim();
    }
    
    // 如果缩进回退到了上层，说明我们要找的嵌套路径断了，重置状态
    if (indent < currentExpectedIndent) {
       currentPartIndex = 0;
       currentExpectedIndent = 0;
    }
    
    if (indent === currentExpectedIndent && key === parts[currentPartIndex]) {
      if (currentPartIndex === parts.length - 1) {
        // 找到了最后一级 key，检查是否为空
        // 1. 如果该行不仅有 key 还有 value (例如 core_rules: "some value" 或 core_rules: [])
        if (rest !== '' && rest !== '[]' && rest !== '{}' && rest !== '""' && rest !== "''") {
          return true;
        }
        // 2. 检查后续行是否有属于该 key 的子元素（缩进大于当前缩进，或者是数组项）
        for (let j = i + 1; j < lines.length; j++) {
          const nextLine = lines[j];
          if (nextLine.trim().startsWith('#') || nextLine.trim() === '') continue;
          
          const nextIndentMatch = nextLine.match(/^(\s*)/);
          const nextIndent = nextIndentMatch ? nextIndentMatch[1].length : 0;
          
          if (nextIndent > indent) {
            return true; // 发现子元素，判定为非空
          } else {
            break; // 遇到了同级或更高级的节点，说明该 key 下面没有内容了
          }
        }
        return false;
      } else {
        // 匹配到了中间层级，继续往下找
        currentPartIndex++;
        // YAML 嵌套规范中，子节点必定有更大的缩进
        // 我们不锁定确切的缩进数，只要求后续的查找在当前缩进之下即可（但为了严谨，我们直接找接下来的结构）
        // 实际上这部分可以更健壮，但对于我们的一般用法足矣
        currentExpectedIndent = indent + 2; 
        
        // 我们需要动态找到真实的下层缩进
        for (let j = i + 1; j < lines.length; j++) {
           const nextLine = lines[j];
           if (nextLine.trim().startsWith('#') || nextLine.trim() === '') continue;
           const nextIndentMatch = nextLine.match(/^(\s*)/);
           if (nextIndentMatch && nextIndentMatch[1].length > indent) {
               currentExpectedIndent = nextIndentMatch[1].length;
           }
           break;
        }
      }
    }
  }
  return false;
}

main();
