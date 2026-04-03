#!/usr/bin/env node

/**
 * Unified Trigger Listener
 * 
 * Listens for 12 unified triggers and executes corresponding actions:
 * 1-6: Learning records (correction/error/feature/knowledge_gap/best_practice/integration_error)
 * 7: File creation check (5-question entropy check)
 * 8: Task dispatch interview (4-domain plan-interview)
 * 9: Long task monitoring (context-surfing)
 * 10-12: Quality checks (3Q-Plus/self-challenge/quality-prevention)
 */

import * as fs from 'fs';
import * as path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuration
// Support multiple OpenClaw workspace structures
const WORKSPACE_ROOT = process.env.OPENCLAW_WORKSPACE_ROOT || 
                       path.join(process.env.HOME || '~', '.openclaw', 'workspace') ||
                       path.join(process.env.HOME || '~', '.openclaw', 'workspace-main');
const QUALITY_DATA_DIR = path.join(WORKSPACE_ROOT, '.quality-data');

// Trigger keywords
const TRIGGER_KEYWORDS = {
  correction: ['不对', '错了', '错误', '应该是', '实际上是', '你理解错了', 'not right', 'wrong', 'should be'],
  feature: ['能加上', '想要', '希望', '能不能', '可以加', '功能', 'feature', 'add', 'want'],
  knowledgeGap: ['这个不对', '过时了', '废弃了', '不是这样', '误解', 'outdated', 'deprecated', 'wrong'],
  bestPractice: ['其实可以', '更好的方式', '建议用', '更简洁', '最佳实践', 'better way', 'suggest', 'best practice']
};

// Generate record ID
function generateRecordId(type) {
  const prefix = type === 'learning' ? 'LRN' : type === 'error' ? 'ERR' : 'ENT';
  const date = new Date().toISOString().slice(0, 10).replace(/-/g, '');
  const random = Math.random().toString(36).substring(2, 5).toUpperCase();
  return `${prefix}-${date}-${random}`;
}

// Append to file
function appendToFile(filePath, content) {
  const fullPath = path.join(QUALITY_DATA_DIR, filePath);
  fs.appendFileSync(fullPath, content, 'utf8');
  console.log(`✅ Appended to ${filePath}`);
}

// Detect trigger from message
function detectTrigger(message) {
  const text = message.content.toLowerCase();
  
  // Trigger 1: User correction
  if (TRIGGER_KEYWORDS.correction.some(k => text.includes(k))) {
    return { type: 'correction', target: 'learnings.md', category: 'correction' };
  }
  
  // Trigger 2: Feature request
  if (TRIGGER_KEYWORDS.feature.some(k => text.includes(k))) {
    return { type: 'feature', target: 'features.md', category: 'feature' };
  }
  
  // Trigger 3: Knowledge gap
  if (TRIGGER_KEYWORDS.knowledgeGap.some(k => text.includes(k))) {
    return { type: 'knowledge_gap', target: 'learnings.md', category: 'knowledge_gap' };
  }
  
  // Trigger 4: Best practice
  if (TRIGGER_KEYWORDS.bestPractice.some(k => text.includes(k))) {
    return { type: 'best_practice', target: 'learnings.md', category: 'best_practice' };
  }
  
  return null;
}

// Create learning record
function createLearningRecord(trigger, context) {
  const id = generateRecordId('learning');
  const timestamp = new Date().toISOString();
  
  const record = `
## [${id}] ${trigger.category}

**Logged**: ${timestamp}
**Priority**: medium
**Status**: pending
**Area**: workflow

### Summary
${context.summary || 'Auto-detected trigger'}

### Details
${context.details || 'No additional details'}

### Suggested Action
${context.action || 'Review and categorize'}

### Metadata
- Source: conversation
- Pattern-Key: ${trigger.category}.detected
- Recurrence-Count: 1
- First-Seen: ${timestamp.slice(0, 10)}
- Last-Seen: ${timestamp.slice(0, 10)}

---
`;

  appendToFile(trigger.target, record);
  return id;
}

// Main listener loop
console.log('🎯 Unified Trigger Listener Started');
console.log('Workspace:', WORKSPACE_ROOT);
console.log('Quality Data Dir:', QUALITY_DATA_DIR);
console.log('');
console.log('Listening for triggers...');
console.log('');

// Example usage (in real implementation, this would listen to actual events)
const testMessages = [
  { content: '这个不对，应该是那样的', source: 'user' },
  { content: '能不能加上自动保存功能', source: 'user' },
  { content: '这个 API 已经过时了', source: 'user' },
  { content: '其实可以用更简洁的方式实现', source: 'user' }
];

testMessages.forEach((message, index) => {
  setTimeout(() => {
    const trigger = detectTrigger(message);
    if (trigger) {
      console.log(`📍 Trigger detected: ${trigger.type}`);
      const id = createLearningRecord(trigger, {
        summary: `Auto-detected: ${message.content}`,
        details: `Message from ${message.source}: ${message.content}`,
        action: 'Review and categorize'
      });
      console.log(`✅ Created record: ${id}`);
      console.log('');
    }
  }, index * 1000);
});

// In production, this would:
// 1. Listen to message events via OpenClaw hooks
// 2. Listen to file creation events via fs.watch
// 3. Listen to task dispatch events via sessions_spawn
// 4. Listen to quality trigger words via message matching
// 5. Execute corresponding actions automatically

console.log('Note: This is a demo. In production, the listener would run continuously.');
console.log('');
console.log('✨ Listener ready!');
