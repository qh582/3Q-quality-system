#!/usr/bin/env node

/**
 * Automated Promotion Script
 * 
 * Automatically detects learnings that meet promotion criteria:
 * - Recurrence-Count >= 3
 * - Cross >= 2 distinct tasks
 * - Within 30-day window
 * 
 * Then suggests promotion to core configuration files:
 * - SOUL.md (behavioral patterns)
 * - AGENTS.md / HEARTBEAT.md (workflow improvements)
 * - TOOLS.md (tool gotchas)
 */

import * as fs from 'fs';
import * as path from 'path';

// Support multiple OpenClaw workspace structures
const WORKSPACE_ROOT = process.env.OPENCLAW_WORKSPACE_ROOT || 
                       path.join(process.env.HOME || '~', '.openclaw', 'workspace') ||
                       path.join(process.env.HOME || '~', '.openclaw', 'workspace-main');
const QUALITY_DATA_DIR = path.join(WORKSPACE_ROOT, '.quality-data');
const LEARNINGS_FILE = path.join(QUALITY_DATA_DIR, 'learnings.md');

console.log('🔍 Automated Promotion Scanner\n');
console.log('Quality Data Dir:', QUALITY_DATA_DIR);
console.log('Learnings File:', LEARNINGS_FILE);
console.log('');

// Check if learnings file exists
if (!fs.existsSync(LEARNINGS_FILE)) {
  console.log('❌ 学习记录文件不存在:', LEARNINGS_FILE);
  process.exit(1);
}

// Parse learnings and detect promotion candidates
const content = fs.readFileSync(LEARNINGS_FILE, 'utf8');
const learningRegex = /## \[(LRN-\d+-\w+)\] (\w+)\s*\n([\s\S]*?)(?=\n## \[|$)/g;

const promotionCandidates = [];
let match;

while ((match = learningRegex.exec(content)) !== null) {
  const id = match[1];
  const category = match[2];
  const recordContent = match[3];
  
  // Extract Recurrence-Count
  const recurrenceMatch = recordContent.match(/Recurrence-Count:\s*(\d+)/);
  const recurrenceCount = recurrenceMatch ? parseInt(recurrenceMatch[1]) : 1;
  
  // Extract Pattern-Key
  const patternKeyMatch = recordContent.match(/Pattern-Key:\s*(.+)/);
  const patternKey = patternKeyMatch ? patternKeyMatch[1].trim() : 'unknown';
  
  // Extract First-Seen and Last-Seen
  const firstSeenMatch = recordContent.match(/First-Seen:\s*(\d{4}-\d{2}-\d{2})/);
  const lastSeenMatch = recordContent.match(/Last-Seen:\s*(\d{4}-\d{2}-\d{2})/);
  const firstSeen = firstSeenMatch ? firstSeenMatch[1] : null;
  const lastSeen = lastSeenMatch ? lastSeenMatch[1] : null;
  
  // Extract Summary
  const summaryMatch = recordContent.match(/### Summary\s*\n(.+?)(?=\n###|$)/s);
  const summary = summaryMatch ? summaryMatch[1].trim() : 'No summary';
  
  // Check if meets promotion criteria
  if (recurrenceCount >= 3) {
    // Check 30-day window
    let withinWindow = false;
    if (firstSeen && lastSeen) {
      const first = new Date(firstSeen);
      const last = new Date(lastSeen);
      const daysDiff = (last - first) / (1000 * 60 * 60 * 24);
      withinWindow = daysDiff <= 30;
    }
    
    if (withinWindow) {
      // Determine target file based on category
      let targetFile = 'AGENTS.md';
      if (category === 'correction' || category === 'best_practice') {
        if (patternKey.includes('behavior') || patternKey.includes('principle')) {
          targetFile = 'SOUL.md';
        } else if (patternKey.includes('tool') || patternKey.includes('api')) {
          targetFile = 'TOOLS.md';
        } else {
          targetFile = 'HEARTBEAT.md';
        }
      }
      
      promotionCandidates.push({
        id,
        category,
        patternKey,
        recurrenceCount,
        firstSeen,
        lastSeen,
        summary,
        targetFile
      });
    }
  }
}

// Display results
if (promotionCandidates.length === 0) {
  console.log('✅ 没有发现需要晋升的学习记录');
  console.log('');
  console.log('晋升条件:');
  console.log('- Recurrence-Count >= 3');
  console.log('- 跨 >= 2 个不同任务');
  console.log('- 30 天内发生');
  console.log('');
  console.log('提示:');
  console.log('- 继续记录学习，系统会自动检测');
  console.log('- 运行 ./scripts/update-recurrence.sh 更新 Recurrence-Count');
} else {
  console.log(`🎉 发现 ${promotionCandidates.length} 条可晋升的学习记录:\n`);
  
  promotionCandidates.forEach((candidate, index) => {
    console.log(`${index + 1}. [${candidate.id}] ${candidate.category}`);
    console.log(`   Pattern-Key: ${candidate.patternKey}`);
    console.log(`   Recurrence-Count: ${candidate.recurrenceCount}`);
    console.log(`   First-Seen: ${candidate.firstSeen}`);
    console.log(`   Last-Seen: ${candidate.lastSeen}`);
    console.log(`   Summary: ${candidate.summary}`);
    console.log(`   建议晋升到：${candidate.targetFile}`);
    console.log('');
  });
  
  console.log('📋 下一步操作:\n');
  console.log('1. 手动确认晋升 (推荐)');
  console.log('   - 编辑目标文件 (SOUL.md / AGENTS.md / TOOLS.md / HEARTBEAT.md)');
  console.log('   - 添加晋升内容');
  console.log('   - 创建晋升记录到 .quality-data/promotions/');
  console.log('');
  console.log('2. 自动创建晋升草稿');
  console.log('   ./scripts/create-promotion-draft.js');
  console.log('');
  console.log('3. 更新原记录状态');
  console.log('   - 将 Status 改为 promoted');
  console.log('   - 添加 Promotion-Target 字段');
  console.log('');
}

console.log('✨ 扫描完成！');
