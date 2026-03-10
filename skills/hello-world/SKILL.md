---
name: hello-world
description: 最简单的 Skill 示例，向用户打招呼并介绍 ChatableX Skills 系统
version: 1.0.0
author: ChatableX
category: other
variables:
  - name: username
    type: string
    required: false
    default: "朋友"
    description: 用户的名字
---

# Hello World Skill

## 什么时候使用这个技能
当用户说"你好"、"介绍一下 Skills"或者需要一个简单的 Skill 示例时使用。

## 执行步骤
1. 向 `{{username}}` 打招呼
2. 简单介绍 ChatableX Skills 系统的核心概念
3. 说明如何创建自己的第一个 Skill

## 输出格式
使用友好的语气，包含：
- 欢迎语
- Skills 系统的三句话介绍
- 一个创建 Skill 的快速指引链接
