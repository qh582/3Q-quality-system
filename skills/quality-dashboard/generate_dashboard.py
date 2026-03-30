#!/usr/bin/env python3
"""
仪表板自动生成脚本

从日志文件读取数据，自动生成并更新 dashboard.md

用法:
    python3 generate_dashboard.py [--hours 24] [--output dashboard.md]
"""

import argparse
import json
from datetime import datetime
from pathlib import Path
from logger import SkillLogger


def generate_dashboard(hours: int = 24, output_file: str = "dashboard.md"):
    """生成仪表板 Markdown 文件"""
    
    logger = SkillLogger()
    stats = logger.get_stats(hours=hours)
    alerts = logger.check_alerts()
    health = logger.get_health_status()
    
    # 获取按小时分布的统计数据
    logs = logger.get_logs(hours=hours)
    hourly_stats = get_hourly_stats(logs)
    
    # 获取最近失败记录
    recent_failures = get_recent_failures(logs, limit=5)
    
    # 生成健康状态 emoji
    health_emoji = {
        "healthy": "🟢",
        "warning": "🟡",
        "critical": "🔴"
    }.get(health["status"], "⚪")
    
    # 生成技能表格行
    skill_rows = []
    for skill_name, skill_data in sorted(stats["by_skill"].items()):
        success_rate = skill_data.get("success_rate", 0)
        if success_rate >= 0.95:
            status_emoji = "🟢"
        elif success_rate >= 0.8:
            status_emoji = "🟡"
        else:
            status_emoji = "🔴"
        
        row = (
            f"| {skill_name} | {skill_data['total']} | "
            f"{skill_data['success']} | {skill_data['errors']} | "
            f"{success_rate:.1%} | {status_emoji} |"
        )
        skill_rows.append(row)
    
    # 如果没有技能数据，显示提示
    if not skill_rows:
        skill_rows = ["| -- | -- | -- | -- | -- | -- |"]
    
    # 生成告警表格行
    alert_rows = []
    for alert in alerts:
        severity_emoji = "🔴" if alert["severity"] == "critical" else "🟡"
        row = (
            f"| -- | {alert['skill_name']} | {alert['alert_type']} | "
            f"{severity_emoji} | {alert['message']} |"
        )
        alert_rows.append(row)
    
    if not alert_rows:
        alert_rows = ["| -- | -- | -- | -- | 无活跃告警 |"]
    
    # 生成失败记录表格行
    failure_rows = []
    for failure in recent_failures:
        error_msg = failure.get("error_msg", "未知错误")[:50]
        row = f"| {failure['timestamp'][:19]} | {failure['skill_name']} | {error_msg} |"
        failure_rows.append(row)
    
    if not failure_rows:
        failure_rows = ["| -- | -- | -- |"]
    
    # 生成小时段统计行
    time_slots = [
        ("00:00-06:00", 0, 6),
        ("06:00-12:00", 6, 12),
        ("12:00-18:00", 12, 18),
        ("18:00-24:00", 18, 24)
    ]
    
    time_rows = []
    for slot_name, start_hour, end_hour in time_slots:
        slot_data = hourly_stats.get((start_hour, end_hour), {
            "total": 0, "success": 0, "errors": 0, "success_rate": 0
        })
        row = (
            f"| {slot_name} | {slot_data['total']} | {slot_data['success']} | "
            f"{slot_data['errors']} | {slot_data['success_rate']:.1%} |"
        )
        time_rows.append(row)
    
    # 生成 Markdown 内容
    markdown = f"""# 📊 技能质量仪表板

**最后更新**: {datetime.now().strftime("%Y-%m-%d %H:%M")}  
**统计周期**: 过去 {hours} 小时  
**数据源**: `logs/skill_calls.jsonl`

---

## 🎯 整体健康状态

| 指标 | 数值 | 状态 |
|------|------|------|
| 整体健康度 | {health['status'].upper()} | {health_emoji} |
| 总调用次数 | {stats['total_calls']} | - |
| 成功率 | {stats['success_rate']:.1%} | {'🟢' if stats['success_rate'] >= 0.95 else '🟡' if stats['success_rate'] >= 0.8 else '🔴'} |
| 平均耗时 | {stats['avg_duration_ms']}ms | - |
| 活跃告警 | {health['active_alerts']} | {'✅' if health['active_alerts'] == 0 else '⚠️'} |

---

## 📈 调用趋势

| 时间段 | 调用次数 | 成功 | 失败 | 成功率 |
|--------|---------|------|------|--------|
{chr(10).join(time_rows)}

---

## 🔧 技能详情

| 技能名称 | 调用次数 | 成功 | 失败 | 成功率 | 状态 |
|----------|---------|------|------|--------|------|
{chr(10).join(skill_rows)}

**状态说明**:
- 🟢 健康：成功率 ≥ 95%
- 🟡 警告：成功率 80%-95%
- 🔴 异常：成功率 < 80%

---

## ⚠️ 活跃告警

| 时间 | 技能 | 告警类型 | 严重性 | 消息 |
|------|------|----------|--------|------|
{chr(10).join(alert_rows)}

**告警级别**:
- 🔴 严重：连续失败 ≥ 5 次 或 失败率 ≥ 80%
- 🟡 警告：连续失败 ≥ 3 次 或 失败率 ≥ 50%

---

## 📋 最近失败记录

| 时间 | 技能 | 错误信息 |
|------|------|----------|
{chr(10).join(failure_rows)}

---

## 🔄 更新说明

### 手动更新

```bash
cd skills/quality-dashboard
python3 generate_dashboard.py --hours 24
```

### 自动更新（推荐）

添加定时任务（crontab）:
```bash
# 每小时更新一次仪表板
0 * * * * cd /home/admin/.openclaw/workspace/skills/quality-dashboard && python3 generate_dashboard.py
```

---

## 📝 日志格式规范

详见 `LOG-FORMAT.md`

---

## 🚨 告警机制

详见 `README.md` - 告警机制章节

---

## 📊 质量目标

| 指标 | 目标值 | 当前值 | 达成 |
|------|--------|--------|------|
| 整体成功率 | ≥ 95% | {stats['success_rate']:.1%} | {'✅' if stats['success_rate'] >= 0.95 else '⏳'} |
| P95 耗时 | < 500ms | -- | ⏳ |
| 严重告警 | 0 | {sum(1 for a in alerts if a['severity'] == 'critical')} | {'✅' if sum(1 for a in alerts if a['severity'] == 'critical') == 0 else '⏳'} |
| 日志覆盖率 | 100% | -- | ⏳ |

---

## 📖 使用文档

详细使用说明请参考 `README.md`

---

**维护者**: 技能质量监控系统  
**版本**: v1.0  
**创建日期**: 2026-03-18  
**自动生成**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
"""
    
    # 写入文件
    output_path = Path(output_file)
    output_path.write_text(markdown, encoding="utf-8")
    
    print(f"✅ 仪表板已生成：{output_path}")
    print(f"📊 统计周期：{hours} 小时")
    print(f"📈 总调用：{stats['total_calls']}")
    print(f"✅ 成功率：{stats['success_rate']:.1%}")
    print(f"⚠️  告警数：{len(alerts)}")


