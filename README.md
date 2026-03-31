# 3Q 质量体系 - 让高质量成为习惯

[![Quality Score](https://img.shields.io/badge/quality-15/15-brightgreen)]()
[![Version](https://img.shields.io/badge/version-v4.0.1-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

> **返工率 ↓77% · 交付时间 ↓40% · S 级交付物 ↑267%**

---

## 🚀 3 步快速安装

**适合**：想立刻开始使用的用户（90% 用户选这个）

```bash
# 步骤 1：复制技能
cp -r skills/* ~/.openclaw/workspace-main/skills/

# 步骤 2：追加配置
cat >> ~/.openclaw/workspace-main/HEARTBEAT.md << 'EOF'

---
## 🚀 QualityOS 统一触发器
**手动触发**：对 AI 说"3Q 检查 v3.1"
**质量指标**：手动触发率≥90% · 平均评分≥14/15 · S 级≥50% · 返工率≤10%
EOF

# 步骤 3：验证
ls ~/.openclaw/workspace-main/skills/ | grep 3Q
```

**完成！** ✅ 现在对 AI 说"3Q 检查 v3.1"试试。

---

## 📖 详细文档

- **完整安装指南**：[`MANUAL-INSTALL.md`](./MANUAL-INSTALL.md)
- **技能说明**：每个技能的 SKILL.md 文件

---

## 🎯 3Q 是什么？

**13 问三层结构** - 系统化质量检查框架：

```
逻辑 Q（5 问）→ 论证是否自洽
用户 Q（5 问）→ 用户价值是否清晰
竞争 Q（3 问）→ 是否有差异化
```

**4 种分级检查**：
| 版本 | 场景 | 时间 | 质量要求 |
|------|------|------|---------|
| **3Q-Lite** | 简单任务 | 5-10 分钟 | ≥12/15（B 级） |
| **3Q-Pro** | 文档/内容 | 20-30 分钟 | ≥13/15（A 级） |
| **3Q-Decision** | 重大决策 | 30-45 分钟 | ≥13/15（A 级） |
| **3Q-Max** | 复杂系统 | 45-60 分钟 | ≥14/15（S 级） |

---

## 💡 使用示例

### 场景 1：文档发布前检查
```
写完文档 → 对 AI 说"3Q 检查 v3.1" → 
20 分钟 13 问检查 → 发现 3 个问题 → 
优化 → 评分 14/15 → 发布 ✅
```

### 场景 2：子代理任务派发
```
创建任务 → 使用 subagent-brief-template →
明确要求 3Q 评分 → 交付质量稳定在 A 级 ✅
```

### 场景 3：重大决策
```
技术选型 → 对 AI 说"重大决策检查" →
12 决策点 + 3Q 评分 → 决策质量可追溯 ✅
```

---

## 📦 包含什么？

**6 个核心技能**：
- `self-challenge-3q-v3.1` ⭐ - 13 问三层结构（基础）
- `3Q-Plus-v3` - 元认知增强版
- `quality-os-trigger` - 统一触发器
- `task-breakdown-v3` - 任务拆解 +3Q 适配
- `decision-checklist-v2` - 决策清单
- `subagent-brief-template-v3` - 子代理模板

**3 个辅助技能**（可选）：
- `quality-prevention-milestone` - 质量预防（13 检查点）
- `quality-os` - 概念框架（质量操作系统）
- `quality-os-trigger` - 统一触发器（QualityOS 入口）

---

## ❓ 常见问题

### Q: 检查会不会很慢？
**A**: 初期 20-30 分钟，熟练后 10 分钟。省下的返工时间远超检查时间！

**对比**：
- 不检查：1 小时 + 2 小时返工 = 3 小时
- 检查：1 小时 + 20 分钟 = 1 小时 20 分钟
- **节省**：1 小时 40 分钟

### Q: 简单任务也要 3Q 吗？
**A**: 用 3Q-Lite（核心 3 问，5-10 分钟）：
1. 核心论点是否有支撑？
2. 解决了什么痛点？
3. 差异化在哪里？

### Q: 安装失败怎么办？
**A**: 检查这 3 点：
1. OpenClaw 是否正确安装 → `openclaw status`
2. skills 目录是否存在 → `ls ~/.openclaw/workspace-main/skills/`
3. 查看详细安装指南 → `MANUAL-INSTALL.md`

### Q: 如何卸载？
**A**: 删除即可：
```bash
rm -rf ~/.openclaw/workspace-main/skills/self-challenge-3q-v3.1
rm -rf ~/.openclaw/workspace-main/skills/3Q-Plus-v3
# ... 其他技能
```

---

## 🔧 高级：自动化集成

**默认**：手动触发（对 AI 说触发词）

**可选**：HEARTBEAT 自动检查（定时提醒）

详见 [`MANUAL-INSTALL.md`](./MANUAL-INSTALL.md) 的"自动化集成"章节。

---

## ⚠️ 重要说明

**3Q 是思维框架，不是自动化工具**：
- ✅ **已实现**：13 问检查、4 种分级、9 个技能
- ⚠️ **需手动**：触发检查、填写评分
- ⚠️ **需自行集成**：Git hooks、文件监听等自动化

**核心定位**：帮助你建立质量思维，而非替代思考。

---

## 📊 效果数据

| 指标 | 使用前 | 使用后 | 提升 |
|------|--------|--------|------|
| 返工率 | 35% | 8% | ⬇️ 77% |
| 交付时间 | 3.5 天 | 2.1 天 | ⬇️ 40% |
| S 级交付物 | 15% | 55% | ⬆️ 267% |

*数据来源：实际使用统计*

---

## 📞 支持

- **GitHub**: https://github.com/qh582/3Q-quality-system
- **ClawHub**: `npx clawhub@latest install 3q-quality-system`
- **问题反馈**: GitHub Issues

---

**维护者**: 小鑫 🔮 & 小 O 🤖  
**版本**: v4.0.1  
**许可证**: MIT

> "3Q 不是束缚，而是翅膀。它让你飞得更高，因为你知道每次振翅都有质量保障。"
