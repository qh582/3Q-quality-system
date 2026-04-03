#!/usr/bin/env node

/**
 * 3Q 自进化框架 - 健康检查脚本
 * 
 * 检查已安装技能的状态和版本
 */

const fs = require('fs');
const path = require('path');

const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
  cyan: '\x1b[36m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

// 检查技能
function checkSkills() {
  // 支持多种 OpenClaw 工作区结构
  const workspace = process.env.OPENCLAW_WORKSPACE || 
                    path.join(require('os').homedir(), '.openclaw', 'workspace', 'skills') ||
                    path.join(require('os').homedir(), '.openclaw', 'workspace-main', 'skills');
  
  const requiredSkills = [
    'quality-os-trigger',
    '3Q-Plus-v3',
    'self-challenge-3q-v3.1',
    'quality-prevention-milestone',
    'task-breakdown',
    'subagent-brief-template',
    'decision-checklist'
  ];

  log('\n🔍 检查技能安装状态...\n', 'cyan');

  let allGood = true;

  requiredSkills.forEach(skill => {
    const skillPath = path.join(workspace, skill, 'SKILL.md');
    
    if (fs.existsSync(skillPath)) {
      log(`✅ ${skill}`, 'green');
    } else {
      log(`❌ ${skill} - 未找到`, 'red');
      allGood = false;
    }
  });

  return allGood;
}

// 检查触发词
function checkTriggers() {
  log('\n🎯 测试触发词...\n', 'cyan');
  
  const triggers = [
    '3Q 检查',
    '质量评分',
    '自我挑战',
    'Simplify and Harden'
  ];

  triggers.forEach(trigger => {
    log(`  - "${trigger}"`, 'yellow');
  });

  log('\n💡 在 OpenClaw 中对 AI 说以上任一触发词测试\n', 'cyan');
}

// 主函数
function main() {
  log('\n' + '='.repeat(60), 'cyan');
  log('🏥 3Q 自进化框架 - 健康检查', 'cyan');
  log('='.repeat(60), 'cyan');

  const allGood = checkSkills();
  checkTriggers();

  if (allGood) {
    log('\n✅ 所有技能已正确安装！\n', 'green');
  } else {
    log('\n⚠️  部分技能缺失，请运行：npx 3q-install\n', 'yellow');
  }
}

main();
