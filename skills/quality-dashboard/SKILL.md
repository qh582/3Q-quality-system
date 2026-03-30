---
name: quality-dashboard
version: v1.0.0
type: tool
owner: 小 O
quality_score: 13/15
last_updated: 2026-03-30
depends_on: []
triggers:
  - "质量仪表板"
  - "生成 dashboard"
  - "quality dashboard"
  - "quality metrics"
best_for: 生成质量指标可视化仪表板
scenarios:
  - "每周质量回顾"
  - "质量指标可视化"
  - "团队质量报告"
---

# quality-dashboard - 质量仪表板生成器

## 🌐 English Summary

**Quality Metrics Visualization Dashboard Generator**

Generates visual dashboards for quality tracking:

**Metrics Tracked**:
- Auto-trigger rate (target: ≥90%)
- Average quality score (target: ≥14/15)
- S-grade deliverable rate (target: ≥50%)
- Rework rate (target: ≤10%)

**Output**:
- Trend charts (weekly/monthly)
- Quality distribution pie chart
- Improvement recommendations
- Markdown/PDF report export

**Use Case**: Weekly quality review, team quality reporting

**Effect**: Visual quality tracking, data-driven improvement

**Triggers**: `质量仪表板`, `生成 dashboard`, `quality dashboard`

---

## 📖 详细文档

## 📖 Overview

**quality-dashboard** 是 3Q 质量体系的数据可视化工具。

**适用场景**：
- 每周质量回顾
- 质量指标可视化
- 团队质量报告

## ✨ Capabilities

### 核心能力
1. **质量指标收集** - 自动收集 3Q 评分数据
2. **可视化生成** - 生成图表和趋势分析
3. **报告导出** - 导出 Markdown/PDF 报告

## 🔧 使用方式

```bash
# 生成质量仪表板
python skills/quality-dashboard/generate_dashboard.py

# 输出：dashboard.md（质量指标可视化）
```

## 📊 输出内容

- 自动触发率趋势
- 平均质量评分
- S 级交付物比例
- 返工率变化

---

**维护者**: 小 O 🤖  
**最后更新**: 2026-03-30
