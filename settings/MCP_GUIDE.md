# MCP Recommendation Guide

> Windsurf Cascade supports MCP (Model Context Protocol) to extend AI capabilities.
> Config: `~/.codeium/windsurf/mcp_config.json`
> **Important**: Total MCP tools limit **100**. Only enable what you need.

## Recommended MCP Servers

### Core (All projects)

| MCP | Use | Install |
|-----|-----|---------|
| **GitHub** | Repo management/PR/Issues | `npx @modelcontextprotocol/server-github` |
| **Chrome DevTools** | Browser debug/screenshots/DOM | Windsurf Marketplace |
| **Sequential Thinking** | Structured reasoning | Windsurf Marketplace |

### Development

| MCP | Use |
|-----|-----|
| **Context7** | 90+ framework docs real-time query |
| **Docker** | Container management |
| **Maven/Gradle** | JVM dependency query |

### Knowledge

| MCP | Use |
|-----|-----|
| **Memory** | Knowledge graph persistent memory |
| **Obsidian** | Obsidian notes access |

## Config Example

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "<YOUR_TOKEN>" }
    }
  }
}
```

## Principles

1. **Budget**: 100 tools max, disable unused MCP tools in settings
2. **On-demand**: Not all MCPs need to be always on
3. **Security**: API keys in env vars, never hardcode
4. **Performance**: Each MCP is a separate process
