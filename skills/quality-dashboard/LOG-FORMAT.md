# 📋 日志格式规范

> 技能质量日志系统的标准化格式定义

---

## 📁 文件结构

```
skills/quality-dashboard/
├── logs/
│   ├── skill_calls.jsonl          # 主日志文件
│   ├── skill_calls_2026-03-18.jsonl.gz  # 归档日志（可选）
│   └── .gitkeep                   # 保持目录存在
├── logger.py                      # 日志工具
├── dashboard.md                   # 仪表板
├── README.md                      # 使用文档
└── LOG-FORMAT.md                  # 本文件
```

---

## 📝 日志格式

### 基础格式

**格式类型**: JSON Lines (JSONL)  
**文件编码**: UTF-8  
**行结束符**: LF (`\n`)  
**文件扩展名**: `.jsonl`

### 单条日志结构

```json
{
  "timestamp": "2026-03-18T08:30:00.123456",
  "skill_name": "feishu-bitable",
  "status": "success",
  "duration_ms": 150,
  "error_msg": null,
  "metadata": {}
}
```

---

## 🔍 字段定义

### 必填字段

#### timestamp

- **类型**: string
- **格式**: ISO 8601 with microseconds
- **示例**: `"2026-03-18T08:30:00.123456"`
- **说明**: 技能调用完成的时间点
- **时区**: 本地时间（Asia/Shanghai）

```python
from datetime import datetime
timestamp = datetime.now().isoformat()
```

#### skill_name

- **类型**: string
- **格式**: kebab-case
- **示例**: `"feishu-bitable"`, `"feishu-calendar"`
- **说明**: 技能的唯一标识符
- **命名规范**: 
  - 使用小写字母
  - 单词间用连字符分隔
  - 以 `feishu-` 为前缀（飞书技能）

#### status

- **类型**: string
- **枚举值**: `success`, `error`, `timeout`
- **说明**: 技能调用的最终状态

| 状态值 | 说明 | 使用场景 |
|--------|------|----------|
| `success` | 调用成功 | API 返回 2xx，业务逻辑执行完成 |
| `error` | 调用失败 | API 返回 4xx/5xx，参数错误，权限不足 |
| `timeout` | 调用超时 | 超过设定阈值（默认 30 秒）未响应 |

### 可选字段

#### duration_ms

- **类型**: number (integer)
- **单位**: 毫秒 (ms)
- **示例**: `150`, `3200`
- **说明**: 技能调用耗时
- **精度**: 整数毫秒
- **建议**: 所有技能调用都应记录耗时

```python
import time

start = time.time()
try:
    result = call_skill()
    duration_ms = int((time.time() - start) * 1000)
except Exception:
    duration_ms = int((time.time() - start) * 1000)
```

#### error_msg

- **类型**: string 或 null
- **最大长度**: 1000 字符
- **示例**: `"API timeout after 30000ms"`
- **说明**: 错误描述信息
- **使用规范**:
  - 仅在 `status` 为 `error` 或 `timeout` 时填写
  - `success` 时应为 `null` 或省略
  - 避免包含敏感信息（token、密码等）

**好的错误信息示例**:
```
"API timeout after 30000ms"
"Permission denied: user lacks bitable write access"
"Invalid parameter: 'date' should be ISO 8601 format, got '2026/03/18'"
"Rate limit exceeded: 100 requests/minute, retry after 60s"
"Record not found: table_id='tbl_xxx', record_id='rec_yyy'"
```

**差的错误信息示例**:
```
"error"                          # 过于简略
"failed"                         # 无意义
"something went wrong"           # 无帮助
"Error: Exception"               # 未提取具体信息
```

#### metadata

- **类型**: object (JSON 对象)
- **说明**: 额外的上下文信息
- **建议字段**:

| 字段名 | 类型 | 说明 | 示例 |
|--------|------|------|------|
| `action` | string | 具体操作类型 | `"create"`, `"read"`, `"update"`, `"delete"` |
| `user_id` | string | 调用用户的 open_id | `"ou_xxx"` |
| `table_id` | string | 操作的数据表 ID | `"tbl_xxx"` |
| `record_count` | number | 批量操作的记录数 | `50` |
| `retry_count` | number | 重试次数 | `2` |
| `api_endpoint` | string | 调用的 API 端点 | `"/bitable/v1/apps"` |

**metadata 示例**:
```json
{
  "action": "batch_create",
  "user_id": "ou_xxx",
  "table_id": "tbl_xxx",
  "record_count": 50,
  "retry_count": 0
}
```

---

## 📊 日志示例

### 成功调用

```json
{"timestamp": "2026-03-18T08:30:00.123456", "skill_name": "feishu-bitable", "status": "success", "duration_ms": 150, "error_msg": null, "metadata": {"action": "create", "table_id": "tbl_xxx"}}
```

### 失败调用（参数错误）

```json
{"timestamp": "2026-03-18T08:30:05.456789", "skill_name": "feishu-calendar", "status": "error", "duration_ms": 50, "error_msg": "Invalid parameter: 'start_time' is required", "metadata": {"action": "create_event", "user_id": "ou_xxx"}}
```

### 失败调用（API 错误）

