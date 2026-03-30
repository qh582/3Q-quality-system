# 🚀 快速开始指南

> 5 分钟上手技能质量监控系统

---

## 📦 系统组成

```
skills/quality-dashboard/
├── logger.py              # 核心日志工具
├── dashboard.md           # 质量仪表板
├── generate_dashboard.py  # 仪表板生成器
├── README.md              # 详细文档
├── LOG-FORMAT.md          # 日志格式规范
├── QUICKSTART.md          # 本文件
├── examples/              # 集成示例
│   └── integration_example.py
└── logs/                  # 日志存储目录
    └── skill_calls.jsonl
```

---

## ⚡ 3 步快速集成

### 步骤 1: 导入日志器

在你的技能代码中:

```python
from skills.quality_dashboard.logger import SkillLogger

logger = SkillLogger()
```

### 步骤 2: 记录调用

在技能调用前后:

```python
import time

start = time.time()
try:
    # 执行技能调用
    result = call_your_skill()
    duration_ms = int((time.time() - start) * 1000)
    
    logger.log_call(
        skill_name="your-skill-name",
        status="success",
        duration_ms=duration_ms
    )
except Exception as e:
    duration_ms = int((time.time() - start) * 1000)
    
    logger.log_call(
        skill_name="your-skill-name",
        status="error",
        duration_ms=duration_ms,
        error_msg=str(e)
    )
```

### 步骤 3: 查看仪表板

```bash
cd skills/quality-dashboard

# 查看统计
python3 logger.py stats 24

# 生成仪表板
python3 generate_dashboard.py

# 查看仪表板
cat dashboard.md
```

---

## 🎯 核心功能

### 记录调用

```python
# 成功调用
logger.log_call("feishu-bitable", "success", duration_ms=150)

# 失败调用
logger.log_call("feishu-calendar", "error", error_msg="API timeout")

# 带元数据
logger.log_call(
    "feishu-doc",
    "success",
    duration_ms=200,
    metadata={"action": "create", "user_id": "ou_xxx"}
)
```

### 查询统计

```python
# 获取统计数据
stats = logger.get_stats(hours=24)
print(f"总调用：{stats['total_calls']}")
print(f"成功率：{stats['success_rate']:.1%}")

# 按技能查看
for skill, data in stats["by_skill"].items():
    print(f"{skill}: {data['total']}次，成功率 {data['success_rate']:.1%}")
```

### 检查告警

```python
alerts = logger.check_alerts()
for alert in alerts:
    print(f"[{alert['severity']}] {alert['message']}")
```

### 健康状态

```python
health = logger.get_health_status()
print(f"健康状态：{health['status']}")  # healthy / warning / critical
```

---

## 📊 命令行工具

```bash
# 记录调用
python3 logger.py log feishu-bitable success 150
python3 logger.py log feishu-calendar error 3000 "API timeout"

# 查看统计（过去 24 小时）
python3 logger.py stats 24

# 查看统计（过去 7 天）
python3 logger.py stats 168

# 检查告警
python3 logger.py alerts

# 查看健康状态
python3 logger.py health
```

---

## 🔧 自动化配置

### 定时生成仪表板

编辑 crontab:
```bash
crontab -e
```

添加任务:
```bash
# 每小时生成一次仪表板
0 * * * * cd /home/admin/.openclaw/workspace/skills/quality-dashboard && python3 generate_dashboard.py
```

### 日志轮转

```bash
# 每天凌晨备份并清空日志
0 0 * * * cd /home/admin/.openclaw/workspace/skills/quality-dashboard && \
    mv logs/skill_calls.jsonl logs/skill_calls_$(date +\%Y-\%m-\%d).jsonl && \
    gzip logs/skill_calls_*.jsonl
```

---

## 📖 下一步

- 📚 阅读 `README.md` 了解完整功能
- 📋 查看 `LOG-FORMAT.md` 了解日志格式规范
- 💡 运行 `examples/integration_example.py` 查看集成示例
- 🔧 根据需求定制告警阈值和通知方式

---

## ❓ 常见问题

### Q: 日志文件在哪里？
A: `skills/quality-dashboard/logs/skill_calls.jsonl`

### Q: 如何查看历史数据？
A: 使用 `logger.get_stats(hours=168)` 查看过去 7 天数据

### Q: 如何修改告警阈值？
A: 编辑 `logger.py` 中的 `ALERT_CONFIG` 字典

### Q: 如何集成通知？
A: 参考 `README.md` 中的"通知集成"章节

---

## 🎉 开始监控！

现在你已经掌握了基础知识，开始在你的技能中集成日志记录吧！

```python
from skills.quality_dashboard.logger import SkillLogger

logger = SkillLogger()
# 开始记录...
```

---

**有问题？** 查看 `README.md` 或联系系统维护者。
