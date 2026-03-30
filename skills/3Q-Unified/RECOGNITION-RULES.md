# 3Q-Unified 识别规则配置

**版本**: v1.0.0  
**创建日期**: 2026-03-28  
**用途**: 智能识别引擎的规则配置

---

## 📋 识别规则

### 规则 1：日常笔记（3Q-Lite）

```yaml
rule_id: daily_note_001
name: 日常笔记识别
framework: 3Q-Lite
priority: 1

# 关键词匹配
keywords:
  include:
    - "笔记"
    - "纪要"
    - "日志"
    - "日记"
    - "记录"
  exclude:
    - "PRD"
    - "方案"
    - "技能"

# 文档类型
doc_types:
  - "note"
  - "meeting_minutes"
  - "log"

# 内容特征
content_features:
  min_word_count: 0
  max_word_count: 2000
  has_action_items: false

# 重要性评分
importance:
  base_score: 10
  word_count_bonus: 10  # >500 字 +10 分
  keyword_bonus: 0

# 阈值
threshold:
  min_score: 0
  max_score: 40
```

---

### 规则 2：重要文档（3Q-Pro）

```yaml
rule_id: important_doc_001
name: 重要文档识别
framework: 3Q-Pro
priority: 2

# 关键词匹配
keywords:
  include:
    - "PRD"
    - "方案"
    - "技能"
    - "SKILL"
    - "需求"
    - "设计"
  exclude: []

# 文档类型
doc_types:
  - "prd"
  - "proposal"
  - "skill_doc"
  - "design_doc"

# 内容特征
content_features:
  min_word_count: 1000
  max_word_count: null
  has_action_items: true

# 重要性评分
importance:
  base_score: 30
  word_count_bonus: 20  # >2000 字 +20 分
  keyword_bonus: 20     # 包含关键词 +20 分

# 阈值
threshold:
  min_score: 40
  max_score: 70
```

---

### 规则 3：里程碑（3Q-Max）

```yaml
rule_id: milestone_001
name: 里程碑识别
framework: 3Q-Max
priority: 3  # 最高优先级

# 关键词匹配
keywords:
  include:
    - "里程碑"
    - "发布"
    - "验收"
    - "交付"
    - "上线"
    - "结项"
  exclude: []

# 文档类型
doc_types:
  - "milestone"
  - "release"
  - "acceptance"
  - "delivery"

# 内容特征
content_features:
  min_word_count: 2000
  max_word_count: null
  has_action_items: true
  has_timeline: true

# 重要性评分
importance:
  base_score: 70
  word_count_bonus: 10
  keyword_bonus: 20

# 阈值
threshold:
  min_score: 70
  max_score: 100
```

---

## 🎯 重要性评分算法

```python
def calculate_importance(doc):
    """
    计算文档重要性评分（0-100 分）
    
    参数:
        doc: 文档对象（包含 type, word_count, keywords 等属性）
    
    返回:
        score: 重要性评分（0-100）
    """
    score = 0
    
    # 1. 文档类型权重（0-40 分）
    type_weights = {
        "milestone": 40,
        "release": 40,
        "prd": 35,
        "skill_doc": 35,
        "proposal": 30,
        "design_doc": 30,
        "note": 10,
        "meeting_minutes": 10,
        "log": 10
    }
    score += type_weights.get(doc.type, 10)
    
    # 2. 内容深度评分（0-30 分）
    if doc.word_count > 5000:
        score += 30
    elif doc.word_count > 2000:
        score += 20
    elif doc.word_count > 500:
        score += 10
    
    # 3. 关键词评分（0-30 分）
    high_priority_keywords = ["发布", "验收", "交付", "上线"]
    medium_priority_keywords = ["方案", "决策", "评审"]
    
    for keyword in high_priority_keywords:
        if keyword in doc.keywords:
            score += 30
            break
    
    for keyword in medium_priority_keywords:
        if keyword in doc.keywords:
            score += 20
            break
    
    return min(score, 100)  # 上限 100 分
```

---

## 📊 框架匹配规则

```python
def match_framework(importance_score, doc_type):
    """
    根据重要性评分匹配检查框架
    
    参数:
        importance_score: 重要性评分（0-100）
        doc_type: 文档类型
    
    返回:
        framework: 匹配的框架名称（3Q-Lite/3Q-Pro/3Q-Max）
    """
    # 里程碑场景强制使用 Max
    if doc_type in ["milestone", "release", "acceptance", "delivery"]:
        return "3Q-Max"
    
    # 根据重要性评分匹配
    if importance_score >= 70:
        return "3Q-Pro"  # 重要文档
    elif importance_score >= 40:
        return "3Q-Lite"  # 中等文档
    else:
        return "3Q-Lite"  # 日常文档
```

---

## 🔧 配置选项

```yaml
# 3Q-Unified 全局配置
3Q-Unified:
  # 智能识别
  auto_detect:
    enabled: true  # 默认开启自动识别
    confidence_threshold: 0.7  # 置信度阈值（>70% 才自动匹配）
  
  # 用户交互
  interaction:
    show_recommendation: true  # 显示推荐框架
    allow_override: true  # 允许用户手动覆盖
    confirm_before_start: true  # 开始前确认
  
  # 性能
  performance:
    max_response_time: 1.0  # 最大响应时间（秒）
    cache_enabled: true  # 开启缓存
  
  # 日志
  logging:
    enabled: true
    level: "INFO"
    log_matches: true  # 记录匹配结果
```

---

## 📈 监控指标

```yaml
# 识别准确率监控
metrics:
  accuracy:
    target: 0.90  # 目标准确率 90%
    current: null  # 待测试
    
  response_time:
    target: 1.0  # 目标响应时间<1 秒
    current: null
    
  user_satisfaction:
    target: 4.5  # 目标满意度 4.5/5
    current: null
    
  framework_distribution:
    3Q-Lite: null  # Lite 使用比例
    3Q-Pro: null   # Pro 使用比例
    3Q-Max: null   # Max 使用比例
```

---

**维护者**: 小 O 🤖  
**最后更新**: 2026-03-28  
**下次审查**: 2026-04-04
