#!/usr/bin/env python3
"""
技能日志集成示例

展示如何在技能调用中集成日志记录功能。
"""

import time
import sys
from pathlib import Path

# 添加父目录到路径，以便导入 logger
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import SkillLogger


def example_basic_usage():
    """基础用法示例"""
    print("=" * 60)
    print("示例 1: 基础用法")
    print("=" * 60)
    
    logger = SkillLogger()
    
    # 模拟技能调用
    start = time.time()
    try:
        # 这里替换为实际的技能调用
        # result = call_feishu_api(...)
        time.sleep(0.15)  # 模拟耗时
        duration_ms = int((time.time() - start) * 1000)
        
        logger.log_call(
            skill_name="feishu-bitable",
            status="success",
            duration_ms=duration_ms,
            metadata={"action": "create"}
        )
        print(f"✓ 成功记录调用（耗时 {duration_ms}ms）")
        
    except Exception as e:
        duration_ms = int((time.time() - start) * 1000)
        logger.log_call(
            skill_name="feishu-bitable",
            status="error",
            duration_ms=duration_ms,
            error_msg=str(e)
        )
        print(f"✗ 记录失败调用：{e}")


def example_with_retry():
    """带重试的用法示例"""
    print("\n" + "=" * 60)
    print("示例 2: 带重试的调用")
    print("=" * 60)
    
    logger = SkillLogger()
    max_retries = 3
    retry_count = 0
    
    start = time.time()
    success = False
    
    while retry_count < max_retries and not success:
        try:
            # 模拟技能调用
            # result = call_feishu_api(...)
            time.sleep(0.1)
            
            # 模拟第一次调用失败，第二次成功
            if retry_count == 0:
                raise Exception("Network error")
            
            success = True
            duration_ms = int((time.time() - start) * 1000)
            
            logger.log_call(
                skill_name="feishu-calendar",
                status="success",
                duration_ms=duration_ms,
                metadata={
                    "action": "create_event",
                    "retry_count": retry_count
                }
            )
            print(f"✓ 调用成功（重试 {retry_count} 次，耗时 {duration_ms}ms）")
            
        except Exception as e:
            retry_count += 1
            if retry_count >= max_retries:
                duration_ms = int((time.time() - start) * 1000)
                logger.log_call(
                    skill_name="feishu-calendar",
                    status="error",
                    duration_ms=duration_ms,
                    error_msg=str(e),
                    metadata={"retry_count": retry_count}
                )
                print(f"✗ 调用失败（重试 {retry_count} 次）：{e}")


def example_batch_operations():
    """批量操作示例"""
    print("\n" + "=" * 60)
    print("示例 3: 批量操作")
    print("=" * 60)
    
    logger = SkillLogger()
    
    # 模拟批量创建记录
    start = time.time()
    total_records = 50
    success_count = 0
    error_count = 0
    
    for i in range(total_records):
        try:
            # 模拟创建记录
            # create_record(data[i])
            time.sleep(0.01)
            success_count += 1
        except Exception:
            error_count += 1
    
    duration_ms = int((time.time() - start) * 1000)
    
    # 记录批量操作结果
    if error_count == 0:
        logger.log_call(
            skill_name="feishu-bitable",
            status="success",
            duration_ms=duration_ms,
            metadata={
                "action": "batch_create",
                "record_count": total_records,
                "success_count": success_count,
                "error_count": error_count
            }
        )
        print(f"✓ 批量操作成功（{total_records}条记录，耗时 {duration_ms}ms）")
    else:
        logger.log_call(
            skill_name="feishu-bitable",
            status="error",
            duration_ms=duration_ms,
            error_msg=f"{error_count} records failed",
            metadata={
                "action": "batch_create",
                "record_count": total_records,
                "success_count": success_count,
                "error_count": error_count
            }
        )
        print(f"✗ 批量操作部分失败（成功 {success_count}/{total_records}）")


def example_context_manager():
    """使用上下文管理器"""
    print("\n" + "=" * 60)
    print("示例 4: 上下文管理器模式")
    print("=" * 60)
    
    from contextlib import contextmanager
    
    @contextmanager
    def log_skill_call(skill_name: str, metadata: dict = None):
        """技能调用日志上下文管理器"""
        logger = SkillLogger()
        start = time.time()
        
        try:
            yield
            duration_ms = int((time.time() - start) * 1000)
            logger.log_call(
                skill_name=skill_name,
                status="success",
                duration_ms=duration_ms,
                metadata=metadata
            )
        except Exception as e:
            duration_ms = int((time.time() - start) * 1000)
            logger.log_call(
                skill_name=skill_name,
                status="error",
                duration_ms=duration_ms,
                error_msg=str(e),
                metadata=metadata
            )
            raise
    
    # 使用示例
    try:
        with log_skill_call("feishu-doc", {"action": "update"}):
            # 模拟文档更新
            time.sleep(0.18)
            # update_doc(...)
        print("✓ 文档更新成功")
    except Exception as e:
        print(f"✗ 文档更新失败：{e}")


def example_query_stats():
    """查询统计示例"""
    print("\n" + "=" * 60)
    print("示例 5: 查询统计")
    print("=" * 60)
    
    logger = SkillLogger()
    
    # 获取统计数据
    stats = logger.get_stats(hours=24)
    
    print(f"\n📊 过去 24 小时统计:")
    print(f"  总调用：{stats['total_calls']}")
    print(f"  成功：{stats['success_count']} ({stats['success_rate']:.1%})")
    print(f"  失败：{stats['error_count']}")
    print(f"  平均耗时：{stats['avg_duration_ms']}ms")
    
    print(f"\n🔧 按技能统计:")
    for skill_name, skill_stats in stats["by_skill"].items():
        print(f"  {skill_name}:")
        print(f"    调用：{skill_stats['total']}")
        print(f"    成功率：{skill_stats['success_rate']:.1%}")
    
    # 检查告警
    alerts = logger.check_alerts()
    if alerts:
        print(f"\n⚠️  发现 {len(alerts)} 个告警:")
        for alert in alerts:
            print(f"  [{alert['severity']}] {alert['message']}")
    else:
        print(f"\n✅ 无告警")
    
    # 获取健康状态
    health = logger.get_health_status()
    print(f"\n💚 健康状态：{health['status'].upper()}")


def main():
    """运行所有示例"""
    print("\n" + "=" * 60)
    print("技能日志集成示例")
    print("=" * 60)
    
    example_basic_usage()
    example_with_retry()
    example_batch_operations()
    example_context_manager()
    example_query_stats()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)
    print("\n查看日志文件：logs/skill_calls.jsonl")
    print("查看统计：python3 logger.py stats 24")
    print("查看告警：python3 logger.py alerts")
    print("查看健康：python3 logger.py health")


if __name__ == "__main__":
    main()
