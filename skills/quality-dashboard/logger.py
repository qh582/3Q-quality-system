#!/usr/bin/env python3
"""
技能质量日志系统 - Skill Quality Logger

记录技能调用日志，支持查询、统计和告警检测。

用法:
    from logger import SkillLogger
    
    logger = SkillLogger()
    logger.log_call("feishu-bitable", "success", duration_ms=150)
    logger.log_call("feishu-calendar", "error", error_msg="API timeout")
    
    # 查询统计
    stats = logger.get_stats(hours=24)
    alerts = logger.check_alerts()
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Any


class SkillLogger:
    """技能调用日志记录器"""
    
    # 告警阈值配置
    ALERT_CONFIG = {
        "consecutive_failures": 3,  # 连续失败次数触发告警
        "failure_rate_threshold": 0.5,  # 失败率超过 50% 触发告警
        "min_calls_for_rate_check": 5,  # 最少调用次数才检查失败率
    }
    
    def __init__(self, log_dir: Optional[str] = None):
        """
        初始化日志器
        
        Args:
            log_dir: 日志目录，默认为当前脚本下的 logs/ 目录
        """
        if log_dir:
            self.log_dir = Path(log_dir)
        else:
            self.log_dir = Path(__file__).parent / "logs"
        
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "skill_calls.jsonl"
    
    def log_call(
        self,
        skill_name: str,
        status: str,
        duration_ms: Optional[int] = None,
        error_msg: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        记录一次技能调用
        
        Args:
            skill_name: 技能名称（如 "feishu-bitable"）
            status: 结果状态 ("success" | "error" | "timeout")
            duration_ms: 调用耗时（毫秒）
            error_msg: 错误信息（仅失败时）
            metadata: 额外元数据
        
        Returns:
            记录的日志条目
        """
        entry = {
            "timestamp": datetime.now().isoformat(),
            "skill_name": skill_name,
            "status": status,
            "duration_ms": duration_ms,
            "error_msg": error_msg,
            "metadata": metadata or {}
        }
        
        # 追加写入日志文件
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        
        return entry
    
    def get_logs(
        self,
        hours: int = 24,
        skill_name: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        获取指定时间范围内的日志
        
        Args:
            hours: 时间范围（小时），默认 24 小时
            skill_name: 筛选特定技能，None 表示全部
        
        Returns:
            日志条目列表
        """
        cutoff = datetime.now() - timedelta(hours=hours)
        logs = []
        
        if not self.log_file.exists():
            return logs
        
        with open(self.log_file, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    entry_time = datetime.fromisoformat(entry["timestamp"])
                    
                    if entry_time < cutoff:
                        continue
                    
                    if skill_name and entry["skill_name"] != skill_name:
                        continue
                    
                    logs.append(entry)
                except (json.JSONDecodeError, KeyError):
                    continue
        
        return logs
    
    def get_stats(
        self,
        hours: int = 24
    ) -> Dict[str, Any]:
        """
        获取统计数据
        
        Args:
            hours: 时间范围（小时）
        
        Returns:
            统计字典，包含：
            - total_calls: 总调用次数
            - success_count: 成功次数
            - error_count: 失败次数
            - success_rate: 成功率
            - avg_duration_ms: 平均耗时
            - by_skill: 按技能分类的统计
        """
        logs = self.get_logs(hours=hours)
        
        if not logs:
            return {
                "total_calls": 0,
                "success_count": 0,
                "error_count": 0,
                "success_rate": 0.0,
                "avg_duration_ms": 0,
                "by_skill": {}
            }
        
        total = len(logs)
        success = sum(1 for log in logs if log["status"] == "success")
        errors = total - success
        
        durations = [log["duration_ms"] for log in logs if log.get("duration_ms")]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        # 按技能分组统计
        by_skill: Dict[str, Dict[str, Any]] = {}
        for log in logs:
            skill = log["skill_name"]
            if skill not in by_skill:
                by_skill[skill] = {
                    "total": 0,
                    "success": 0,
                    "errors": 0,
                    "consecutive_failures": 0
                }
            
            by_skill[skill]["total"] += 1
            if log["status"] == "success":
                by_skill[skill]["success"] += 1
                by_skill[skill]["consecutive_failures"] = 0
            else:
                by_skill[skill]["errors"] += 1
                by_skill[skill]["consecutive_failures"] += 1
        
        # 计算每个技能的成功率
        for skill in by_skill:
            total_skill = by_skill[skill]["total"]
            by_skill[skill]["success_rate"] = (
                by_skill[skill]["success"] / total_skill if total_skill > 0 else 0
            )
        
        return {
            "total_calls": total,
            "success_count": success,
            "error_count": errors,
            "success_rate": success / total if total > 0 else 0,
            "avg_duration_ms": round(avg_duration, 2),
            "by_skill": by_skill,
            "time_range_hours": hours
        }
    
    def check_alerts(self) -> List[Dict[str, Any]]:
        """
        检查是否需要告警
        
        Returns:
            告警列表，每个告警包含：
            - skill_name: 技能名称
            - alert_type: 告警类型 ("consecutive_failures" | "high_failure_rate")
            - message: 告警消息
            - severity: 严重程度 ("warning" | "critical")
        """
        alerts = []
        logs = self.get_logs(hours=24)
        
        # 按技能分组检查
        skill_logs: Dict[str, List[Dict]] = {}
        for log in logs:
            skill = log["skill_name"]
            if skill not in skill_logs:
                skill_logs[skill] = []
            skill_logs[skill].append(log)
        
        for skill, skill_log_list in skill_logs.items():
            # 按时间排序
            skill_log_list.sort(key=lambda x: x["timestamp"])
            
            # 检查连续失败
            consecutive = 0
            for log in skill_log_list:
                if log["status"] != "success":
                    consecutive += 1
                    if consecutive >= self.ALERT_CONFIG["consecutive_failures"]:
                        alerts.append({
                            "skill_name": skill,
                            "alert_type": "consecutive_failures",
                            "message": f"技能 '{skill}' 连续失败 {consecutive} 次",
                            "severity": "critical" if consecutive >= 5 else "warning"
                        })
                        break
                else:
                    consecutive = 0
            
            # 检查失败率
            total = len(skill_log_list)
            if total >= self.ALERT_CONFIG["min_calls_for_rate_check"]:
                errors = sum(1 for log in skill_log_list if log["status"] != "success")
                failure_rate = errors / total
                
                if failure_rate >= self.ALERT_CONFIG["failure_rate_threshold"]:
                    alerts.append({
                        "skill_name": skill,
                        "alert_type": "high_failure_rate",
                        "message": f"技能 '{skill}' 失败率过高 ({failure_rate:.1%})",
                        "severity": "critical" if failure_rate >= 0.8 else "warning"
                    })
        
        return alerts
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        获取技能健康状态
        
        Returns:
            健康状态字典
        """
        stats = self.get_stats(hours=24)
        alerts = self.check_alerts()
        
        # 计算整体健康度
        success_rate = stats["success_rate"]
        alert_count = len(alerts)
        
        if success_rate >= 0.95 and alert_count == 0:
            health = "healthy"
        elif success_rate >= 0.8 and alert_count <= 2:
            health = "warning"
        else:
            health = "critical"
        
        return {
            "status": health,
            "success_rate": success_rate,
            "total_calls": stats["total_calls"],
            "active_alerts": alert_count,
            "alerts": alerts,
            "skills_monitored": len(stats["by_skill"])
        }


def main():
    """命令行工具入口"""
    import sys
    
    logger = SkillLogger()
    
    if len(sys.argv) < 2:
        print("用法：python logger.py <command> [args]")
        print("命令:")
        print("  log <skill> <status> [duration_ms] [error_msg]  - 记录调用")
        print("  stats [hours]                                    - 查看统计")
        print("  alerts                                           - 检查告警")
        print("  health                                           - 健康状态")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "log":
        if len(sys.argv) < 4:
            print("用法：python logger.py log <skill> <status> [duration_ms] [error_msg]")
            sys.exit(1)
        
        skill = sys.argv[2]
        status = sys.argv[3]
        duration = int(sys.argv[4]) if len(sys.argv) > 4 else None
        error = sys.argv[5] if len(sys.argv) > 5 else None
        
        entry = logger.log_call(skill, status, duration, error)
        print(f"✓ 已记录：{json.dumps(entry, ensure_ascii=False)}")
    
    elif command == "stats":
        hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
        stats = logger.get_stats(hours)
        print(f"\n📊 技能调用统计（过去{hours}小时）")
        print(f"总调用：{stats['total_calls']}")
        print(f"成功：{stats['success_count']} ({stats['success_rate']:.1%})")
        print(f"失败：{stats['error_count']}")
        print(f"平均耗时：{stats['avg_duration_ms']}ms")
        print(f"\n按技能:")
        for skill, data in stats["by_skill"].items():
            print(f"  {skill}: {data['total']}次，成功率 {data['success_rate']:.1%}")
    
    elif command == "alerts":
        alerts = logger.check_alerts()
        if alerts:
            print(f"\n⚠️  发现 {len(alerts)} 个告警:")
            for alert in alerts:
                severity = "🔴" if alert["severity"] == "critical" else "🟡"
                print(f"  {severity} {alert['message']}")
        else:
            print("\n✅ 无告警")
    
    elif command == "health":
        health = logger.get_health_status()
        emoji = {"healthy": "✅", "warning": "⚠️", "critical": "🔴"}
        print(f"\n{emoji.get(health['status'], '❓')} 技能健康状态：{health['status'].upper()}")
        print(f"成功率：{health['success_rate']:.1%}")
        print(f"监控技能数：{health['skills_monitored']}")
        print(f"活跃告警：{health['active_alerts']}")
    
    else:
        print(f"未知命令：{command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
