# 📊 技能质量仪表板系统

> 建立技能质量监控体系，实现技能调用的可视化监控与告警

---

## 📖 目录

- [功能概述](#-功能概述)
- [快速开始](#-快速开始)
- [日志系统](#-日志系统)
- [仪表板](#-仪表板)
- [告警机制](#-告警机制)
- [API 参考](#-api-参考)
- [最佳实践](#-最佳实践)
- [故障排查](#-故障排查)

---

## 🎯 功能概述

### 核心价值

1. **可观测性** - 实时了解所有技能的调用状况
2. **质量监控** - 追踪成功率、耗时等关键指标
3. **主动告警** - 在问题影响用户前发现问题
4. **数据驱动** - 基于历史数据优化技能性能

### 系统架构

```
┌─────────────────────────────────────────────────────────┐
│                    技能调用层                              │
│  (feishu-bitable, feishu-calendar, feishu-doc, ...)     │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    日志记录层                              │
│              (logger.py - SkillLogger 类)                │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    数据存储层                              │
│           (logs/skill_calls.jsonl - JSONL 格式)           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    展示告警层                              │
│     (dashboard.md + 告警检测 + 定时更新脚本)               │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 快速开始

### 1. 安装依赖

本系统使用 Python 标准库，无需额外安装依赖。

```bash
# 验证 Python 环境
python3 --version  # 需要 Python 3.7+
```

### 2. 集成到技能调用

在技能调用代码中集成日志记录:

```python
from skills.quality_dashboard.logger import SkillLogger

# 初始化日志器
logger = SkillLogger()

# 在技能调用前后记录
import time

start_time = time.time()
try:
    # 执行技能调用
    result = call_skill(...)
    duration_ms = int((time.time() - start_time) * 1000)
    
    # 记录成功
    logger.log_call(
        skill_name="feishu-bitable",
        status="success",
        duration_ms=duration_ms
    )
except Exception as e:
    duration_ms = int((time.time() - start_time) * 1000)
    
    # 记录失败
    logger.log_call(
        skill_name="feishu-bitable",
        status="error",
        duration_ms=duration_ms,
        error_msg=str(e)
    )
```

### 3. 查看统计

```bash
cd skills/quality-dashboard

# 查看过去 24 小时统计
python3 logger.py stats 24

# 检查告警
python3 logger.py alerts

# 查看健康状态
python3 logger.py health
```

### 4. 更新仪表板

```bash
# 手动更新（编辑 dashboard.md 填入最新数据）
# 或使用自动更新脚本（待实现）
python3 generate_dashboard.py
```

---

## 📝 日志系统

### 日志格式

采用 JSON Lines 格式，每行一个 JSON 对象:

```json
{"timestamp": "2026-03-18T08:30:00.123456", "skill_name": "feishu-bitable", "status": "success", "duration_ms": 150, "error_msg": null, "metadata": {"action": "create"}}
{"timestamp": "2026-03-18T08:30:05.456789", "skill_name": "feishu-calendar", "status": "error", "duration_ms": 3200, "error_msg": "API timeout", "metadata": {"action": "create_event"}}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| timestamp | string | ✅ | ISO 8601 时间戳 | `"2026-03-18T08:30:00.123456"` |
| skill_name | string | ✅ | 技能名称 | `"feishu-bitable"` |
| status | string | ✅ | 状态：success/error/timeout | `"success"` |
| duration_ms | number | ❌ | 调用耗时（毫秒） | `150` |
| error_msg | string | ❌ | 错误信息 | `"API timeout"` |
| metadata | object | ❌ | 额外元数据 | `{"action": "create"}` |

### 日志管理

#### 日志轮转（建议配置）

```bash
# 添加 crontab 任务，每天备份并清空日志
0 0 * * * cd /home/admin/.openclaw/workspace/skills/quality-dashboard && \
    mv logs/skill_calls.jsonl logs/skill_calls_$(date +\%Y-\%m-\%d).jsonl && \
    gzip logs/skill_calls_*.jsonl
```

#### 日志清理

保留最近 30 天的日志:

```bash
# 删除 30 天前的压缩日志
find logs/ -name "*.jsonl.gz" -mtime +30 -delete
```

---

## 📊 仪表板

### 仪表板位置

`skills/quality-dashboard/dashboard.md`

### 关键指标

| 指标 | 计算方式 | 健康阈值 |
|------|---------|---------|
| 成功率 | 成功次数 / 总调用次数 | ≥ 95% |
| 平均耗时 | 所有调用耗时的平均值 | < 500ms |
| 连续失败 | 最近连续失败次数 | < 3 |
| 失败率 | 失败次数 / 总调用次数 | < 5% |

### 更新频率

- **实时监控**: 告警检测每小时运行
- **仪表板更新**: 建议每小时或每天更新
- **历史归档**: 每天备份日志

### 自定义仪表板

可以创建自定义视图:

```python
from logger import SkillLogger

logger = SkillLogger()

# 获取特定技能的统计
stats = logger.get_stats(hours=24)
bitable_stats = stats["by_skill"].get("feishu-bitable", {})

# 生成自定义报告
print(f"多维表格技能 24 小时调用 {bitable_stats.get('total', 0)} 次")
print(f"成功率：{bitable_stats.get('success_rate', 0):.1%}")
```

---

## 🚨 告警机制

### 告警类型

#### 1. 连续失败告警

| 级别 | 条件 | 响应 |
|------|------|------|
| 警告 (🟡) | 连续失败 ≥ 3 次 | 关注并排查 |
| 严重 (🔴) | 连续失败 ≥ 5 次 | 立即处理 |

#### 2. 高失败率告警

| 级别 | 条件 | 响应 |
|------|------|------|
| 警告 (🟡) | 失败率 ≥ 50% (最少 5 次调用) | 分析原因 |
| 严重 (🔴) | 失败率 ≥ 80% | 紧急修复 |

### 告警检测

```python
from logger import SkillLogger

logger = SkillLogger()
alerts = logger.check_alerts()

for alert in alerts:
    print(f"[{alert['severity'].upper()}] {alert['message']}")
    
    # 这里可以集成通知逻辑
    # send_notification(alert)
```

### 通知集成（待实现）

```python
def send_notification(alert):
    """发送告警通知到飞书群"""
    from feishu_im_user_message import feishu_im_user_message
    
    message = f"""
⚠️ 技能质量告警

技能：{alert['skill_name']}
类型：{alert['alert_type']}
级别：{alert['severity']}
消息：{alert['message']}

请及时处理！
    """
    
    feishu_im_user_message(
        action="send",
        msg_type="text",
        receive_id_type="chat_id",
        receive_id="oc_xxx",  # 替换为实际群 ID
        content=json.dumps({"text": message})
    )
```

---

## 🔧 API 参考

### SkillLogger 类

#### 初始化

```python
logger = SkillLogger(log_dir: Optional[str] = None)
```

- `log_dir`: 日志目录，默认为脚本下的 `logs/` 目录

#### log_call()

记录一次技能调用。

```python
logger.log_call(
    skill_name: str,
    status: str,
    duration_ms: Optional[int] = None,
    error_msg: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]
```

**示例**:
```python
logger.log_call("feishu-bitable", "success", duration_ms=150)
logger.log_call("feishu-calendar", "error", error_msg="API timeout")
```

#### get_logs()

获取日志列表。

```python
logger.get_logs(
    hours: int = 24,
    skill_name: Optional[str] = None
) -> List[Dict[str, Any]]
```

#### get_stats()

获取统计数据。

```python
logger.get_stats(hours: int = 24) -> Dict[str, Any]
```

**返回示例**:
```json
{
  "total_calls": 100,
  "success_count": 95,
  "error_count": 5,
  "success_rate": 0.95,
  "avg_duration_ms": 150.5,
  "by_skill": {
    "feishu-bitable": {
      "total": 50,
      "success": 48,
      "errors": 2,
      "success_rate": 0.96
    }
  }
}
```

#### check_alerts()

检查告警。

```python
logger.check_alerts() -> List[Dict[str, Any]]
```

#### get_health_status()

获取健康状态。

```python
logger.get_health_status() -> Dict[str, Any]
```

**返回示例**:
```json
{
  "status": "healthy",
  "success_rate": 0.95,
  "total_calls": 100,
  "active_alerts": 0,
  "alerts": [],
  "skills_monitored": 5
}
```

---

## 💡 最佳实践

### 1. 日志记录时机

✅ **推荐**:
- 在技能调用完成后立即记录
- 记录准确的耗时（包含网络时间）
- 记录有意义的错误信息

❌ **避免**:
- 只记录成功，不记录失败
- 记录过于简略的错误信息（如只写 "error"）
- 在异步任务中丢失日志上下文

### 2. 错误信息规范

✅ **好的错误信息**:
```
"API timeout after 30000ms"
"Permission denied: user lacks bitable write access"
"Invalid parameter: 'date' should be ISO 8601 format"
```

❌ **差的错误信息**:
```
"error"
"failed"
"something went wrong"
```

### 3. 元数据使用

记录有助于排查问题的上下文信息:

```python
logger.log_call(
    skill_name="feishu-bitable",
    status="error",
    duration_ms=3200,
    error_msg="Record limit exceeded",
    metadata={
        "action": "batch_create",
        "record_count": 600,
        "table_id": "tbl_xxx",
        "user_id": "ou_xxx"
    }
)
```

### 4. 性能优化

- 日志写入是追加模式，性能较好
- 大批量调用时，可考虑批量写入（每 100 条 flush 一次）
- 避免在日志中包含敏感信息（如 token、密码）

---

## 🐛 故障排查

### 问题 1: 日志文件不存在

**现象**: 运行 `logger.py stats` 显示无数据

**解决**:
```bash
# 检查日志目录
ls -la logs/

# 如果没有 logs 目录，创建它
mkdir -p logs

# 检查是否有写入权限
touch logs/test.txt && rm logs/test.txt
```

### 问题 2: 日志格式错误

**现象**: 部分日志未被统计

**解决**:
```bash
# 检查日志格式
head -5 logs/skill_calls.jsonl

# 验证 JSON 格式
python3 -c "import json; [json.loads(line) for line in open('logs/skill_calls.jsonl')]"
```

### 问题 3: 告警未触发

**现象**: 技能明显有问题但未收到告警

**解决**:
```python
# 手动检查告警逻辑
from logger import SkillLogger
logger = SkillLogger()

# 查看原始日志
logs = logger.get_logs(hours=24)
print(f"总日志数：{len(logs)}")

# 查看失败日志
failures = [log for log in logs if log['status'] != 'success']
print(f"失败数：{len(failures)}")

# 手动触发告警检测
alerts = logger.check_alerts()
print(f"告警数：{len(alerts)}")
```

### 问题 4: 仪表板数据不更新

**现象**: dashboard.md 数据过时

**解决**:
- 手动更新：编辑 dashboard.md 填入最新统计数据
- 自动更新：配置定时任务运行 `generate_dashboard.py`（待实现）

---

## 📈 演进计划

### v1.0 (当前版本)
- ✅ 基础日志记录
- ✅ 统计查询
- ✅ 告警检测
- ✅ 仪表板模板

### v1.1 (计划中)
- [ ] 自动生成仪表板脚本
- [ ] 飞书通知集成
- [ ] 日志轮转自动化
- [ ] Web 可视化界面

### v2.0 (未来)
- [ ] 实时告警推送
- [ ] 趋势分析与预测
- [ ] 技能性能对比
- [ ] 自动化根因分析

---

## 📄 许可证

本系统为内部工具，遵循公司代码管理规范。

---

## 🤝 贡献指南

欢迎提交改进建议！

1. Fork 项目
2. 创建特性分支
3. 提交变更
4. 推送到分支
5. 创建 Pull Request

---

**维护者**: 技能质量监控系统  
**版本**: v1.0  
**创建日期**: 2026-03-18  
**最后更新**: 2026-03-18
