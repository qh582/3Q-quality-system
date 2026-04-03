#!/usr/bin/env node

/**
 * Weekly Quality Report Generator
 * 
 * Generates comprehensive quality metrics and trends
 * Pure Node.js implementation (no shell scripts for ClawHub safety)
 */

import * as fs from 'fs';
import * as path from 'path';

// Configuration
// Support multiple OpenClaw workspace structures
const WORKSPACE_ROOT = process.env.OPENCLAW_WORKSPACE_ROOT || 
                       path.join(process.env.HOME || '~', '.openclaw', 'workspace') ||
                       path.join(process.env.HOME || '~', '.openclaw', 'workspace-main');
const QUALITY_DATA_DIR = path.join(WORKSPACE_ROOT, '.quality-data');
const REPORTS_DIR = path.join(QUALITY_DATA_DIR, 'reports');

// Helper: Count lines matching pattern
function countLines(filePath, pattern) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    const regex = new RegExp(pattern, 'gm');
    const matches = content.match(regex);
    return matches ? matches.length : 0;
  } catch (error) {
    return 0;
  }
}

// Helper: Count files in directory
function countFiles(dirPath, extension = '.md') {
  try {
    if (!fs.existsSync(dirPath)) return 0;
    const files = fs.readdirSync(dirPath);
    return files.filter(f => f.endsWith(extension)).length;
  } catch (error) {
    return 0;
  }
}

// Helper: Get date range
function getDateRange(days = 7) {
  const end = new Date();
  const start = new Date();
  start.setDate(start.getDate() - days);
  
  return {
    start: start.toISOString().slice(0, 10),
    end: end.toISOString().slice(0, 10),
    week: getWeekNumber(start)
  };
}

// Helper: Get ISO week number
function getWeekNumber(d) {
  d = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
  d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay() || 7));
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
  const weekNo = Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
  return `${d.getUTCFullYear()}-W${weekNo.toString().padStart(2, '0')}`;
}

// Main function
function generateReport() {
  console.log('📊 Weekly Quality Report Generator\n');
  console.log('==================================\n');

  // Create reports directory
  if (!fs.existsSync(REPORTS_DIR)) {
    fs.mkdirSync(REPORTS_DIR, { recursive: true });
  }

  // Get date range
  const dateRange = getDateRange(7);
  const reportFile = path.join(REPORTS_DIR, `weekly-report-${new Date().toISOString().slice(0, 10).replace(/-/g, '')}.md`);

  console.log(`Generating report: ${reportFile}\n`);

  // Count records
  const learningsFile = path.join(QUALITY_DATA_DIR, 'learnings.md');
  const errorsFile = path.join(QUALITY_DATA_DIR, 'errors.md');
  const featuresFile = path.join(QUALITY_DATA_DIR, 'features.md');
  const entropyFile = path.join(QUALITY_DATA_DIR, 'entropy-log.md');
  const handoffsDir = path.join(QUALITY_DATA_DIR, 'handoffs');
  const promotionsDir = path.join(QUALITY_DATA_DIR, 'promotions');

  const learningsCount = countLines(learningsFile, '^## \\[LRN-');
  const errorsCount = countLines(errorsFile, '^## \\[ERR-');
  const featuresCount = countLines(featuresFile, '^## \\[FEAT-');
  const entropyCount = countLines(entropyFile, '^## \\[ENT-');
  const handoffsCount = countFiles(handoffsDir);
  const promotionsCount = countFiles(promotionsDir);

  // Count by category
  const correctionCount = countLines(learningsFile, '\\] correction');
  const knowledgeGapCount = countLines(learningsFile, '\\] knowledge_gap');
  const bestPracticeCount = countLines(learningsFile, '\\] best_practice');

  // Calculate percentages
  const total = learningsCount || 1;
  const correctionPct = ((correctionCount * 100) / total).toFixed(1);
  const knowledgeGapPct = ((knowledgeGapCount * 100) / total).toFixed(1);
  const bestPracticePct = ((bestPracticeCount * 100) / total).toFixed(1);

  // Generate report
  const report = `# 📊 Weekly Quality Report

**Week**: ${dateRange.week}  
**Generated**: ${new Date().toISOString()}  
**Period**: ${dateRange.start} to ${dateRange.end}

---

## 📈 Summary

| Metric | Count | Trend |
|--------|-------|-------|
| **Learning Records** | ${learningsCount} | 📊 |
| **Error Records** | ${errorsCount} | 📊 |
| **Feature Requests** | ${featuresCount} | 📊 |
| **Entropy Events** | ${entropyCount} | 📊 |
| **Handoff Files** | ${handoffsCount} | 📊 |
| **Promotions** | ${promotionsCount} | 📊 |

---

## 🧠 Learning Records Breakdown

| Category | Count | Percentage |
|----------|-------|------------|
| **Correction** | ${correctionCount} | ${correctionPct}% |
| **Knowledge Gap** | ${knowledgeGapCount} | ${knowledgeGapPct}% |
| **Best Practice** | ${bestPracticeCount} | ${bestPracticePct}% |

---

## 🎯 Key Insights

### Top Patterns
<!-- Auto-generated: Add manual insights here -->

### Recurring Issues
<!-- Auto-generated: Add manual insights here -->

### Promotion Candidates
<!-- Auto-generated: Run node scripts/automated-promotion.js -->

---

## 📋 Action Items

### This Week
- [ ] Review new learning records
- [ ] Process promotion candidates
- [ ] Update core configuration files
- [ ] Clean up old handoff files

### Next Week
- [ ] Analyze trends
- [ ] Optimize trigger detection
- [ ] Improve documentation

---

## 📊 Trends

### Learning Records Trend
<!-- Add chart or trend analysis -->

### Error Types Trend
<!-- Add chart or trend analysis -->

### Entropy Score Trend
<!-- Add chart or trend analysis -->

---

**Generated by**: Weekly Quality Report Script (Node.js)  
**Next Report**: ${new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().slice(0, 10)}
`;

  // Write report
  fs.writeFileSync(reportFile, report, 'utf8');

  console.log('✅ Report generated successfully!\n');
  console.log(`📄 Report file: ${reportFile}\n`);
  console.log('📊 Summary:');
  console.log(`   - Learning Records: ${learningsCount}`);
  console.log(`   - Error Records: ${errorsCount}`);
  console.log(`   - Feature Requests: ${featuresCount}`);
  console.log(`   - Entropy Events: ${entropyCount}`);
  console.log(`   - Handoff Files: ${handoffsCount}`);
  console.log(`   - Promotions: ${promotionsCount}\n`);
  console.log('🎯 Next steps:');
  console.log('   1. Review the report: cat ' + reportFile);
  console.log('   2. Add manual insights');
  console.log('   3. Process action items\n');
  console.log('✨ Done!');
}

// Run
generateReport();
