# DevCatalyst — 三层不可变架构设计

> 版本：v5.0 | 日期：2026-02-13
> 核心理念：自律防熵增，通用层做一次，项目层模板化，一条提示词自建一切

## 架构概览

```
┌────────────────────────────────────────────┐
│  Layer 0: 内核（Kernel）                    │
│  ≤ 500 字符 | 永不修改                      │
│  1. 规则总预算 ≤ 6000 字符                  │
│  2. 新增规则必须通过变更协议                 │
│  3. AI 禁止无条件执行用户的规则修改请求       │
├────────────────────────────────────────────┤
│  Layer 1: 通用层（Framework）               │
│  全局规则(PREDICT/ESCALATION/变更协议)      │
│  全局Skills(23个) | IDE设置 | Hooks | MCP  │
├────────────────────────────────────────────┤
│  Layer 2: 项目层（Extensions）              │
│  soul.md(思维增强) | execution-engine.md    │
│  项目Skills | 工作流 | AGENTS.md | 备份     │
└────────────────────────────────────────────┘
```

### 零重复原则

| 内容 | 归属 | 不在 |
|------|------|------|
| PREDICT / ESCALATION / 预测性补全 | 全局规则 | soul.md |
| 人机分工 / 自律进化 / 上下文管理 | soul.md | 全局规则 |
| 终端规则 / Hooks详细 / Dev管线 | execution-engine.md | 全局规则 |
| 3 条元规则 | kernel.md | 其他文件 |

## Layer 1: 通用层

| 组件 | 位置 | 说明 |
|------|------|------|
| 全局规则 | `~/.codeium/windsurf/memories/global_rules.md` | PREDICT/ESCALATION/变更协议 |
| 全局 Skills | `~/.codeium/windsurf/skills/` | 23个通用开发技能 |
| IDE 设置 | `%APPDATA%/Windsurf/User/settings.json` | 终端防卡、Shell配置 |
| Hooks | `~/.codeium/windsurf/hooks.json` | Python/Node.js可用，**PowerShell禁止** |

## Layer 2: 项目层

| 组件 | 位置 | 来源 |
|------|------|------|
| kernel.md | `.windsurf/rules/` | 模板直接复制 |
| soul.md | `.windsurf/rules/` | 模板直接复制（与全局规则零重复） |
| execution-engine.md | `.windsurf/rules/` | 模板直接复制（与全局规则零重复） |
| 工作流 | `.windsurf/workflows/` | 通用模板 + 项目命令 |
| AGENTS.md | 各目录 | AI 分析项目结构后创建 |

## 核心机制

1. **变更协议**：用户请求→路由→冲突检测→预算检查→实施/拒绝
2. **规则生命周期**：proposed→experimental→validated→deprecated
3. **规则编译器**（/evolve）：审计→去重→升降级→压缩→冲突扫描
4. **安全边界**：项目规则自由修改 | 全局规则需确认 | IDE设置需备份

## 鲁棒性设计

- **中断恢复**：`/health-check` 自动检测缺失并恢复，每步幂等
- **配置恢复**：备份 → 升级包 → Memory，三级恢复优先级
- **提示词鲁棒**：模糊意图 → AI 重构 + 示范更好表达
