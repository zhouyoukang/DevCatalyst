---
description: AI Observatory 监控系统的部署、验证、维护和升级工作流
---

# AI Observatory 工作流

## Phase 1: 部署（首次或重新部署）

1. 确认 Python 可用
```bash
python --version
```

2. 确认 hook_logger.py 存在
```bash
// turbo
Get-Item e:\windsurf-intelligence-pack\observatory\hook_logger.py
```

3. 部署 hooks.json 到 Windsurf
```bash
Copy-Item "e:\windsurf-intelligence-pack\observatory\hooks.json" "C:\Users\zhouyoukang\.codeium\windsurf\hooks.json" -Force
```

4. 生成初始仪表盘
```bash
// turbo
python e:/windsurf-intelligence-pack/observatory/hook_logger.py --dashboard
```

5. 验证仪表盘文件存在
```bash
// turbo
Test-Path "e:\windsurf-intelligence-pack\observatory\logs\dashboard.html"
```

## Phase 2: 验证（端到端测试）

1. 发送模拟事件测试日志记录
```bash
'{"agent_action_name":"post_cascade_response","trajectory_id":"test","execution_id":"test","timestamp":"2026-01-01T00:00:00Z","tool_info":{"response":"- (Always On) Triggered Rule: test.md"}}' | python e:/windsurf-intelligence-pack/observatory/hook_logger.py
```

2. 检查日志文件是否写入
```bash
// turbo
Test-Path "e:\windsurf-intelligence-pack\observatory\logs\cascade_log.jsonl"
```

3. 检查统计文件是否更新
```bash
// turbo
Get-Content "e:\windsurf-intelligence-pack\observatory\logs\stats.json" | ConvertFrom-Json | Select-Object total_events
```

4. 在浏览器中打开仪表盘确认可视化
```bash
Start-Process "e:\windsurf-intelligence-pack\observatory\logs\dashboard.html"
```

5. 清理测试数据（可选）
```bash
Remove-Item "e:\windsurf-intelligence-pack\observatory\logs\cascade_log.jsonl" -Force -ErrorAction SilentlyContinue
Remove-Item "e:\windsurf-intelligence-pack\observatory\logs\stats.json" -Force -ErrorAction SilentlyContinue
python e:/windsurf-intelligence-pack/observatory/hook_logger.py --dashboard
```

## Phase 3: 日常维护

### 查看仪表盘
浏览器打开 `e:\windsurf-intelligence-pack\observatory\logs\dashboard.html`（每30秒自动刷新）

### 手动刷新仪表盘
```bash
// turbo
python e:/windsurf-intelligence-pack/observatory/hook_logger.py --dashboard
```

### 查看原始日志（最近20条）
```bash
// turbo
Get-Content "e:\windsurf-intelligence-pack\observatory\logs\cascade_log.jsonl" -Tail 20
```

### 查看规则触发统计
```bash
// turbo
(Get-Content "e:\windsurf-intelligence-pack\observatory\logs\stats.json" | ConvertFrom-Json).rules_triggered
```

### 重置所有数据
```bash
Remove-Item "e:\windsurf-intelligence-pack\observatory\logs\cascade_log.jsonl" -Force -ErrorAction SilentlyContinue
Remove-Item "e:\windsurf-intelligence-pack\observatory\logs\stats.json" -Force -ErrorAction SilentlyContinue
python e:/windsurf-intelligence-pack/observatory/hook_logger.py --dashboard
```

## Phase 4: 升级路径

### Phase 2 升级 → Web 实时仪表盘
- 用 Flask/Node.js 创建 HTTP 服务
- 添加 WebSocket 实时推送
- 历史趋势图表（Chart.js）
- 触发条件：Phase 1 使用稳定 + 用户需要更丰富的可视化

### Phase 3 升级 → IDE 侧边栏扩展
- 基于 VS Code Extension API
- Webview sidebar panel 显示实时状态
- 原生通知集成
- 触发条件：Phase 2 验证价值 + 用户有扩展开发经验

## 故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| dashboard.html 不存在 | 日志被清理 | `python hook_logger.py --dashboard` |
| Hook 不触发 | hooks.json 未部署 | 重新执行 Phase 1 步骤 3 |
| Python 报错 | 路径或版本问题 | 检查 `python --version` 和脚本路径 |
| 日志文件过大 | 长期使用 | 脚本自动轮转（>5MB 保留最近 10000 条） |
| IDE 卡顿 | Hook 脚本耗时过长 | 检查 hook_logger.py 是否有阻塞操作 |
