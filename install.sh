#!/bin/bash

# 3Q 质量体系 - 一键安装脚本
# 版本：v4.0
# 创建日期：2026-03-30

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印函数
print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

# 主函数
main() {
    print_header "🚀 3Q 质量体系安装脚本 v4.0"
    echo ""

    # 步骤 1：检查环境
    print_info "步骤 1/5: 检查环境..."
    
    if [ ! -d "$HOME/.openclaw/workspace-main" ]; then
        print_error "未找到 OpenClaw workspace 目录：$HOME/.openclaw/workspace-main"
        print_info "请确认 OpenClaw 已正确安装"
        exit 1
    fi
    print_success "OpenClaw workspace 存在"

    # 步骤 2：备份现有配置
    print_info "步骤 2/5: 备份现有配置..."
    
    BACKUP_DIR="$HOME/.openclaw/workspace-main/backup-$(date +%Y%m%d-%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    if [ -f "$HOME/.openclaw/workspace-main/HEARTBEAT.md" ]; then
        cp "$HOME/.openclaw/workspace-main/HEARTBEAT.md" "$BACKUP_DIR/"
        print_success "已备份 HEARTBEAT.md"
    fi
    
    if [ -f "$HOME/.openclaw/workspace-main/quality-metrics.json" ]; then
        cp "$HOME/.openclaw/workspace-main/quality-metrics.json" "$BACKUP_DIR/"
        print_success "已备份 quality-metrics.json"
    fi

    # 步骤 3：复制技能文件
    print_info "步骤 3/5: 复制技能文件..."
    
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    SKILLS_SOURCE="$SCRIPT_DIR/skills"
    SKILLS_DEST="$HOME/.openclaw/workspace-main/skills"
    
    if [ ! -d "$SKILLS_SOURCE" ]; then
        print_error "未找到技能目录：$SKILLS_SOURCE"
        print_info "请确保从 3Q-Installation-Pack 目录运行此脚本"
        exit 1
    fi
    
    # 复制 6 个核心技能
    SKILLS=(
        "self-challenge-3q-v3.1"
        "3Q-Plus-v3"
        "quality-os-trigger"
        "task-breakdown-v3"
        "decision-checklist-v2"
        "subagent-brief-template-v3"
    )
    
    for skill in "${SKILLS[@]}"; do
        if [ -d "$SKILLS_SOURCE/$skill" ]; then
            cp -r "$SKILLS_SOURCE/$skill" "$SKILLS_DEST/"
            print_success "已复制：$skill"
        else
            print_error "技能不存在：$skill"
        fi
    done

    # 步骤 4：配置 HEARTBEAT.md
    print_info "步骤 4/5: 配置 HEARTBEAT.md..."
    
    HEARTBEAT_FILE="$HOME/.openclaw/workspace-main/HEARTBEAT.md"
    
    # 检查是否已存在 QualityOS 配置
    if grep -q "QualityOS 统一触发器" "$HEARTBEAT_FILE" 2>/dev/null; then
        print_info "HEARTBEAT.md 已包含 QualityOS 配置，跳过"
    else
        # 追加配置
        cat >> "$HEARTBEAT_FILE" << 'EOF'

---

## 🚀 QualityOS 统一触发器 v4.0（3Q 质量体系）

**触发入口**: `skills/quality-os-trigger/SKILL.md`

**自动触发规则**：
| 场景 | 触发时机 | 自动触发技能 |
|------|---------|-------------|
| 文档保存 | 文件保存时 | quality-prevention(事后 3Q) |
| 代码提交 | git commit 时 | quality-prevention(CODE) |
| 决策开始 | 决策需求创建 | decision-checklist |
| 子代理创建 | 任务下达时 | subagent-brief-template |
| 子代理交付 | 任务完成时 | 3Q 自动验收 |
| 内容发布 | 发布前 | 3Q-Plus-v3（强制检查） |

**质量指标**：
- 自动触发率：≥90%
- 平均评分：≥14/15
- S 级比例：≥50%
- 返工率：≤10%
EOF
        print_success "已配置 HEARTBEAT.md"
    fi

    # 步骤 5：创建质量指标文件
    print_info "步骤 5/5: 创建质量指标追踪文件..."
    
    METRICS_FILE="$HOME/.openclaw/workspace-main/quality-metrics.json"
    
    if [ ! -f "$METRICS_FILE" ]; then
        cat > "$METRICS_FILE" << 'EOF'
{
  "autoTriggerRate": 0.90,
  "avgScore": 14.0,
  "sGradeRatio": 0.50,
  "reworkRate": 0.10,
  "lastUpdate": "2026-03-30",
  "taskDistribution": {
    "mechanical": 0.40,
    "creative": 0.40,
    "decision": 0.10,
    "integration": 0.10
  }
}
EOF
        print_success "已创建 quality-metrics.json"
    else
        print_info "quality-metrics.json 已存在，跳过"
    fi

    # 验证安装
    print_info "验证安装..."
    echo ""
    
    VERIFIED=0
    TOTAL=${#SKILLS[@]}
    
    for skill in "${SKILLS[@]}"; do
        if [ -f "$SKILLS_DEST/$skill/SKILL.md" ]; then
            print_success "$skill"
            ((VERIFIED++))
        else
            print_error "$skill"
        fi
    done
    
    echo ""
    print_header "安装完成！"
    echo ""
    print_success "成功安装 $VERIFIED/$TOTAL 个技能"
    echo ""
    
    if [ $VERIFIED -eq $TOTAL ]; then
        print_success "🎉 3Q 质量体系安装成功！"
        echo ""
        print_info "下一步："
        echo "  1. 阅读 QUICKSTART.md（5 分钟快速上手）"
        echo "  2. 阅读 README.md（完整文档）"
        echo "  3. 尝试第一次 3Q 检查：对任意文档说'3Q 检查 v3.1'"
        echo ""
        print_info "备份目录：$BACKUP_DIR"
    else
        print_error "部分技能安装失败，请检查错误信息"
        exit 1
    fi
}

# 运行主函数
main "$@"