def get_hourly_stats(logs: list) -> dict:
    """按小时段统计"""
    time_slots = [
        (0, 6),
        (6, 12),
        (12, 18),
        (18, 24)
    ]
    
    stats = {}
    for start_hour, end_hour in time_slots:
        slot_logs = []
        for log in logs:
            try:
                log_time = datetime.fromisoformat(log["timestamp"])
                if start_hour <= log_time.hour < end_hour:
                    slot_logs.append(log)
            except (ValueError, KeyError):
                continue
        
        total = len(slot_logs)
        success = sum(1 for log in slot_logs if log.get("status") == "success")
        errors = total - success
        
        stats[(start_hour, end_hour)] = {
            "total": total,
            "success": success,
            "errors": errors,
            "success_rate": success / total if total > 0 else 0
        }
    
    return stats


def get_recent_failures(logs: list, limit: int = 5) -> list:
    """获取最近的失败记录"""
    failures = [log for log in logs if log.get("status") != "success"]
    
    # 按时间倒序排序
    failures.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    return failures[:limit]


def main():
    parser = argparse.ArgumentParser(description="生成技能质量仪表板")
    parser.add_argument(
        "--hours",
        type=int,
        default=24,
        help="统计周期（小时），默认 24"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="dashboard.md",
        help="输出文件路径，默认 dashboard.md"
    )
    
    args = parser.parse_args()
    
    generate_dashboard(hours=args.hours, output_file=args.output)


if __name__ == "__main__":
    main()
