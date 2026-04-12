---
description: System self-evolution — audit, compile, simplify
---

# /evolve — 自进化

> 反者道之动。物壮则老，是谓不道。 —— 第四十章·第三十章

## Phase 1: 审计
// turbo
1. 读取所有 always-on 规则文件，统计总量
2. 检查：冗余、冲突、过时、膨胀
3. 检查 Memory：陈旧、重复、缺失

## Phase 2: 编译（反熵核心）
1. **去重** — 语义重复则合并
2. **压缩** — 保语义，减表达
3. **降级** — 未触发规则 → Memory
4. **升级** — Memory 验证3+次 → 规则（预算内）
5. **冲突扫描** — 矛盾则取其一

## Phase 3: 实施
- 明确错误 → 立即修
- 权衡取舍 → 建议用户
- 不确定 → 记入 Memory 观察

## Phase 4: 报告
```
## Evolution Report
| 类别 | 发现 | 动作 | 状态 |
|------|------|------|------|
```
