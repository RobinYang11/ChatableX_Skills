---
name: daily-news-briefing
description: 搜索今日行业新闻，整理成结构化简报并发送到指定邮箱
version: 1.0.0
author: ChatableX
category: productivity
tool_ids:
  - google-search
  - email-sender
variables:
  - name: topic
    type: string
    required: true
    description: 搜索主题（如"人工智能"、"新能源汽车"、"半导体"）
  - name: email
    type: string
    required: true
    description: 接收简报的邮箱地址
  - name: count
    type: number
    required: false
    default: 10
    description: 抓取的新闻条数
---

# 今日行业新闻简报

## 什么时候使用这个技能
当用户需要快速了解某个行业的最新动态，并希望整理成简报发送到邮箱时使用。
典型场景：
- "帮我搜一下今天AI行业的新闻，整理后发到我邮箱"
- "每日新能源简报"
- "半导体行业最新消息汇总"

## 执行步骤
1. 使用 google-search 工具搜索「{{topic}} 最新新闻」，获取最近 24 小时内的相关报道
2. 从搜索结果中筛选 Top {{count}} 最相关、最有价值的新闻
3. 对每条新闻提取：标题、一句话摘要（不超过 50 字）、原文链接
4. 使用 references/news-format-guide.md 中的格式模板整理简报
5. 在简报末尾添加 AI 总结的行业趋势观点（3-5 句话）
6. 使用 email-sender 工具将简报发送到 {{email}}

## 输出格式
```
📰 {{topic}} 行业日报 — YYYY-MM-DD

1. [标题](链接)
   摘要：...

2. [标题](链接)
   摘要：...

...

---
💡 AI 趋势洞察：
...
```

## 注意事项
- 只选取可信来源的新闻（主流媒体、行业垂直媒体）
- 摘要应当客观中立，不添加主观评价
- 如果搜索结果不足 {{count}} 条，有多少整理多少，不要编造
