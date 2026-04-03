#!/usr/bin/env node

/**
 * 3Q 自进化框架 - 安装脚本
 * 
 * 安全安装：只复制文件，不执行系统命令
 * 跨平台支持：Windows / Mac / Linux
 */

const fs = require('fs');
const path = require('path');

// 颜色输出
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  blue: '\x1b[34m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
  cyan: '\x1b[36m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

// 配置
const CONFIG = {
  skills: [
    'quality-os-trigger',
    '3Q-Plus-v3',
    'self-challenge-3q-v3.1',
    'quality-prevention-milestone',
    'task-breakdown',
    'subagent-brief-template',
    'decision-checklist',
    'quality-os'
  ],
  // 支持多种 OpenClaw 工作区结构
  targetDir: process.env.OPENCLAW_WORKSPACE || 
             path.join(process.env.HOME || '~', '.openclaw', 'workspace', 'skills') ||
             path.join(process.env.HOME || '~', '.openclaw', 'workspace-main', 'skills')
};

// 检查目标目录
function checkTargetDir() {
  if (!fs.existsSync(CONFIG.targetDir)) {
    log(`❌ 未找到 OpenClaw 工作目录：${CONFIG.targetDir}`, 'red');
    log('\n请确认：', 'yellow');
    log('1. OpenClaw 已正确安装');
    log('2. 或者设置环境变量：export OPENCLAW_WORKSPACE=/your/workspace/path\n');
    return false;
  }
  return true;
}

// 复制技能
function installSkills() {
  const sourceDir = path.join(__dirname, '..', 'skills');
  let successCount = 0;
  let skipCount = 0;

  log('\n📦 开始安装技能...\n', 'blue');

  CONFIG.skills.forEach(skill => {
    const sourcePath = path.join(sourceDir, skill);
    const targetPath = path.join(CONFIG.targetDir, skill);

    if (!fs.existsSync(sourcePath)) {
      log(`⚠️  跳过：${skill}（源文件不存在）`, 'yellow');
      skipCount++;
      return;
    }

    if (fs.existsSync(targetPath)) {
      log(`⚠️  跳过：${skill}（已存在）`, 'yellow');
      skipCount++;
      return;
    }

    try {
      // 递归复制目录
      fs.cpSync(sourcePath, targetPath, { recursive: true });
      log(`✅ 已安装：${skill}`, 'green');
      successCount++;
    } catch (error) {
      log(`❌ 安装失败：${skill} - ${error.message}`, 'red');
    }
  });

  log(`\n📊 安装完成：${successCount} 个成功，${skipCount} 个跳过`, 'blue');
  return successCount;
}

// 显示使用说明
function showUsage() {
  log('\n' + '='.repeat(60), 'cyan');
  log('🎉 3Q 自进化框架安装完成！', 'green');
  log('='.repeat(60), 'cyan');
  log('\n📚 下一步：', 'blue');
  log('1. 重启 OpenClaw 或执行 /reload');
  log('2. 对 AI 说："3Q 检查" 测试安装');
  log('3. 阅读 README.md 了解完整功能\n');
  log('🔗 文档：https://github.com/qh582/3Q-quality-system\n');
}

// 主函数
function main() {
  log('\n' + '='.repeat(60), 'cyan');
  log('🚀 3Q 自进化框架 - 安装程序', 'cyan');
  log('='.repeat(60), 'cyan');

  if (!checkTargetDir()) {
    process.exit(1);
  }

  const successCount = installSkills();
  
  if (successCount > 0) {
    showUsage();
  } else {
    log('\n⚠️  没有安装新技能（可能已全部存在）\n', 'yellow');
  }
}

// 运行
main();