```json
{"timestamp": "2026-03-18T08:30:10.789012", "skill_name": "feishu-doc", "status": "error", "duration_ms": 320, "error_msg": "API returned 403: Permission denied", "metadata": {"action": "update", "doc_id": "doc_xxx"}}
```

### 超时调用

```json
{"timestamp": "2026-03-18T08:30:40.012345", "skill_name": "feishu-sheet", "status": "timeout", "duration_ms": 30000, "error_msg": "API timeout after 30000ms", "metadata": {"action": "export", "retry_count": 2}}
```

---

## 🔧 写入规范

### 原子写入

日志写入应保证原子性，避免并发写入导致数据损坏：

```python
import fcntl

def append_log(entry: dict, log_file: Path):
    line = json.dumps(entry, ensure_ascii=False) + "\n"
    
    with open(log_file, "a", encoding="utf-8") as f:
        # 获取文件锁（防止并发写入）
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            f.write(line)
            f.flush()  # 确保写入磁盘
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
```

### 批量写入优化

高频调用场景下，可考虑批量写入：

```python
class BatchLogger:
    def __init__(self, batch_size=100):
        self.buffer = []
        self.batch_size = batch_size
    
    def log(self, entry):
        self.buffer.append(entry)
        if len(self.buffer) >= self.batch_size:
            self.flush()
    
    def flush(self):
        if self.buffer:
            with open("logs/skill_calls.jsonl", "a") as f:
                for entry in self.buffer:
                    f.write(json.dumps(entry) + "\n")
            self.buffer = []
```

---

## 🗂️ 日志管理

### 日志轮转

建议每天轮转一次日志文件：

```bash
#!/bin/bash
# rotate_logs.sh

LOG_DIR="logs"
DATE=$(date +%Y-%m-%d)

# 移动当前日志到归档文件
mv "$LOG_DIR/skill_calls.jsonl" "$LOG_DIR/skill_calls_$DATE.jsonl"

# 压缩归档文件
gzip "$LOG_DIR/skill_calls_$DATE.jsonl"

# 创建新的空日志文件
touch "$LOG_DIR/skill_calls.jsonl"

echo "[$(date)] Log rotated successfully"
```

### 日志清理

保留最近 30 天的日志：

```bash
#!/bin/bash
# cleanup_logs.sh

LOG_DIR="logs"
RETENTION_DAYS=30

# 删除超过保留期的归档日志
find "$LOG_DIR" -name "*.jsonl.gz" -mtime +$RETENTION_DAYS -delete

echo "[$(date)] Cleaned up logs older than $RETENTION_DAYS days"
```

### Crontab 配置

```bash
# 每天凌晨 0 点轮转日志
0 0 * * * /home/admin/.openclaw/workspace/skills/quality-dashboard/rotate_logs.sh

# 每周日凌晨 1 点清理旧日志
0 1 * * 0 /home/admin/.openclaw/workspace/skills/quality-dashboard/cleanup_logs.sh
```

---

## 🔒 安全规范

### 敏感信息处理

**禁止记录**:
- ❌ API Token / Access Token
- ❌ 用户密码
- ❌ 完整手机号
- ❌ 身份证号
- ❌ 银行卡号

**脱敏示例**:
```python
def mask_phone(phone: str) -> str:
    """手机号脱敏：13812345678 → 138****5678"""
    if len(phone) == 11:
        return phone[:3] + "****" + phone[-4:]
    return "***"

def mask_token(token: str) -> str:
    """Token 脱敏：只保留前 8 位和后 4 位"""
    if len(token) > 12:
        return token[:8] + "..." + token[-4:]
    return "***"
```

### 日志访问控制

- 日志文件权限：`600`（仅所有者可读写）
- 日志目录权限：`700`（仅所有者可访问）

```bash
chmod 700 logs/
chmod 600 logs/*.jsonl
```

---

## 📈 统计分析

### 查询示例

#### 查询某技能的调用次数

```bash
grep '"skill_name": "feishu-bitable"' logs/skill_calls.jsonl | wc -l
```

#### 查询失败日志

```bash
grep '"status": "error"' logs/skill_calls.jsonl | head -10
```

#### 使用 Python 分析

```python
import json
from collections import Counter

with open("logs/skill_calls.jsonl") as f:
    logs = [json.loads(line) for line in f]

# 按技能统计
skill_counts = Counter(log["skill_name"] for log in logs)
print(skill_counts)

# 按状态统计
status_counts = Counter(log["status"] for log in logs)
print(status_counts)

# 计算成功率
success_rate = status_counts["success"] / sum(status_counts.values())
print(f"成功率：{success_rate:.1%}")
```

---

## 📋 检查清单

在集成日志系统前，请确认：

- [ ] 日志目录已创建 (`logs/`)
- [ ] 日志文件权限正确 (`600`)
- [ ] 所有技能调用都记录日志
- [ ] 错误信息具体且有用
- [ ] 不包含敏感信息
- [ ] 记录了调用耗时
- [ ] 添加了有意义的 metadata
- [ ] 配置了日志轮转
- [ ] 配置了日志清理
- [ ] 测试了日志查询功能

---

**版本**: v1.0  
**创建日期**: 2026-03-18  
**维护者**: 技能质量监控系统
