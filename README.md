# ChatableX Skills

ChatableX 官方技能仓库 —— 社区贡献的 AI Agent 技能集合。

每个 Skill 是一个文件夹，包含 `SKILL.md` 指令文件和可选的脚本、参考文档、资源文件。ChatableX 客户端的 Skills 商店直接从本仓库拉取已发布的技能。

---

## 目录

- [什么是 Skill？](#什么是-skill)
- [Skill 文件夹结构](#skill-文件夹结构)
- [SKILL.md 规范](#skillmd-规范)
  - [Frontmatter 字段说明](#frontmatter-字段说明)
  - [Markdown 正文规范](#markdown-正文规范)
- [子目录说明](#子目录说明)
- [发布方式](#发布方式)
  - [方式一：应用内发布（推荐）](#方式一应用内发布推荐)
  - [方式二：Git PR 发布（开发者）](#方式二git-pr-发布开发者)
- [分支策略](#分支策略)
- [CI 校验规则](#ci-校验规则)
- [示例 Skill](#示例-skill)
- [FAQ](#faq)
- [License](#license)

---

## 什么是 Skill？

Skill（技能）是 ChatableX 三层扩展体系中的顶层概念：

```
ChatableX 扩展体系
│
├── Tool（工具）      纯功能性，无 UI（如 web-search、calculator）
├── AI App（应用）    带 WebUI 的完整应用（如 Web Excel、Todo-List）
└── Skill（技能）     SKILL.md 指令 + 工具组合 ← 你在这里
```

**简单来说**：Tool 是乐高积木，Skill 是用积木拼好的作品。

Skill 的核心是一个 `SKILL.md` 文件，用 Markdown 编写，告诉 AI Agent「做什么」和「怎么做」。不需要写代码，只要会写文字就能创建 Skill。

---

## Skill 文件夹结构

```
skills/
└── daily-news-briefing/         # Skill ID（小写、连字符分隔）
    ├── SKILL.md                 # 必须：指令 + 元数据
    ├── scripts/                 # 可选：可执行脚本
    │   └── summarize.py
    ├── references/              # 可选：参考文档（上下文注入）
    │   └── news-format-guide.md
    └── assets/                  # 可选：模板、图片等资源
        └── email-template.html
```

| 文件/目录 | 是否必须 | 说明 |
|-----------|---------|------|
| `SKILL.md` | **必须** | 技能的核心定义，包含 YAML frontmatter 和 Markdown 指令 |
| `scripts/` | 可选 | Python/Bash 脚本，作为 Skill 自带的工具注册到 Agent runtime |
| `references/` | 可选 | 参考文档，Skill 激活时按需加载到 Agent 上下文 |
| `assets/` | 可选 | 模板、图片等静态资源 |

---

## SKILL.md 规范

SKILL.md 由两部分组成：**YAML Frontmatter**（元数据）和 **Markdown 正文**（指令）。

### 完整示例

```markdown
---
name: daily-news-briefing
description: 搜索今日行业新闻，整理成简报并发送邮件
version: 1.0.0
author: your-username
category: productivity
tool_ids:
  - google-search
  - email-sender
variables:
  - name: topic
    type: string
    required: true
    description: 搜索主题（如"人工智能"、"新能源"）
  - name: email
    type: string
    required: true
    description: 接收简报的邮箱地址
  - name: count
    type: number
    required: false
    default: 10
    description: 新闻条数
---

# 今日行业新闻简报

## 什么时候使用这个技能
当用户需要获取某个行业的最新新闻并整理成简报时使用。

## 执行步骤
1. 使用 google-search 工具搜索 `{{topic}}` 的最新新闻
2. 筛选 Top `{{count}}` 最相关的新闻
3. 整理成结构化简报（标题、摘要、链接）
4. 使用 email-sender 工具发送到 `{{email}}`

## 输出格式
简报应包含：
- 日期和主题标题
- 每条新闻：标题、一句话摘要、原文链接
- 底部附上 AI 总结的行业趋势观点
```

### Frontmatter 字段说明

| 字段 | 类型 | 是否必填 | 说明 |
|------|------|---------|------|
| `name` | string | **必填** | Skill 唯一标识，小写字母 + 连字符（如 `daily-news-briefing`） |
| `description` | string | **必填** | 一句话描述技能用途，用于商店搜索和 Agent 自动匹配 |
| `version` | string | **必填** | 语义化版本号（如 `1.0.0`） |
| `author` | string | 推荐 | 作者名称或 GitHub 用户名 |
| `category` | string | 推荐 | 分类标签，可选值见下方 |
| `tool_ids` | string[] | 可选 | 引用的外部工具 ID 列表，安装时自动检查依赖 |
| `variables` | object[] | 可选 | 可配置参数列表，安装后用户可填写 |

**category 可选值**：

| 值 | 说明 |
|----|------|
| `productivity` | 生产力（邮件、日程、文档处理） |
| `data-analysis` | 数据分析（报表、统计、可视化） |
| `content-creation` | 内容创作（写作、翻译、设计） |
| `development` | 开发工具（代码生成、调试、部署） |
| `research` | 研究调研（搜索、文献整理、总结） |
| `automation` | 自动化（定时任务、批处理） |
| `education` | 教育学习 |
| `other` | 其他 |

**variables 字段详解**：

```yaml
variables:
  - name: topic          # 变量名（用于 {{topic}} 替换）
    type: string         # 类型：string | number | boolean | select
    required: true       # 是否必填
    description: 搜索主题  # 变量说明（展示给用户）
    default: "AI"        # 默认值（可选）
    options:             # 当 type 为 select 时的选项列表
      - value: "tech"
        label: "科技"
      - value: "finance"
        label: "金融"
```

### Markdown 正文规范

正文使用标准 Markdown 语法，建议包含以下章节：

| 章节 | 说明 | 重要性 |
|------|------|--------|
| **什么时候使用这个技能** | 描述适用场景，帮助 Agent 自动判断何时激活 | 强烈建议 |
| **执行步骤** | 清晰的分步指令，Agent 会逐步执行 | **必须** |
| **输出格式** | 期望的输出结构和格式 | 推荐 |
| **注意事项** | 边界情况、限制条件 | 可选 |
| **示例** | 输入/输出示例 | 可选 |

**写好 SKILL.md 的技巧**：

1. **具体明确**：避免模糊指令如「整理一下」，改为「按时间倒序排列，每条包含标题和摘要」
2. **使用变量**：用 `{{variable_name}}` 标记可替换参数，提高技能的通用性
3. **分步骤写**：每个步骤一个编号，Agent 会按顺序执行
4. **声明工具**：在 frontmatter 的 `tool_ids` 中列出所有需要的工具，确保用户安装时自动检查依赖
5. **说明场景**：清楚描述「什么时候该用」，Agent 的自动匹配依赖 `description` 和正文第一段

---

## 子目录说明

### scripts/

存放 Skill 自带的可执行脚本。脚本会被注册为 Agent 的内置工具，在 Skill 激活时自动加载。

```python
# scripts/summarize.py
"""
tool_name: summarize_text
description: 将长文本压缩为指定字数的摘要
"""

def run(text: str, max_words: int = 100) -> str:
    # 你的处理逻辑
    ...
```

**要求**：
- 支持 Python 3.10+
- 文件顶部用 docstring 声明 `tool_name` 和 `description`
- 入口函数名为 `run`，参数和返回值都有类型标注
- 不要引入大型依赖（优先使用标准库）
- 不执行危险操作（删除文件、网络请求到未知域名等）

### references/

参考文档，Skill 激活时按需注入到 Agent 上下文。适合放置：
- 格式模板
- 规范文档
- 领域知识

**要求**：
- 使用 Markdown 或纯文本格式
- 单个文件不超过 50KB（避免上下文溢出）

### assets/

静态资源文件，如邮件模板、图片素材等。

**要求**：
- 避免存放大文件（单文件 < 1MB，整个 Skill 文件夹 < 5MB）
- 图片优先使用 SVG 或压缩过的 PNG

---

## 发布方式

### 方式一：应用内发布（推荐）

适合所有用户，不需要任何 Git 知识。

1. 打开 ChatableX 客户端
2. 在侧边栏 Skills → My Skills → 创建新 Skill
3. 在 VS Code 风格的编辑器中编写 SKILL.md、添加脚本和资源
4. 拖入对话框测试效果
5. 点击「提交审核」

> 系统会自动将你的 Skill 文件夹推送到本仓库，创建一个 PR，你不需要手动操作 Git。

### 方式二：Git PR 发布（开发者）

适合熟悉 Git 的开发者。

```bash
# 1. Fork 本仓库

# 2. Clone 你的 Fork
git clone https://github.com/YOUR_USERNAME/ChatableX-skills.git
cd ChatableX-skills

# 3. 创建分支
git checkout -b skill/my-awesome-skill

# 4. 创建 Skill 目录
mkdir -p skills/my-awesome-skill/scripts
mkdir -p skills/my-awesome-skill/references
mkdir -p skills/my-awesome-skill/assets

# 5. 编写 SKILL.md
cat > skills/my-awesome-skill/SKILL.md << 'EOF'
---
name: my-awesome-skill
description: 描述你的技能
version: 1.0.0
author: your-username
category: productivity
---

# 我的技能

## 什么时候使用这个技能
...

## 执行步骤
1. ...
2. ...
EOF

# 6. 提交并推送
git add .
git commit -m "skill: add my-awesome-skill v1.0.0"
git push origin skill/my-awesome-skill

# 7. 在 GitHub 上创建 PR，目标分支选 review
```

**PR 要求**：
- 标题格式：`[Skill] skill-name vX.Y.Z`
- 目标分支：`review`（**不是 main**）
- 确保 SKILL.md frontmatter 中 `name`、`description`、`version` 已填写
- CI 检查通过后等待人工 Review

---

## 分支策略

本仓库使用三层分支保护策略，确保 `main` 分支始终干净可靠：

```
main          已发布的 Skills，客户端商店拉取源
  ↑            （受保护，仅 review → main 合并，需管理员审批）
  │
review        审核暂存区，所有 PR 的合并目标
  ↑            （CI + 人工 Review 后合并）
  │
  ├── submissions/{skill_id}/{version}   ← 应用内发布自动创建
  └── skill/{skill-name}                 ← 开发者手动创建
```

| 分支 | 用途 | 谁可以合并 |
|------|------|-----------|
| `main` | 已发布 Skills，商店数据源 | 仅管理员（从 review 合并） |
| `review` | 审核暂存区 | Reviewer 审核通过后合并 |
| `submissions/*` | 单次提交的工作分支 | 自动创建，合并后删除 |

**为什么不直接合并到 main？**

`main` 是商店的数据源，客户端直接拉取。`review` 分支作为缓冲区，允许管理员批量检查后统一发布到商店，避免审核通过但尚未确认的技能直接暴露给用户。

---

## CI 校验规则

每个 PR 会自动运行以下检查：

| 检查项 | 说明 | 必须通过 |
|--------|------|---------|
| **Frontmatter 校验** | `name`、`description` 必填 | 是 |
| **SKILL.md 存在** | 必须包含 `SKILL.md` 文件 | 是 |
| **文件大小检查** | 单文件 < 1MB，Skill 文件夹 < 5MB | 是 |
| **YAML 语法检查** | Frontmatter 是合法的 YAML | 是 |
| **scripts/ lint** | Python 文件基础语法检查（如有） | 是 |
| **安全扫描** | 检查 scripts/ 中是否有危险操作 | 是 |

> 顶层文件不做限制，你可以在 Skill 文件夹中放 LICENSE、README 等额外文件。

---

## 示例 Skill

仓库内置以下示例技能供参考：

| Skill | 分类 | 说明 |
|-------|------|------|
| [`hello-world`](skills/hello-world/) | other | 最简单的 Skill 示例，适合入门 |
| [`daily-news-briefing`](skills/daily-news-briefing/) | productivity | 完整示例：搜索新闻 → 整理简报 → 发邮件 |

---

## FAQ

**Q: Skill 和 Tool 有什么区别？**

Tool 是纯功能性的原子操作（如搜索、发邮件），Skill 是组合多个 Tool 并配上 Prompt 指令的完整工作流。Tool 需要编程能力开发，Skill 只需要写 Markdown。

**Q: 我的 Skill 被退回了怎么办？**

查看 PR 上的 Review 意见，修改后重新提交。应用内发布会自动更新 PR；Git 方式直接推送新 commit 到同一分支即可。

**Q: 可以引用不存在的 Tool 吗？**

可以在 `tool_ids` 中声明，但用户安装时系统会提示缺少依赖。建议只引用已发布在 ChatableX 工具市场中的 Tool。

**Q: Skill 可以不用任何 Tool 吗？**

可以。一个纯 Prompt 指令的 SKILL.md（不引用任何 tool_ids）也是有效的 Skill。比如「代码审查助手」这类纯对话指令型 Skill。

**Q: variables 是必须的吗？**

不是。如果你的 Skill 不需要参数化，可以省略 `variables` 字段。

**Q: 如何本地测试 Skill？**

在 ChatableX 客户端中，将 Skill 拖入对话框即可测试。草稿状态的 Skill 也可以拖入测试。

---

## License

本仓库中的 Skills 遵循 [MIT License](LICENSE)。

贡献者提交 PR 即表示同意以 MIT License 开源其 Skill 内容。
