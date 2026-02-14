---
description: 新项目一键引导：当用户在新项目中首次使用 DevCatalyst 时，自动配置项目专属规则、技能、工作流。用户只需发一条提示词即可完成全部配置。
---

# /onboard — 新项目一键引导工作流

> 让小白用户也能一键获得完整的 AI 开发环境配置，无需理解底层架构。

## 触发方式
- 用户在新项目中说 `/onboard` 或「帮我配置这个项目」
- AI 检测到项目缺少 `.windsurf/` 目录时主动建议

## Step 1: 项目分析（自动执行）

// turbo
扫描项目结构，识别：
- **语言/框架**：package.json / requirements.txt / go.mod / Cargo.toml / pom.xml 等
- **项目类型**：Web前端 / 后端API / 全栈 / CLI / 库 / 数据分析 / 文档
- **已有工具**：ESLint / Prettier / pytest / Docker / CI配置
- **代码规模**：文件数量、目录深度、主要代码目录

## Step 2: 生成项目配置（自动执行）

根据分析结果，创建以下文件：

### `.windsurf/rules/soul.md`
从模板 `project-templates/soul.md` 复制，并根据项目类型调整：
- 项目定位描述
- 技术栈声明
- 特定于项目类型的约定

### `.windsurf/rules/execution-engine.md`
从模板 `project-templates/execution-engine.md` 复制，并调整：
- 测试命令（npm test / pytest / go test 等）
- 构建命令
- 启动命令

### `AGENTS.md`
根据项目结构生成目录级指令：
- 项目概述
- 关键目录说明
- 开发约定

## Step 3: 技能匹配

从已部署的技能中，根据项目类型自动推荐：

| 项目类型 | 推荐技能 |
|---------|---------|
| Web前端 | frontend-dev, write-tests, code-review |
| 后端API | api-design, api-testing, database-design, docker-deploy |
| 全栈 | 以上全部 + ci-cd-setup |
| Python | write-tests, error-diagnosis, performance-optimize |
| 通用 | code-review, git-smart-commit, doc-generator |

## Step 4: 注册项目

将项目添加到 `management/PROJECT_REGISTRY.md`：
```markdown
| [项目名] | [路径] | [类型] | [日期] | 从未收割 | 活跃 |
```

## Step 5: 用户确认

展示配置摘要：
```
🚀 项目引导完成！

项目：[名称]（[类型]）
技术栈：[检测到的技术栈]

已创建：
  ✅ .windsurf/rules/soul.md（项目灵魂）
  ✅ .windsurf/rules/execution-engine.md（执行引擎）
  ✅ AGENTS.md（目录指令）

推荐技能：[列表]

已注册到 DevCatalyst 管理中心。
后续 AI 将根据你的开发习惯自动优化这些配置。
```

## Step 6: 启动学习模式

在项目的 Memory 中创建初始条目：
- 项目类型和技术栈
- 初始配置状态
- 标记为「学习中」— 前 10 次对话将积极收集用户偏好

## 冷启动优化

对于全新用户（无历史对话）：
1. 使用通用模板的默认配置
2. 在前 3 次对话中询问关键偏好：
   - 「你喜欢详细还是简洁的代码注释？」
   - 「你的 Git 提交习惯是什么？」
   - 「你有偏好的代码风格吗？」
3. 将回答写入 Memory，逐步个性化

对于有历史的用户：
1. 从 Memory 中提取已知偏好
2. 结合项目类型生成更个性化的配置
3. 跳过偏好询问，直接应用
