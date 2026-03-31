# Changelog

All notable changes to the 3Q Quality System will be documented in this file.

---

## [4.0.1] - 2026-03-31

### 🔧 Fixed (ClawHub 审核问题修复)

#### 问题 1：文档夸大自动触发功能
- ❌ **问题**：README 声称"文档保存/代码提交时自动触发"，但无实际实现
- ✅ **修复**：
  - 修改定位为"手动质量检查框架"
  - 删除"自动触发"表述，改为"手动触发 + HEARTBEAT 集成"
  - 新增"🔧 自动化集成"章节，说明 3 种集成方案（HEARTBEAT/Git Hooks/文件监听）
  - 明确标注 HEARTBEAT 已集成，其他需自行开发

#### 问题 2：外部依赖未声明
- ❌ **问题**：SKILL.md 提及 feishu_task_task API 和 Python 脚本，但未声明
- ✅ **修复**：
  - 删除 `task-breakdown/SKILL.md` 中的 `feishu_task_task` 依赖
  - 删除 `quality-dashboard/SKILL.md` 中的 `generate_dashboard.py` 引用
  - 修改为通过 OpenClaw 技能实现，不依赖外部 API 或脚本
  - 在 `package.json` 中添加 `notes` 字段明确说明：
    - 不依赖任何外部 API
    - 不包含 Python 脚本
    - Git hooks/文件监听需自行集成

#### 问题 3：安装脚本未提示用户
- ❌ **问题**：install.sh 修改用户配置但未提前告知
- ✅ **修复**：
  - ~~在安装前增加用户确认步骤~~ → 改为手动安装指南
  - 创建 `MANUAL-INSTALL.md`，详细说明每一步
  - 用户可自主选择是否执行配置步骤

#### 问题 4：缺少免责声明
- ❌ **问题**：未说明技能包的定位和限制
- ✅ **修复**：
  - 在 README 开头添加定位说明
  - 在 README 结尾添加免责声明
  - 明确标注"已实现"vs"需自行集成"vs"不包含"

#### 问题 5：ClawHub 不允许 .sh 文件（新增）
- ❌ **问题**：ClawHub 只允许 .md 文件，不允许 shell 脚本
- ✅ **修复**：
  - 删除 `install.sh`
  - 创建 `MANUAL-INSTALL.md` 手动安装指南
  - 修改 `README.md` 移除脚本引用
  - 修改 `package.json` 删除 `scripts` 字段

### 📝 Changed

#### README.md
- 标题修改："OpenClaw 质量保障系统" → "手动质量检查框架"
- 新增"⚠️ 重要说明（安装前必读）"章节
- 修改"自动触发机制" → "触发方式"（手动 + 自动集成）
- 修改使用案例中的"自动"表述为"手动"
- 新增"🔧 自动化集成"章节（HEARTBEAT/Git Hooks/文件监听）
- 新增"⚠️ 免责声明"章节
- 修改 FAQ 中关于自动触发的回答

#### package.json
- 新增 `requirements` 字段
- 新增 `optionalIntegrations` 字段
- 新增 `notes` 字段（说明自动触发/API/Python）
- 修改 `features`：删除"自动触发机制"，改为"HEARTBEAT 集成"
- 新增 `manualTriggers: true`
- 新增 `autoTriggerNote`

#### install.sh
- 步骤 1 增加用户确认
- 明确列出将被修改的文件
- 用户可取消安装

#### skills/task-breakdown/SKILL.md
- 删除 `api_used: feishu_task_task`
- 删除 `scripts: []`
- 简化依赖声明格式

#### skills/quality-dashboard/SKILL.md
- 删除 Python 脚本引用
- 修改使用方式为"手动触发 + HEARTBEAT 自动触发"

### 📚 Documentation

- 核心定位：从"自动触发系统"重新定位为"思维框架 + 技能包集合"
- 明确说明：自动化是锦上添花，思维转变才是核心
- 推荐方案：90% 用户使用 HEARTBEAT 方案即可

### 🎯 Impact

**ClawHub 审核状态**：✅ 预计通过

**用户影响**：
- ✅ 更清晰的定位和期望管理
- ✅ 安装前明确告知修改内容
- ✅ 无外部依赖，降低使用门槛
- ⚠️ 自动触发功能需自行集成（HEARTBEAT 除外）

**向后兼容性**：
- ✅ 已安装用户不受影响
- ✅ 所有技能功能保持不变
- ⚠️ 文档表述更保守，避免夸大

---

## [4.0.0] - 2026-03-30

### 🎉 Initial Release

- 13 问三层结构（逻辑 5+ 用户 5+ 竞争 3）
- 4 种分级检查版本（Max/Pro/Lite/Decision）
- 9 个完整技能（6 核心 +3 辅助）
- HEARTBEAT 集成
- 一键安装脚本

---

**版本规范**：遵循 Semantic Versioning (MAJOR.MINOR.PATCH)

**发布说明**：
- v4.0.1 是 v4.0.0 的修复版本，解决 ClawHub 审核问题
- 所有功能向后兼容
- 核心定位调整，但技能包功能不变
