# 🔭 AI Observatory

**DevCatalyst Intelligence Pack — AI 行为监控与可视化系统**

## 概述

AI Observatory 通过 Windsurf Cascade Hooks 拦截所有 AI 动作，记录结构化日志，并生成可视化仪表盘。
从「写规则祈祷生效」进化到「程序化监控确保生效」。

## 架构

```
Cascade 执行操作 → 11 个 Hook 事件触发 → hook_logger.py
  → cascade_log.jsonl（结构化日志）
  → stats.json（运行统计）
  → dashboard.html（可视化仪表盘，每次 AI 回复后自动刷新）
```

## 文件结构

```
observatory/
├── hook_logger.py      # 主脚本：日志记录 + 统计 + 仪表盘生成
├── hooks.json          # Hook 配置源文件（已部署到 ~/.codeium/windsurf/）
├── README.md           # 本文档
└── logs/               # 自动生成
    ├── cascade_log.jsonl   # 结构化事件日志（JSONL 格式）
    ├── stats.json          # 累计统计数据
    └── dashboard.html      # 可视化仪表盘（浏览器打开）
```

## 监控的 11 个事件

| 事件 | 类型 | 说明 |
|------|------|------|
| `pre_read_code` | 拦截 | AI 读文件前 |
| `post_read_code` | 记录 | AI 读文件后 |
| `pre_write_code` | 拦截 | AI 改代码前（含完整 diff） |
| `post_write_code` | 记录 | AI 改代码后 |
| `pre_run_command` | 拦截 | AI 跑命令前 |
| `post_run_command` | 记录 | AI 跑命令后 |
| `pre_mcp_tool_use` | 拦截 | AI 用 MCP 工具前 |
| `post_mcp_tool_use` | 记录 | AI 用 MCP 工具后 |
| `pre_user_prompt` | 审计 | 用户发消息前 |
| `post_cascade_response` | 分析 | AI 完成回复后（含规则触发信息） |
| `post_setup_worktree` | 记录 | 创建 worktree 后 |

## 仪表盘功能

- **Total Events** — 累计事件总数
- **Sessions** — 独立对话会话数
- **Rules Tracked** — 被触发的规则数量及频次
- **Files Touched** — 被访问/修改的文件统计
- **Event Distribution** — 各类事件的分布柱状图
- **Rule Effectiveness** — 规则触发排行（哪些规则真正生效）
- **Recent Operations** — 最近操作时间线
- **Top Files** — 最常被访问的文件

## 使用方法

### 查看仪表盘
在浏览器中打开 `observatory/logs/dashboard.html`，每 30 秒自动刷新。

### 手动刷新仪表盘
```bash
python observatory/hook_logger.py --dashboard
```

### 查看原始日志
```bash
# 最近 20 条事件
Get-Content observatory/logs/cascade_log.jsonl -Tail 20
```

### 重置数据
```bash
Remove-Item observatory/logs/* -Force
```

## 部署位置

- **Hook 配置**：`C:\Users\zhouyoukang\.codeium\windsurf\hooks.json`
- **源文件**：`e:\windsurf-intelligence-pack\observatory\hooks.json`

## 注意事项

- Hook 脚本仅使用 Python（禁止 PowerShell hooks，会导致终端卡死）
- 日志文件超过 5MB 时自动轮转，保留最近 10000 条
- `show_output: false` 避免 Hook 输出干扰 Cascade 正常工作
- `post_cascade_response` 和 `pre_user_prompt` 的 show_output 不受配置控制

## Phase 路线图

- **Phase 1** ✅ Hook 日志 + HTML 仪表盘（当前）
- **Phase 2** 🔜 Web 实时仪表盘（Flask/Node + 文件监听）
- **Phase 3** 📋 VS Code/Windsurf 侧边栏扩展
