# DevCatalyst

**一小段文字，释放 AI 编程助手的全部智能。**

> A tiny config that catalyzes your AI coding assistant into a truly intelligent collaborator.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 这是什么？

DevCatalyst 是一套**自律配置架构**，让 AI 编程助手（如 Windsurf Cascade）从"指令执行器"变成"智能协作者"。

- 📦 **极简**：核心规则不到 6000 字符，却能显著提升 AI 的代码质量、主动性和问题解决能力
- 🧬 **自律**：内置规则预算制 + 变更协议 + 生命周期管理，**防止配置膨胀**
- 🔄 **自进化**：AI 在日常工作中自动观察、记录和优化自身配置
- 🛡️ **安全**：跨项目修改有保护机制，全局配置变更需确认
- ⚡ **一键部署**：一条提示词完成全部安装

## 解决什么问题？

### 规则熵增问题

每个 AI 编程助手的用户都会遇到：

```
不断添加规则 → 短期有效 → 长期冗余矛盾 → AI 效率下降 → 再加规则修补 → 恶性循环
```

现有方案（如 ARM、aicodingrules.org）解决了规则的**分发**，但没有解决**进化过程中的自律**。

DevCatalyst 的核心创新是**规则编译器模式**：

| 机制 | 作用 |
|------|------|
| **预算制** | always-on 规则总量 ≤ 6000 字符，强制精简 |
| **变更协议** | 用户说"加规则"时，AI 先路由→冲突检测→预算检查 |
| **生命周期** | 新想法默认进 Memory 观察，验证 3+ 次才升级为规则 |
| **规则编译** | `/evolve` 定期去重、压缩、降级未使用规则 |

## 架构

```
┌─────────────────────────────────────┐
│  Layer 0: 内核 (≤500 chars)         │ ← 3 条元规则，永不修改
│  预算制 | 变更协议 | AI不盲加规则    │
├─────────────────────────────────────┤
│  Layer 1: 框架 (≤3000 chars)        │ ← 决策框架 + 执行引擎
│  PREDICT | ESCALATION | 安全约束    │
├─────────────────────────────────────┤
│  Layer 2: 扩展 (≤2500 chars)        │ ← 项目特定 + 用户自定义
│  语言规则 | 项目结构 | 自定义       │
└─────────────────────────────────────┘
```

## 快速开始

### 方式 1：一键部署（推荐）

在 Windsurf 中新建对话，粘贴：

```
请阅读 {DevCatalyst路径}/installer/INSTALLER.md 并按步骤执行完整安装。
```

### 方式 2：手动安装

1. **全局规则**：将 `core/global-rules.md` 内容复制到 Windsurf Settings → AI Rules
2. **项目规则**：在项目中创建 `.windsurf/rules/` 目录，放入 `soul.md` 和 `execution-engine.md`
3. **验证**：运行 `/health-check` 确认安装完整

## 核心理念

### PREDICT 决策框架

- **P**redict — 预测用户下一步需要什么
- **R**esearch — 先搜索再动手
- **E**xecute — 一次性闭环完成
- **D**ocument — 重要发现写入 Memory
- **I**terate — 反思改进
- **C**omplete — 主动补全遗漏
- **T**ransfer — 经验迁移

### ESCALATION 问题升级

1. **L1** 自主解决（仅限简单改动）
2. **L2** 搜索研究（默认起点）
3. **L3** 人机协作（请用户观察 AI 看不到的）
4. **L4** 用户指挥（承认无效，请用户给方向）

### 自律进化

- **双输出原则**：每次交互产生任务结果 + 系统进化
- **规则路由**：80% 的"规则请求"应路由到 Memory 或 Skill，不是规则文件
- **进化质量门槛**：重复性 + 通用性 + 可操作性 + 不冲突 → 4Yes 才固化

## 工作流

| 命令 | 功能 |
|------|------|
| `/dev` | 全流程开发：需求→研究→设计→实现→构建→部署→文档 |
| `/evolve` | 系统进化：审查+编译+优化规则/Skills/Memory |
| `/health-check` | 健康检查：检测配置完整性+预算使用率 |
| `/review` | 代码审查 |
| `/debug-escalation` | 逐层升级调试 |

## 与其他方案的对比

| 特性 | DevCatalyst | ARM | .cursorrules |
|------|-------------|-----|-------------|
| 规则分发 | ✅ 一键部署 | ✅ 包管理 | ❌ 手动复制 |
| 防膨胀 | ✅ 预算制+编译器 | ❌ | ❌ |
| 自进化 | ✅ 被动+主动 | ❌ | ❌ |
| 变更协议 | ✅ 路由+冲突+预算 | ❌ | ❌ |
| 生命周期 | ✅ proposed→validated→deprecated | ❌ | ❌ |

## 适配状态

- ✅ **Windsurf (Cascade)** — 完整支持
- ⏳ **Cursor** — 规划中
- ⏳ **GitHub Copilot** — 规划中
- ⏳ **Claude Code** — 规划中

## 版本历史

- **v5.0** — 自律架构：预算制 + 变更协议 + 规则编译器 + 生命周期管理
- v4.0 — 规则精简 75% + Hooks 策略修正 + Context Engineering
- v3.0 — 活体智能架构 + 两层分离 + 用户教练

## License

MIT
