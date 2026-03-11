# 贡献指南

感谢你有兴趣为 ChatableX Skills 生态做贡献！

## 快速开始

### 我不会编程

没关系！创建 Skill 不需要编程。打开 ChatableX 客户端，在 Skill 编辑器中用所见即所得的方式编写，然后一键提交审核。详见 [README - 应用内发布](README.md#方式一应用内发布推荐)。

### 我是开发者

Fork 本仓库，在 `skills/` 下创建你的 Skill 文件夹，提交 PR 到 `review` 分支。详见 [README - Git PR 发布](README.md#方式二git-pr-发布开发者)。

## 命名规范

| 项目 | 规范 | 示例 |
|------|------|------|
| Skill 文件夹名 | 小写字母 + 连字符 | `daily-news-briefing` |
| `name` 字段 | 与文件夹名一致 | `daily-news-briefing` |
| `version` | 语义化版本 | `1.0.0` |
| PR 标题 | `[Skill] name vX.Y.Z` | `[Skill] daily-news-briefing v1.0.0` |
| 分支名 | `skill/name` 或自动 `submissions/name/version` | `skill/daily-news-briefing` |

## PR 审核标准

我们会从以下几个方面 Review 你的 Skill：

1. **有用性**：Skill 解决了真实的使用场景吗？
2. **质量**：指令是否清晰、具体、可执行？
3. **安全性**：scripts/ 中是否有不安全的代码？
4. **规范性**：是否遵循了 SKILL.md 格式规范？
5. **独特性**：是否与已有 Skill 功能重复？
6. **文件输出**：如果 Skill 会生成文件，是否使用了 `{{output_dir}}`？是否 `print()` 了绝对路径？

## 审核流程

1. 提交 PR → 自动 CI 校验
2. CI 通过 → Reviewer 人工审核
3. 审核通过 → 合并到 `review` 分支
4. 管理员定期将 `review` 合并到 `main` → 上架商店

整个流程通常在 3-5 个工作日内完成。

## 常见退回原因

- `name` 或 `description` 为空
- 指令过于模糊（如"帮我处理一下"）
- scripts/ 中有危险操作（任意文件删除、未知域名请求等）
- 文件夹超过 5MB 大小限制
- 与已有 Skill 高度重复
- 文件输出使用硬编码路径而非 `{{output_dir}}`（详见 [README - 文件输出规范](README.md#文件输出规范)）
- 生成文件后没有 `print()` 绝对路径（文件将不会在聊天中显示）

## 行为准则

- 提交的内容必须是原创或有合法授权
- 不提交恶意代码、垃圾内容或违法内容
- 尊重其他贡献者，文明交流
