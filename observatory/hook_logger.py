#!/usr/bin/env python3
"""
AI Observatory — Cascade Hook Logger & Dashboard Generator
Part of DevCatalyst Intelligence Pack

Monitors all Cascade AI actions through Windsurf Hooks,
records structured logs, and generates a visual dashboard.

Usage:
  Called automatically by Windsurf hooks (reads JSON from stdin)
  Manual dashboard refresh: python hook_logger.py --dashboard
"""

import sys
import json
import os
import re
from datetime import datetime
from pathlib import Path

# ─── Configuration ───────────────────────────────────────────────────────────

OBSERVATORY_DIR = Path(__file__).parent
LOG_DIR = OBSERVATORY_DIR / "logs"
LOG_FILE = LOG_DIR / "cascade_log.jsonl"
STATS_FILE = LOG_DIR / "stats.json"
DASHBOARD_FILE = LOG_DIR / "dashboard.html"
MAX_LOG_LINES = 10000
MAX_RECENT_FOR_DASHBOARD = 200

# ─── System Scanning Configuration ─────────────────────────────────────────

WINDSURF_HOME = Path.home() / ".codeium" / "windsurf"
PROJECT_ROOT = Path(__file__).resolve().parent.parent

SCAN_CATEGORIES = {
    "规则模板": {"path": PROJECT_ROOT / "project-templates", "icon": "📋", "exts": {".md"}},
    "工作流": {"path": PROJECT_ROOT / "workflows", "icon": "🔄", "exts": {".md"}},
    "管理文件": {"path": PROJECT_ROOT / "management", "icon": "📂", "exts": {".md"}},
    "观测站": {"path": PROJECT_ROOT / "observatory", "icon": "🔭", "exts": None},
    "全局Skills": {"path": WINDSURF_HOME / "skills", "icon": "🧠", "exts": {".md"}},
}

SCAN_KEY_FILES = {
    "全局规则": WINDSURF_HOME / "memories" / "global_rules.md",
    "Hooks配置": WINDSURF_HOME / "hooks.json",
    "MCP配置": WINDSURF_HOME / "mcp_config.json",
}

NEW_THRESHOLD_HOURS = 24
MODIFIED_THRESHOLD_HOURS = 168  # 7 days


def scan_system_state() -> dict:
    """Scan the DevCatalyst system to get current file state and recent changes."""
    now = datetime.now()
    state = {
        "categories": {},
        "recent_changes": [],
        "total_files": 0,
        "new_count": 0,
        "modified_count": 0,
        "skills_count": 0,
        "workflows_count": 0,
        "memory_count": 0,
        "conversation_count": 0,
        "mcp_count": 0,
    }

    for cat_name, cat_info in SCAN_CATEGORIES.items():
        dir_path = cat_info["path"]
        if not dir_path.exists():
            continue
        files = []
        for f in sorted(dir_path.rglob("*")):
            if not f.is_file() or f.name.startswith("."):
                continue
            if cat_info["exts"] and f.suffix.lower() not in cat_info["exts"]:
                continue
            try:
                st = f.stat()
                mtime = datetime.fromtimestamp(st.st_mtime)
                age_h = (now - mtime).total_seconds() / 3600
                status = "new" if age_h < NEW_THRESHOLD_HOURS else "modified" if age_h < MODIFIED_THRESHOLD_HOURS else "stable"
                rel = str(f.relative_to(PROJECT_ROOT)) if str(f).startswith(str(PROJECT_ROOT)) else f.name
                entry = {
                    "name": f.name, "rel": rel.replace("\\", "/"),
                    "size": st.st_size, "mtime_str": mtime.strftime("%m-%d %H:%M"),
                    "status": status, "mtime": mtime,
                }
                files.append(entry)
                state["recent_changes"].append({**entry, "category": cat_name, "icon": cat_info["icon"]})
                if status == "new":
                    state["new_count"] += 1
                elif status == "modified":
                    state["modified_count"] += 1
            except Exception:
                continue
        state["categories"][cat_name] = {"files": files, "icon": cat_info["icon"]}
        state["total_files"] += len(files)

    # Count specific resources
    for cat_name, cat_data in state["categories"].items():
        if cat_name == "全局Skills":
            state["skills_count"] = len(cat_data["files"])
        elif cat_name == "工作流":
            state["workflows_count"] = len(cat_data["files"])

    # Key single files
    for name, fpath in SCAN_KEY_FILES.items():
        if not fpath.exists():
            continue
        try:
            st = fpath.stat()
            mtime = datetime.fromtimestamp(st.st_mtime)
            age_h = (now - mtime).total_seconds() / 3600
            status = "new" if age_h < NEW_THRESHOLD_HOURS else "modified" if age_h < MODIFIED_THRESHOLD_HOURS else "stable"
            state["recent_changes"].append({
                "name": fpath.name, "rel": fpath.name, "category": name,
                "icon": "⚙️", "mtime": mtime, "mtime_str": mtime.strftime("%m-%d %H:%M"),
                "status": status, "size": st.st_size,
            })
        except Exception:
            continue

    # Count memories and conversations with rich metadata
    mem_dir = WINDSURF_HOME / "memories"
    cas_dir = WINDSURF_HOME / "cascade"
    imp_dir = WINDSURF_HOME / "implicit"
    state["memory_count"] = len(list(mem_dir.glob("*.pb"))) if mem_dir.exists() else 0
    state["conversation_count"] = len(list(cas_dir.glob("*.pb"))) if cas_dir.exists() else 0
    state["implicit_count"] = len(list(imp_dir.glob("*.pb"))) if imp_dir.exists() else 0

    # Conversation intelligence metadata + active process detection
    conv_meta = {"total_size_mb": 0, "oldest": None, "newest": None, "by_week": {}, "size_dist": [], "active": []}
    ACTIVE_THRESHOLD_MIN = 10  # Modified within last 10 min = active
    if cas_dir.exists():
        for pb in cas_dir.glob("*.pb"):
            try:
                st = pb.stat()
                sz_mb = st.st_size / (1024 * 1024)
                mt = datetime.fromtimestamp(st.st_mtime)
                age_min = (now - mt).total_seconds() / 60
                conv_meta["total_size_mb"] += sz_mb
                conv_meta["size_dist"].append({"name": pb.stem[:8], "size_mb": round(sz_mb, 1), "date": mt.strftime("%m-%d %H:%M"), "active": age_min < ACTIVE_THRESHOLD_MIN})
                week_key = mt.strftime("%m/%d")
                conv_meta["by_week"][week_key] = conv_meta["by_week"].get(week_key, 0) + 1
                if age_min < ACTIVE_THRESHOLD_MIN:
                    conv_meta["active"].append({"id": pb.stem[:8], "size_mb": round(sz_mb, 1), "last": mt.strftime("%H:%M:%S")})
                if conv_meta["oldest"] is None or mt < conv_meta["oldest"]:
                    conv_meta["oldest"] = mt
                if conv_meta["newest"] is None or mt > conv_meta["newest"]:
                    conv_meta["newest"] = mt
            except Exception:
                continue
        conv_meta["size_dist"].sort(key=lambda x: x.get("size_mb", 0), reverse=True)
        conv_meta["total_size_mb"] = round(conv_meta["total_size_mb"], 1)
    state["active_count"] = len(conv_meta["active"])
    state["conv_meta"] = conv_meta

    # Count MCP servers
    mcp_path = SCAN_KEY_FILES.get("MCP配置")
    if mcp_path and mcp_path.exists():
        try:
            mcp_data = json.loads(mcp_path.read_text(encoding="utf-8"))
            state["mcp_count"] = len(mcp_data.get("mcpServers", {}))
        except Exception:
            state["mcp_count"] = 0

    # Sort recent changes newest first
    state["recent_changes"].sort(key=lambda x: x.get("mtime", datetime.min), reverse=True)
    return state


def format_file_size(size: int) -> str:
    """Format file size in human-readable form."""
    if size < 1024:
        return f"{size} B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size / (1024 * 1024):.1f} MB"


# ─── Core Logging ───────────────────────────────────────────────────────────

def ensure_dirs():
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def log_event(data: dict):
    """Append a structured event to the JSONL log file."""
    ensure_dirs()
    data["_logged_at"] = datetime.now().isoformat()
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n")
    except Exception:
        pass
    rotate_log_if_needed()


def rotate_log_if_needed():
    """Keep only the last MAX_LOG_LINES entries to prevent unbounded growth."""
    try:
        if not LOG_FILE.exists():
            return
        size = LOG_FILE.stat().st_size
        if size < 5 * 1024 * 1024:  # Only rotate if > 5MB
            return
        lines = LOG_FILE.read_text(encoding="utf-8").strip().split("\n")
        if len(lines) > MAX_LOG_LINES:
            LOG_FILE.write_text(
                "\n".join(lines[-MAX_LOG_LINES:]) + "\n", encoding="utf-8"
            )
    except Exception:
        pass


# ─── Rule Extraction ────────────────────────────────────────────────────────

def extract_rules(response_text: str) -> dict:
    """Extract triggered rules from Cascade response text."""
    pattern = r"- \(([^)]+)\) Triggered Rule: (.+?)(?:\s*$)"
    rules = {}
    for match in re.finditer(pattern, response_text, re.MULTILINE):
        rule_type, rule_name = match.groups()
        rules.setdefault(rule_type, []).append(rule_name.strip())
    return rules


# ─── Statistics ──────────────────────────────────────────────────────────────

def load_stats() -> dict:
    """Load existing statistics or create new."""
    if STATS_FILE.exists():
        try:
            return json.loads(STATS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "total_events": 0,
        "events_by_type": {},
        "sessions": {},
        "rules_triggered": {},
        "files_accessed": {},
        "commands_executed": [],
        "alerts": [],
        "first_event": None,
        "last_updated": None,
    }


def save_stats(stats: dict):
    """Save statistics to file."""
    ensure_dirs()
    try:
        STATS_FILE.write_text(
            json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    except Exception:
        pass


def update_stats(data: dict) -> dict:
    """Update running statistics with new event data."""
    stats = load_stats()
    event = data.get("agent_action_name", "unknown")
    timestamp = data.get("timestamp", datetime.now().isoformat())
    traj_id = data.get("trajectory_id", "unknown")
    tool_info = data.get("tool_info", {})

    # ── Basic counts ──
    stats["total_events"] += 1
    stats["events_by_type"][event] = stats["events_by_type"].get(event, 0) + 1
    if not stats["first_event"]:
        stats["first_event"] = timestamp
    stats["last_updated"] = timestamp

    # ── Session tracking ──
    if traj_id not in stats["sessions"]:
        stats["sessions"][traj_id] = {
            "first_seen": timestamp,
            "event_count": 0,
            "events": {},
        }
    session = stats["sessions"][traj_id]
    session["event_count"] += 1
    session["last_seen"] = timestamp
    session["events"][event] = session["events"].get(event, 0) + 1

    # ── File access tracking ──
    if event in ("post_write_code", "post_read_code", "pre_write_code", "pre_read_code"):
        fp = tool_info.get("file_path", "")
        if fp:
            short = fp.replace("\\", "/").split("/")[-1]  # filename only
            stats["files_accessed"][short] = stats["files_accessed"].get(short, 0) + 1

    # ── Command tracking ──
    if event == "post_run_command":
        cmd = tool_info.get("command_line", "")
        if cmd:
            stats["commands_executed"].append(
                {
                    "cmd": cmd[:200],
                    "time": timestamp,
                    "cwd": tool_info.get("cwd", "")[:100],
                }
            )
            stats["commands_executed"] = stats["commands_executed"][-100:]

    # ── Rule extraction from post_cascade_response ──
    if event == "post_cascade_response":
        response = tool_info.get("response", "")
        rules = extract_rules(response)
        for rule_type, rule_list in rules.items():
            for rule_name in rule_list:
                key = f"[{rule_type}] {rule_name}"
                stats["rules_triggered"][key] = (
                    stats["rules_triggered"].get(key, 0) + 1
                )

    # ── Limit sessions to last 50 ──
    if len(stats["sessions"]) > 50:
        sorted_sessions = sorted(
            stats["sessions"].items(),
            key=lambda x: x[1].get("last_seen", ""),
            reverse=True,
        )
        stats["sessions"] = dict(sorted_sessions[:50])

    # ── Limit files_accessed to top 100 ──
    if len(stats["files_accessed"]) > 100:
        top = sorted(
            stats["files_accessed"].items(), key=lambda x: x[1], reverse=True
        )[:100]
        stats["files_accessed"] = dict(top)

    save_stats(stats)
    return stats


# ─── Recent Events Reader ───────────────────────────────────────────────────

def read_recent_events(n: int = MAX_RECENT_FOR_DASHBOARD) -> list:
    """Read the last N events from the JSONL log."""
    if not LOG_FILE.exists():
        return []
    try:
        lines = LOG_FILE.read_text(encoding="utf-8").strip().split("\n")
        recent = lines[-n:]
        events = []
        for line in recent:
            try:
                events.append(json.loads(line))
            except Exception:
                continue
        return events
    except Exception:
        return []


# ─── Dashboard Generator ────────────────────────────────────────────────────

def generate_dashboard(stats: dict):
    """Generate a self-contained HTML dashboard file."""
    ensure_dirs()
    recent = read_recent_events(100)

    # Prepare data for template
    total = stats.get("total_events", 0)
    session_count = len(stats.get("sessions", {}))
    rule_count = len(stats.get("rules_triggered", {}))
    file_count = len(stats.get("files_accessed", {}))
    last_updated = stats.get("last_updated", "N/A")
    if last_updated and last_updated != "N/A":
        try:
            last_updated = last_updated[:19].replace("T", " ")
        except Exception:
            pass

    # Event distribution bars
    events_by_type = stats.get("events_by_type", {})
    max_event_count = max(events_by_type.values()) if events_by_type else 1
    event_bars_html = ""
    event_labels = {
        "pre_read_code": "📖 读取文件（前）",
        "post_read_code": "📖 读取文件（后）",
        "pre_write_code": "✏️ 修改代码（前）",
        "post_write_code": "✏️ 修改代码（后）",
        "pre_run_command": "⚡ 执行命令（前）",
        "post_run_command": "⚡ 执行命令（后）",
        "pre_mcp_tool_use": "🔧 MCP工具（前）",
        "post_mcp_tool_use": "🔧 MCP工具（后）",
        "pre_user_prompt": "💬 用户消息（前）",
        "post_cascade_response": "🤖 AI回复（后）",
        "post_setup_worktree": "🌲 工作树（后）",
    }
    for etype in sorted(events_by_type.keys()):
        count = events_by_type[etype]
        pct = int((count / max_event_count) * 100) if max_event_count > 0 else 0
        label = event_labels.get(etype, etype)
        event_bars_html += f"""
        <div class="bar-row">
            <span class="bar-label">{label}</span>
            <div class="bar-track"><div class="bar-fill" style="width:{pct}%"></div></div>
            <span class="bar-count">{count}</span>
        </div>"""

    # Rules table
    rules = stats.get("rules_triggered", {})
    rules_sorted = sorted(rules.items(), key=lambda x: x[1], reverse=True)
    rules_html = ""
    for rule_key, count in rules_sorted:
        rules_html += f"<tr><td>{rule_key}</td><td class='num'>{count}</td></tr>\n"
    if not rules_html:
        rules_html = "<tr><td colspan='2' class='empty'>暂无规则触发记录（等待 AI 回复后自动采集）</td></tr>"

    # Recent operations
    recent_html = ""
    for ev in reversed(recent[-50:]):
        ts = ev.get("timestamp", ev.get("_logged_at", ""))
        if ts:
            ts = ts[11:19]  # HH:MM:SS
        action = ev.get("agent_action_name", "?")
        ti = ev.get("tool_info", {})
        detail = ""
        if "file_path" in ti:
            detail = ti["file_path"].replace("\\", "/").split("/")[-1]
        elif "command_line" in ti:
            detail = ti["command_line"][:60]
        elif "mcp_tool_name" in ti:
            detail = f'{ti.get("mcp_server_name","")}/{ti["mcp_tool_name"]}'
        elif "user_prompt" in ti:
            detail = ti["user_prompt"][:60]
        elif "response" in ti:
            detail = f'{len(ti["response"])} chars'

        icon = "📖" if "read" in action else "✏️" if "write" in action else "⚡" if "command" in action else "🔧" if "mcp" in action else "💬" if "prompt" in action else "🤖" if "response" in action else "📌"
        recent_html += f"""<div class="op-row">
            <span class="op-time">{ts}</span>
            <span class="op-icon">{icon}</span>
            <span class="op-action">{action}</span>
            <span class="op-detail" title="{detail}">{detail}</span>
        </div>\n"""
    if not recent_html:
        recent_html = '<div class="op-row"><span class="empty">暂无操作记录</span></div>'

    # Sessions summary
    sessions = stats.get("sessions", {})
    sessions_html = ""
    sorted_s = sorted(sessions.items(), key=lambda x: x[1].get("last_seen", ""), reverse=True)
    for sid, sdata in sorted_s[:10]:
        short_id = sid[:8]
        count = sdata.get("event_count", 0)
        first = sdata.get("first_seen", "")[:16].replace("T", " ")
        last = sdata.get("last_seen", "")[:16].replace("T", " ")
        sessions_html += f"<tr><td><code>{short_id}</code></td><td class='num'>{count}</td><td>{first}</td><td>{last}</td></tr>\n"
    if not sessions_html:
        sessions_html = "<tr><td colspan='4' class='empty'>暂无会话记录</td></tr>"

    # Top files
    files = stats.get("files_accessed", {})
    files_sorted = sorted(files.items(), key=lambda x: x[1], reverse=True)[:15]
    files_html = ""
    for fname, count in files_sorted:
        files_html += f"<tr><td>{fname}</td><td class='num'>{count}</td></tr>\n"
    if not files_html:
        files_html = "<tr><td colspan='2' class='empty'>暂无文件访问记录</td></tr>"

    # ── System scan for evolution tracking + dynamic overview ──
    try:
        sys_state = scan_system_state()
    except Exception:
        sys_state = {"categories": {}, "recent_changes": [], "total_files": 0,
                     "new_count": 0, "modified_count": 0, "skills_count": 0,
                     "workflows_count": 0, "memory_count": 0, "conversation_count": 0,
                     "mcp_count": 0, "implicit_count": 0,
                     "conv_meta": {"total_size_mb": 0, "oldest": None, "newest": None, "by_week": {}, "size_dist": []}}

    # Architecture tree HTML
    tree_html = ""
    for cat_name, cat_data in sys_state["categories"].items():
        flist = cat_data["files"]
        icon = cat_data["icon"]
        new_in_cat = sum(1 for f in flist if f["status"] == "new")
        mod_in_cat = sum(1 for f in flist if f["status"] == "modified")
        badges = ""
        if new_in_cat:
            badges += f' <span class="badge-new">+{new_in_cat} 新</span>'
        if mod_in_cat:
            badges += f' <span class="badge-mod">{mod_in_cat} 改</span>'
        tree_html += f'<div class="tree-cat"><div class="tree-hdr" onclick="toggleTree(this)">'
        tree_html += f'<span class="tree-arrow">&#9654;</span> {icon} <strong>{cat_name}</strong>'
        tree_html += f' <span class="tree-cnt">({len(flist)} 个文件)</span>{badges}</div>'
        tree_html += '<div class="tree-body" style="display:none">'
        for fi in flist:
            sc = fi["status"]
            badge = ' <span class="badge-new">新</span>' if sc == "new" else ' <span class="badge-mod">近期修改</span>' if sc == "modified" else ""
            sz = format_file_size(fi["size"])
            tree_html += f'<div class="tree-file {sc}"><span class="tf-name">{fi["name"]}{badge}</span>'
            tree_html += f'<span class="tf-size">{sz}</span><span class="tf-time">{fi["mtime_str"]}</span></div>'
        tree_html += '</div></div>'

    # Timeline HTML (recent 30 changes)
    timeline_html = ""
    for ch in sys_state["recent_changes"][:30]:
        sc = ch["status"]
        label = "新增" if sc == "new" else "修改" if sc == "modified" else ""
        badge_cls = "badge-new" if sc == "new" else "badge-mod" if sc == "modified" else ""
        badge_html = f'<span class="{badge_cls}">{label}</span>' if label else ""
        timeline_html += f'<div class="tl-item {sc}">'
        timeline_html += f'<span class="tl-time">{ch["mtime_str"]}</span>'
        timeline_html += f'{badge_html}'
        timeline_html += f'<span class="tl-icon">{ch.get("icon", "📄")}</span>'
        timeline_html += f'<span class="tl-name">{ch["name"]}</span>'
        timeline_html += f'<span class="tl-cat">{ch["category"]}</span>'
        timeline_html += '</div>\n'
    if not timeline_html:
        timeline_html = '<div class="empty">暂无文件变更记录</div>'

    # ── Conversation Intelligence HTML ──
    conv_meta = sys_state.get("conv_meta", {})
    conv_size_mb = conv_meta.get("total_size_mb", 0)
    conv_oldest = conv_meta.get("oldest")
    conv_newest = conv_meta.get("newest")
    conv_span = ""
    if conv_oldest and conv_newest:
        days = (conv_newest - conv_oldest).days
        conv_span = f"{conv_oldest.strftime('%Y-%m-%d')} ~ {conv_newest.strftime('%Y-%m-%d')}（{days} 天）"

    # Active processes HTML
    active_list = conv_meta.get("active", [])
    active_count = len(active_list)
    active_html = ""
    for ap in active_list:
        active_html += f'<div class="op-row"><span class="op-icon">🟢</span>'
        active_html += f'<span class="op-action">{ap["id"]}…</span>'
        active_html += f'<span class="op-detail">{ap["size_mb"]}MB</span>'
        active_html += f'<span class="op-time">最后活跃 {ap["last"]}</span></div>'
    if not active_html:
        active_html = '<div class="op-row"><span class="empty">当前无活跃进程</span></div>'

    # Top conversations by size
    top_conv_html = ""
    size_dist = conv_meta.get("size_dist", [])[:10]
    max_conv_sz = max((c["size_mb"] for c in size_dist), default=1) or 1
    for c in size_dist:
        pct = int((c["size_mb"] / max_conv_sz) * 100)
        active_tag = ' <span style="color:#a6e3a1;font-size:0.75em">● 活跃</span>' if c.get("active") else ""
        top_conv_html += f'<div class="bar-row"><span class="bar-label">{c["name"]}… ({c["date"]}){active_tag}</span>'
        top_conv_html += f'<div class="bar-track"><div class="bar-fill" style="width:{pct}%"></div></div>'
        top_conv_html += f'<span class="bar-count">{c["size_mb"]}MB</span></div>'

    # Activity by date
    by_week = conv_meta.get("by_week", {})
    activity_html = ""
    max_day_count = max(by_week.values(), default=1) or 1
    for date_key in sorted(by_week.keys())[-14:]:
        cnt = by_week[date_key]
        pct = int((cnt / max_day_count) * 100)
        activity_html += f'<div class="bar-row"><span class="bar-label">{date_key}</span>'
        activity_html += f'<div class="bar-track"><div class="bar-fill" style="width:{pct}%;background:linear-gradient(90deg,#cba6f7,#f38ba8)"></div></div>'
        activity_html += f'<span class="bar-count">{cnt}</span></div>'

    html = DASHBOARD_TEMPLATE.format(
        total_events=total,
        session_count=session_count,
        rule_count=rule_count,
        file_count=file_count,
        last_updated=last_updated,
        event_bars_html=event_bars_html,
        rules_html=rules_html,
        recent_html=recent_html,
        sessions_html=sessions_html,
        files_html=files_html,
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        # Evolution tracking data
        tree_html=tree_html,
        timeline_html=timeline_html,
        total_system_files=sys_state["total_files"],
        new_file_count=sys_state["new_count"],
        modified_file_count=sys_state["modified_count"],
        # Dynamic overview data
        skills_count=sys_state["skills_count"] or 23,
        mcp_count=sys_state["mcp_count"] or 7,
        workflows_count=sys_state["workflows_count"] or 11,
        memory_count=sys_state["memory_count"],
        conversation_count=sys_state["conversation_count"],
        # Conversation intelligence data
        implicit_count=sys_state.get("implicit_count", 0),
        conv_size_mb=conv_size_mb,
        conv_span=conv_span,
        top_conv_html=top_conv_html,
        activity_html=activity_html,
        active_count=active_count,
        active_html=active_html,
    )

    try:
        DASHBOARD_FILE.write_text(html, encoding="utf-8")
    except Exception as e:
        print(f"[Observatory] Dashboard write error: {e}", file=sys.stderr)


# ─── HTML Template ───────────────────────────────────────────────────────────

DASHBOARD_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI 观测站 — DevCatalyst 智能管理中心</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI',system-ui,-apple-system,sans-serif;background:#1e1e2e;color:#cdd6f4;padding:24px;min-height:100vh}}
a{{color:#89b4fa}}
.header{{display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;padding-bottom:16px;border-bottom:1px solid #313244}}
.header h1{{font-size:1.6em;font-weight:700}}.header h1 span{{color:#89b4fa}}
.header .meta{{text-align:right;font-size:0.85em;color:#6c7086}}
.tabs{{display:flex;gap:4px;margin-bottom:20px;background:#181825;border-radius:10px;padding:4px}}
.tab{{flex:1;padding:10px 16px;border:none;background:transparent;color:#6c7086;font-size:0.95em;cursor:pointer;border-radius:8px;transition:all 0.2s;font-weight:600}}
.tab:hover{{color:#cdd6f4}}.tab.active{{background:#313244;color:#89b4fa}}
.tab-content{{display:none}}.tab-content.active{{display:block}}
.stats-grid{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:20px}}
.stat-card{{background:#2a2a3c;border-radius:12px;padding:20px;text-align:center;border:1px solid #313244;transition:border-color 0.2s}}
.stat-card:hover{{border-color:#89b4fa}}.stat-value{{font-size:2.2em;font-weight:700;margin-bottom:4px}}
.stat-label{{font-size:0.85em;color:#6c7086;letter-spacing:1px}}
.c-blue .stat-value{{color:#89b4fa}}.c-green .stat-value{{color:#a6e3a1}}
.c-purple .stat-value{{color:#cba6f7}}.c-yellow .stat-value{{color:#f9e2af}}
.panels{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px}}
.panel{{background:#2a2a3c;border-radius:12px;padding:20px;border:1px solid #313244}}
.panel h2{{font-size:1.1em;margin-bottom:16px;color:#cdd6f4;display:flex;align-items:center;gap:8px}}
.panel h2::before{{content:'';display:inline-block;width:4px;height:18px;background:#89b4fa;border-radius:2px}}
.full-width{{grid-column:1/-1}}
.bar-row{{display:flex;align-items:center;gap:10px;margin-bottom:8px}}
.bar-label{{width:160px;font-size:0.85em;text-align:right;flex-shrink:0}}
.bar-track{{flex:1;height:20px;background:#313244;border-radius:4px;overflow:hidden}}
.bar-fill{{height:100%;background:linear-gradient(90deg,#89b4fa,#74c7ec);border-radius:4px;transition:width 0.5s ease;min-width:2px}}
.bar-count{{width:50px;font-size:0.85em;color:#6c7086;text-align:right}}
table{{width:100%;border-collapse:collapse;font-size:0.9em}}
th{{text-align:left;padding:8px 12px;border-bottom:2px solid #313244;color:#6c7086;font-weight:600;font-size:0.8em;letter-spacing:0.5px}}
td{{padding:8px 12px;border-bottom:1px solid #313244}}tr:hover td{{background:#313244}}
.num{{text-align:right;font-variant-numeric:tabular-nums;font-weight:600;color:#89b4fa}}
.empty{{text-align:center;color:#6c7086;padding:20px;font-style:italic}}
code{{background:#313244;padding:2px 6px;border-radius:4px;font-size:0.9em}}
.ops-container{{max-height:400px;overflow-y:auto;scrollbar-width:thin;scrollbar-color:#45475a #2a2a3c}}
.ops-container::-webkit-scrollbar{{width:6px}}.ops-container::-webkit-scrollbar-track{{background:#2a2a3c}}
.ops-container::-webkit-scrollbar-thumb{{background:#45475a;border-radius:3px}}
.op-row{{display:flex;align-items:center;gap:10px;padding:6px 8px;border-bottom:1px solid #313244;font-size:0.85em}}
.op-row:hover{{background:#313244}}.op-time{{color:#6c7086;font-family:monospace;flex-shrink:0;width:70px}}
.op-icon{{flex-shrink:0;width:24px;text-align:center}}
.op-action{{color:#cba6f7;flex-shrink:0;width:180px;font-family:monospace;font-size:0.9em}}
.op-detail{{color:#a6adc8;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1}}
.flow-diagram{{display:flex;align-items:center;justify-content:center;padding:20px 0}}
.flow-down{{display:flex;flex-direction:column;align-items:center;gap:8px}}
.flow-box{{background:#313244;border:1px solid #45475a;border-radius:8px;padding:12px 16px;text-align:center;min-width:140px}}
.flow-box.hl{{border-color:#89b4fa;background:#1e3a5f}}.flow-arrow{{color:#6c7086;font-size:1.5em}}
.flow-branch{{display:flex;gap:16px;justify-content:center}}.flow-branch .flow-box{{min-width:100px;font-size:0.85em}}
.hook-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-top:12px}}
.hook-item{{background:#313244;border-radius:6px;padding:8px 12px;font-size:0.8em;border-left:3px solid #45475a}}
.hook-item.pre{{border-left-color:#f9e2af}}.hook-item.post{{border-left-color:#a6e3a1}}
.hook-label{{color:#6c7086;font-size:0.75em;text-transform:uppercase}}
.kp{{display:flex;align-items:center;gap:8px;padding:6px 0;font-size:0.9em}}.kp .ic{{font-size:1.1em}}
.layer-stack{{display:flex;flex-direction:column;gap:8px;margin:12px 0}}
.layer{{display:flex;align-items:center;gap:12px;padding:14px 16px;border-radius:8px;background:#313244;border-left:4px solid #45475a}}
.layer-n{{font-weight:700;font-size:1.2em;min-width:30px;text-align:center}}
.layer-t{{font-weight:600;min-width:100px}}.layer-d{{color:#a6adc8;font-size:0.85em;flex:1}}
.l0{{border-left-color:#f38ba8}}.l0 .layer-n{{color:#f38ba8}}
.l1{{border-left-color:#f9e2af}}.l1 .layer-n{{color:#f9e2af}}
.l2{{border-left-color:#a6e3a1}}.l2 .layer-n{{color:#a6e3a1}}
.l3{{border-left-color:#89b4fa}}.l3 .layer-n{{color:#89b4fa}}
.cap-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.cap-card{{background:#313244;border-radius:8px;padding:14px;text-align:center}}
.cap-icon{{font-size:1.8em;margin-bottom:6px}}.cap-num{{font-size:1.6em;font-weight:700;color:#89b4fa}}
.cap-label{{font-size:0.8em;color:#6c7086;margin-top:2px}}
.wf-list{{display:grid;grid-template-columns:repeat(2,1fr);gap:8px}}
.wf-item{{background:#313244;border-radius:6px;padding:10px 14px;font-size:0.85em}}
.wf-item code{{color:#89b4fa}}.wf-item span{{color:#6c7086;margin-left:4px}}
.phil-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.phil-card{{background:#313244;border-radius:8px;padding:16px}}
.phil-title{{font-size:1.3em;margin-bottom:8px}}.phil-desc{{color:#a6adc8;font-size:0.85em}}
.tree-cat{{margin-bottom:8px}}
.tree-hdr{{background:#313244;border-radius:6px;padding:10px 14px;cursor:pointer;display:flex;align-items:center;gap:6px;font-size:0.9em;transition:background 0.2s}}
.tree-hdr:hover{{background:#3a3a4c}}
.tree-arrow{{color:#6c7086;font-size:0.7em;transition:transform 0.2s;display:inline-block}}
.tree-arrow.open{{transform:rotate(90deg)}}
.tree-cnt{{color:#6c7086;font-size:0.85em;margin-left:auto}}
.tree-body{{padding-left:24px;margin-top:4px}}
.tree-file{{display:flex;align-items:center;gap:8px;padding:5px 10px;border-left:2px solid #313244;font-size:0.83em;transition:background 0.2s}}
.tree-file:hover{{background:#313244}}
.tree-file.new{{border-left-color:#a6e3a1}}.tree-file.modified{{border-left-color:#f9e2af}}
.tf-name{{flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.tf-size{{color:#6c7086;font-size:0.85em;min-width:60px;text-align:right}}
.tf-time{{color:#6c7086;font-size:0.85em;min-width:90px;text-align:right;font-family:monospace}}
.badge-new{{background:#a6e3a1;color:#1e1e2e;padding:1px 6px;border-radius:4px;font-size:0.75em;font-weight:600;margin-left:4px}}
.badge-mod{{background:#f9e2af;color:#1e1e2e;padding:1px 6px;border-radius:4px;font-size:0.75em;font-weight:600;margin-left:4px}}
.tl-item{{display:flex;align-items:center;gap:8px;padding:6px 8px;border-bottom:1px solid #313244;font-size:0.85em}}
.tl-item:hover{{background:#313244}}
.tl-item.new{{border-left:3px solid #a6e3a1}}.tl-item.modified{{border-left:3px solid #f9e2af}}.tl-item.stable{{border-left:3px solid #45475a}}
.tl-time{{color:#6c7086;font-family:monospace;min-width:80px}}
.tl-icon{{min-width:20px;text-align:center}}
.tl-name{{font-weight:600;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.tl-cat{{color:#6c7086;font-size:0.85em;min-width:80px;text-align:right}}
.cmp-table{{width:100%;border-collapse:collapse;font-size:0.82em;margin-top:8px}}
.cmp-table th{{padding:8px 6px;border-bottom:2px solid #45475a;color:#89b4fa;font-weight:600;text-align:center;font-size:0.85em}}
.cmp-table th:first-child{{text-align:left;min-width:140px}}
.cmp-table td{{padding:6px;border-bottom:1px solid #313244;text-align:center}}
.cmp-table td:first-child{{text-align:left;font-weight:500}}
.cmp-table tr:hover td{{background:#313244}}
.st-yes{{color:#a6e3a1}}.st-no{{color:#f38ba8}}.st-part{{color:#f9e2af}}
.gap-card{{background:#313244;border-radius:8px;padding:14px 16px;border-left:4px solid #45475a;margin-bottom:8px}}
.gap-card.critical{{border-left-color:#f38ba8}}.gap-card.important{{border-left-color:#f9e2af}}.gap-card.leading{{border-left-color:#a6e3a1}}
.gap-title{{font-weight:600;margin-bottom:4px;display:flex;align-items:center;gap:6px}}
.gap-desc{{color:#a6adc8;font-size:0.85em}}
.gap-tag{{font-size:0.7em;padding:2px 6px;border-radius:4px;font-weight:600}}
.gap-tag.red{{background:#f38ba8;color:#1e1e2e}}.gap-tag.yellow{{background:#f9e2af;color:#1e1e2e}}.gap-tag.green{{background:#a6e3a1;color:#1e1e2e}}
.roadmap-item{{display:flex;align-items:center;gap:12px;padding:10px 14px;background:#313244;border-radius:6px;margin-bottom:6px;font-size:0.85em}}
.roadmap-phase{{min-width:70px;font-weight:700;font-size:0.8em;text-transform:uppercase;letter-spacing:0.5px}}
.roadmap-phase.p1{{color:#f38ba8}}.roadmap-phase.p2{{color:#f9e2af}}.roadmap-phase.p3{{color:#a6e3a1}}
.evo-flow{{display:flex;align-items:center;justify-content:center;gap:8px;flex-wrap:wrap;padding:16px 0}}
.evo-node{{background:#313244;border:2px solid #45475a;border-radius:12px;padding:12px 16px;text-align:center;min-width:100px;transition:border-color 0.3s}}
.evo-node:hover{{border-color:#89b4fa}}
.evo-node .evo-icon{{font-size:1.5em;margin-bottom:4px}}
.evo-node .evo-label{{font-size:0.8em;font-weight:600}}
.evo-arrow{{color:#45475a;font-size:1.2em}}
.evo-node.active{{border-color:#a6e3a1;box-shadow:0 0 12px rgba(166,227,161,0.2)}}
.profile-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}
.profile-item{{background:#313244;border-radius:8px;padding:12px;text-align:center}}
.profile-item .pi-val{{font-size:1.5em;font-weight:700;color:#89b4fa}}
.profile-item .pi-label{{font-size:0.8em;color:#6c7086;margin-top:4px}}
.footer{{text-align:center;padding:20px;color:#45475a;font-size:0.8em;margin-top:16px}}
@media(max-width:900px){{
    .stats-grid{{grid-template-columns:repeat(2,1fr)}}.panels{{grid-template-columns:1fr}}
    .cap-grid{{grid-template-columns:repeat(2,1fr)}}.hook-grid{{grid-template-columns:repeat(2,1fr)}}
    .wf-list{{grid-template-columns:1fr}}.phil-grid{{grid-template-columns:1fr}}
}}
</style>
</head>
<body>
<div class="header">
    <h1>&#128301; AI <span>观测站</span></h1>
    <div class="meta">
        <div>DevCatalyst 智能管理中心</div>
        <div>最后更新: {last_updated}</div>
    </div>
</div>

<div class="tabs">
    <button class="tab active" onclick="switchTab('monitor',this)">&#128202; 实时监控</button>
    <button class="tab" onclick="switchTab('arch',this)">&#9881; 系统架构</button>
    <button class="tab" onclick="switchTab('overview',this)">&#127760; 全景总览</button>
    <button class="tab" onclick="switchTab('evo',this)">&#128256; 进化追踪</button>
    <button class="tab" onclick="switchTab('bench',this)">&#127942; 架构对标</button>
    <button class="tab" onclick="switchTab('intel',this)">&#129504; 智能进化</button>
</div>

<!-- ═══ Tab 1: 实时监控 ═══ -->
<div id="tab-monitor" class="tab-content active">

<div class="stats-grid">
    <div class="stat-card c-green">
        <div class="stat-value">{active_count}</div>
        <div class="stat-label">🟢 活跃进程</div>
    </div>
    <div class="stat-card c-blue">
        <div class="stat-value">{total_events}</div>
        <div class="stat-label">事件总数</div>
    </div>
    <div class="stat-card c-purple">
        <div class="stat-value">{rule_count}</div>
        <div class="stat-label">规则追踪</div>
    </div>
    <div class="stat-card c-yellow">
        <div class="stat-value">{file_count}</div>
        <div class="stat-label">涉及文件</div>
    </div>
</div>

<div class="panels">
    <div class="panel">
        <h2>当前活跃进程</h2>
        <p style="color:#6c7086;font-size:0.8em;margin-bottom:8px">最近 10 分钟有活动的 Cascade 对话</p>
        <div class="ops-container" style="max-height:200px">
            {active_html}
        </div>
    </div>
    <div class="panel">
        <h2>事件分布</h2>
        {event_bars_html}
    </div>
</div>

<div class="panels">
    <div class="panel">
        <h2>规则触发排行</h2>
        <div style="max-height:300px;overflow-y:auto">
        <table>
            <thead><tr><th>规则</th><th style="text-align:right">触发次数</th></tr></thead>
            <tbody>{rules_html}</tbody>
        </table>
        </div>
    </div>
    <div class="panel">
        <h2>最近操作</h2>
        <div class="ops-container">
            {recent_html}
        </div>
    </div>
</div>

<div class="panels">
    <div class="panel">
        <h2>对话会话</h2>
        <div style="max-height:300px;overflow-y:auto">
        <table>
            <thead><tr><th>ID</th><th style="text-align:right">事件数</th><th>开始时间</th><th>最后活跃</th></tr></thead>
            <tbody>{sessions_html}</tbody>
        </table>
        </div>
    </div>
    <div class="panel">
        <h2>高频文件</h2>
        <div style="max-height:300px;overflow-y:auto">
        <table>
            <thead><tr><th>文件</th><th style="text-align:right">访问次数</th></tr></thead>
            <tbody>{files_html}</tbody>
        </table>
        </div>
    </div>
</div>

</div>

<!-- ═══ Tab 2: 系统架构 ═══ -->
<div id="tab-arch" class="tab-content">

<div class="panels">
    <div class="panel full-width">
        <h2>运作原理：事件驱动式监控</h2>
        <p style="color:#a6adc8;margin-bottom:16px;font-size:0.9em">
            Observatory <strong>不是</strong>后台守护进程，<strong>不是</strong>定时轮询，<strong>不是</strong>自循环机制。
            它利用 Windsurf IDE 内置的 <strong style="color:#89b4fa">Cascade Hooks</strong> 机制 ——
            每当 AI 执行任何操作时，IDE 自动将事件数据通过 stdin 管道传给 Python 脚本，实现零开销的全链路监控。
        </p>
        <div class="flow-diagram">
            <div class="flow-down">
                <div class="flow-box">&#128100; 用户发送消息</div>
                <div class="flow-arrow">&#8595;</div>
                <div class="flow-box hl">&#129302; Cascade AI 思考并执行操作<br><small style="color:#6c7086">读文件 / 改代码 / 跑命令 / 用MCP</small></div>
                <div class="flow-arrow">&#8595;</div>
                <div class="flow-box" style="border-color:#f9e2af">&#127919; Windsurf IDE 自动触发 Hook<br><small style="color:#6c7086">将操作的 JSON 数据通过 stdin 传入脚本</small></div>
                <div class="flow-arrow">&#8595;</div>
                <div class="flow-box hl">&#128640; hook_logger.py 处理事件</div>
                <div class="flow-arrow">&#8595;</div>
                <div class="flow-branch">
                    <div class="flow-box">&#128196; 日志记录<br><small style="color:#6c7086">JSONL 格式</small></div>
                    <div class="flow-box">&#128200; 统计更新<br><small style="color:#6c7086">JSON 格式</small></div>
                    <div class="flow-box" style="border-color:#a6e3a1">&#127912; 仪表盘<br><small style="color:#6c7086">HTML 自动刷新</small></div>
                </div>
            </div>
        </div>
    </div>
</div>

<div class="panels">
    <div class="panel">
        <h2>与其他方案的区别</h2>
        <div class="kp"><span class="ic">&#10060;</span> <strong>不是</strong>后台常驻进程 —— 无额外内存/CPU 消耗</div>
        <div class="kp"><span class="ic">&#10060;</span> <strong>不是</strong>定时轮询（cron/timer）—— 不会错过任何事件</div>
        <div class="kp"><span class="ic">&#10060;</span> <strong>不是</strong>自循环机制（如 Lobster AI）—— 无需独立服务</div>
        <div class="kp"><span class="ic">&#9989;</span> <strong>是</strong> IDE 原生事件钩子 —— 零开销，100% 事件覆盖</div>
        <div class="kp"><span class="ic">&#9989;</span> <strong>是</strong>被动触发 —— AI 操作时自动激活，不操作时完全静默</div>
        <div class="kp"><span class="ic">&#9989;</span> <strong>是</strong>纯 Python —— 无需安装依赖，跨平台兼容</div>
    </div>
    <div class="panel">
        <h2>11 个监控点</h2>
        <div class="hook-grid">
            <div class="hook-item pre"><div class="hook-label">前置拦截</div>读取文件</div>
            <div class="hook-item post"><div class="hook-label">后置记录</div>读取文件</div>
            <div class="hook-item pre"><div class="hook-label">前置拦截</div>修改代码</div>
            <div class="hook-item post"><div class="hook-label">后置记录</div>修改代码</div>
            <div class="hook-item pre"><div class="hook-label">前置拦截</div>执行命令</div>
            <div class="hook-item post"><div class="hook-label">后置记录</div>执行命令</div>
            <div class="hook-item pre"><div class="hook-label">前置拦截</div>MCP 工具</div>
            <div class="hook-item post"><div class="hook-label">后置记录</div>MCP 工具</div>
            <div class="hook-item pre"><div class="hook-label">审计</div>用户消息</div>
            <div class="hook-item post"><div class="hook-label">分析</div>AI 回复</div>
            <div class="hook-item post"><div class="hook-label">记录</div>工作树创建</div>
        </div>
    </div>
</div>

<div class="panels">
    <div class="panel full-width">
        <h2>数据流与文件</h2>
        <table>
            <thead><tr><th>文件</th><th>格式</th><th>更新时机</th><th>用途</th></tr></thead>
            <tbody>
                <tr><td><code>cascade_log.jsonl</code></td><td>JSON Lines</td><td>每个 Hook 事件</td><td>完整事件日志（自动轮转，保留最近 10000 条）</td></tr>
                <tr><td><code>stats.json</code></td><td>JSON</td><td>每个 Hook 事件</td><td>累计统计：事件计数、会话、规则触发、文件访问</td></tr>
                <tr><td><code>dashboard.html</code></td><td>HTML</td><td>每次 AI 回复后</td><td>可视化仪表盘（浏览器打开，每 30 秒自动刷新）</td></tr>
                <tr><td><code>hooks.json</code></td><td>JSON</td><td>手动部署</td><td>Hook 配置（已部署到 ~/.codeium/windsurf/）</td></tr>
            </tbody>
        </table>
    </div>
</div>

</div>

<!-- ═══ Tab 3: 全景总览 ═══ -->
<div id="tab-overview" class="tab-content">

<div class="panels">
    <div class="panel full-width">
        <h2>DevCatalyst 四层架构</h2>
        <p style="color:#a6adc8;margin-bottom:16px;font-size:0.9em">
            DevCatalyst 是整台电脑的 AI 智能管理中心。通过四层架构管理所有项目的 AI 配置、规则、经验和监控。
        </p>
        <div class="layer-stack">
            <div class="layer l3">
                <div class="layer-n">L3</div>
                <div class="layer-t">管理中心</div>
                <div class="layer-d">项目注册表 + 经验归档 + 规则仓库 + AI 观测站 + 工作流引擎</div>
            </div>
            <div class="layer l2">
                <div class="layer-n">L2</div>
                <div class="layer-t">项目层</div>
                <div class="layer-d">soul.md（人机分工/自律进化）+ execution-engine.md（终端/命令/错误处理）&rarr; 每个项目独立配置</div>
            </div>
            <div class="layer l1">
                <div class="layer-n">L1</div>
                <div class="layer-t">全局层</div>
                <div class="layer-d">GLOBAL_RULES.md &mdash; PREDICT 决策框架 / ESCALATION 升级 / 预测性补全 / 核心信念 / 代码准则</div>
            </div>
            <div class="layer l0">
                <div class="layer-n">L0</div>
                <div class="layer-t">内核</div>
                <div class="layer-d">kernel.md &mdash; 3 条元规则（预算制 / 变更协议 / AI 不盲加规则），永不修改</div>
            </div>
        </div>
    </div>
</div>

<div class="panels">
    <div class="panel full-width">
        <h2>能力矩阵</h2>
        <div class="cap-grid">
            <div class="cap-card"><div class="cap-icon">&#129504;</div><div class="cap-num">{skills_count}</div><div class="cap-label">全局 Skills</div></div>
            <div class="cap-card"><div class="cap-icon">&#128295;</div><div class="cap-num">{mcp_count}</div><div class="cap-label">MCP 服务器</div></div>
            <div class="cap-card"><div class="cap-icon">&#128203;</div><div class="cap-num">{workflows_count}</div><div class="cap-label">工作流</div></div>
            <div class="cap-card"><div class="cap-icon">&#128301;</div><div class="cap-num">11</div><div class="cap-label">监控钩子</div></div>
            <div class="cap-card"><div class="cap-icon">&#128190;</div><div class="cap-num">{memory_count}</div><div class="cap-label">持久记忆</div></div>
            <div class="cap-card"><div class="cap-icon">&#128172;</div><div class="cap-num">{conversation_count}</div><div class="cap-label">对话历史</div></div>
        </div>
    </div>
</div>

<div class="panels">
    <div class="panel">
        <h2>三大管理工作流</h2>
        <div class="layer-stack">
            <div class="layer l3" style="cursor:default">
                <div class="layer-n" style="font-size:1.4em">&#127793;</div>
                <div class="layer-t"><code>/harvest</code></div>
                <div class="layer-d">从指定项目收割经验 &rarr; 写入 EXPERIENCE_LOG.md</div>
            </div>
            <div class="layer l1" style="cursor:default">
                <div class="layer-n" style="font-size:1.4em">&#129504;</div>
                <div class="layer-t"><code>/evolve</code></div>
                <div class="layer-d">审查经验 + 规则编译 + 人机协作决策 &rarr; 固化到模板</div>
            </div>
            <div class="layer l2" style="cursor:default">
                <div class="layer-n" style="font-size:1.4em">&#128259;</div>
                <div class="layer-t"><code>/sync</code></div>
                <div class="layer-d">将更新同步部署到所有已注册项目</div>
            </div>
        </div>
    </div>
    <div class="panel">
        <h2>所有工作流</h2>
        <div class="wf-list">
            <div class="wf-item"><code>/harvest</code> <span>经验收割</span></div>
            <div class="wf-item"><code>/evolve</code> <span>规则进化</span></div>
            <div class="wf-item"><code>/sync</code> <span>同步部署</span></div>
            <div class="wf-item"><code>/observatory</code> <span>监控运维</span></div>
            <div class="wf-item"><code>/health-check</code> <span>健康检查</span></div>
            <div class="wf-item"><code>/review</code> <span>代码审查</span></div>
            <div class="wf-item"><code>/test</code> <span>测试验证</span></div>
            <div class="wf-item"><code>/refactor</code> <span>重构优化</span></div>
            <div class="wf-item"><code>/doc</code> <span>文档生成</span></div>
            <div class="wf-item"><code>/optimize</code> <span>性能优化</span></div>
            <div class="wf-item"><code>/debug-escalation</code> <span>调试升级</span></div>
        </div>
    </div>
</div>

<div class="panels">
    <div class="panel full-width">
        <h2>核心哲学</h2>
        <div class="phil-grid">
            <div class="phil-card">
                <div class="phil-title">&#128300; 上下文隔离</div>
                <div class="phil-desc">AI 在具体项目中无暇改进元规则，需要独立管理工作区</div>
            </div>
            <div class="phil-card">
                <div class="phil-title">&#128260; 通用 + 特化</div>
                <div class="phil-desc">一套规则模板融化成任何项目想要的模样</div>
            </div>
            <div class="phil-card">
                <div class="phil-title">&#129309; 人机协作进化</div>
                <div class="phil-desc">人参与决策 + 成熟工具链 + 跨项目视野，比全自动更优</div>
            </div>
        </div>
    </div>
</div>

</div>

<!-- ═══ Tab 4: 进化追踪 ═══ -->
<div id="tab-evo" class="tab-content">

<div class="stats-grid" style="grid-template-columns:repeat(3,1fr)">
    <div class="stat-card c-green">
        <div class="stat-value">{new_file_count}</div>
        <div class="stat-label">24h 内新增</div>
    </div>
    <div class="stat-card c-yellow">
        <div class="stat-value">{modified_file_count}</div>
        <div class="stat-label">7 天内修改</div>
    </div>
    <div class="stat-card c-blue">
        <div class="stat-value">{total_system_files}</div>
        <div class="stat-label">系统总文件</div>
    </div>
</div>

<div class="panels">
    <div class="panel">
        <h2>系统架构树</h2>
        <p style="color:#6c7086;font-size:0.8em;margin-bottom:12px">点击分类展开查看文件 &middot; <span class="badge-new">新</span> = 24h内 &middot; <span class="badge-mod">改</span> = 7天内</p>
        {tree_html}
    </div>
    <div class="panel">
        <h2>变更时间线</h2>
        <div class="ops-container">
            {timeline_html}
        </div>
    </div>
</div>

</div>

<!-- ═══ Tab 6: 智能进化 ═══ -->
<div id="tab-intel" class="tab-content">

<div class="stats-grid">
    <div class="stat-card c-purple"><div class="stat-value">{conversation_count}</div><div class="stat-label">对话总数</div></div>
    <div class="stat-card c-blue"><div class="stat-value">{conv_size_mb}MB</div><div class="stat-label">对话数据量</div></div>
    <div class="stat-card c-green"><div class="stat-value">{memory_count}</div><div class="stat-label">显式记忆</div></div>
    <div class="stat-card c-yellow"><div class="stat-value">{implicit_count}</div><div class="stat-label">隐式上下文</div></div>
</div>

<div class="panels">
    <div class="panel full-width">
        <h2>自进化循环架构</h2>
        <p style="color:#a6adc8;font-size:0.85em;margin-bottom:8px">每次对话都是学习机会，每条经验都能固化为规则</p>
        <div class="evo-flow">
            <div class="evo-node active"><div class="evo-icon">&#128172;</div><div class="evo-label">用户对话</div></div>
            <div class="evo-arrow">→</div>
            <div class="evo-node"><div class="evo-icon">&#128270;</div><div class="evo-label">Hooks 采集</div></div>
            <div class="evo-arrow">→</div>
            <div class="evo-node"><div class="evo-icon">&#129504;</div><div class="evo-label">模式识别</div></div>
            <div class="evo-arrow">→</div>
            <div class="evo-node"><div class="evo-icon">&#128220;</div><div class="evo-label">经验提炼</div></div>
            <div class="evo-arrow">→</div>
            <div class="evo-node"><div class="evo-icon">&#9989;</div><div class="evo-label">审查固化</div></div>
            <div class="evo-arrow">→</div>
            <div class="evo-node"><div class="evo-icon">&#128640;</div><div class="evo-label">规则升级</div></div>
            <div class="evo-arrow">↻</div>
        </div>
    </div>
</div>

<div class="panels">
    <div class="panel">
        <h2>对话规模分布（Top 10）</h2>
        <p style="color:#6c7086;font-size:0.8em;margin-bottom:8px">按数据量排序，大对话 = 深度学习机会</p>
        {top_conv_html}
    </div>
    <div class="panel">
        <h2>对话活动时间线</h2>
        <p style="color:#6c7086;font-size:0.8em;margin-bottom:8px">每日对话数量（近 14 天）</p>
        {activity_html}
    </div>
</div>

<div class="panels">
    <div class="panel full-width">
        <h2>数据资产总览</h2>
        <p style="color:#a6adc8;font-size:0.85em;margin-bottom:12px">对话范围：{conv_span}</p>
        <div class="profile-grid">
            <div class="profile-item"><div class="pi-val">{conversation_count}</div><div class="pi-label">&#128172; 对话记录</div></div>
            <div class="profile-item"><div class="pi-val">{memory_count}</div><div class="pi-label">&#129504; 显式记忆</div></div>
            <div class="profile-item"><div class="pi-val">{implicit_count}</div><div class="pi-label">&#128065; 隐式上下文</div></div>
            <div class="profile-item"><div class="pi-val">{skills_count}</div><div class="pi-label">&#129520; 已部署技能</div></div>
            <div class="profile-item"><div class="pi-val">{workflows_count}</div><div class="pi-label">&#128260; 工作流</div></div>
            <div class="profile-item"><div class="pi-val">{mcp_count}</div><div class="pi-label">&#128295; MCP 服务器</div></div>
        </div>
    </div>
</div>

<div class="panels">
    <div class="panel">
        <h2>进化工作流</h2>
        <div class="gap-card leading">
            <div class="gap-title"><span class="gap-tag green">已部署</span> /harvest 经验收割</div>
            <div class="gap-desc">从指定项目提炼有价值的经验，写入经验日志</div>
        </div>
        <div class="gap-card leading">
            <div class="gap-title"><span class="gap-tag green">已部署</span> /evolve-auto 自动进化</div>
            <div class="gap-desc">周期性扫描对话记录，提炼用户习惯，自动优化规则</div>
        </div>
        <div class="gap-card leading">
            <div class="gap-title"><span class="gap-tag green">已部署</span> /onboard 新项目引导</div>
            <div class="gap-desc">一键配置项目专属规则、技能、工作流</div>
        </div>
        <div class="gap-card leading">
            <div class="gap-title"><span class="gap-tag green">已部署</span> /blueprint 蓝图模式</div>
            <div class="gap-desc">研究→规划→审查→执行→验证，防止 AI 幻觉</div>
        </div>
    </div>
    <div class="panel">
        <h2>智能进化机制说明</h2>
        <div class="gap-card important">
            <div class="gap-title"><span class="gap-tag yellow">核心</span> 对话智能引擎</div>
            <div class="gap-desc">每次对话通过 Hooks 采集数据→分析用户习惯→提炼可固化经验→审查后升级规则。无需用户手动管理。</div>
        </div>
        <div class="gap-card important">
            <div class="gap-title"><span class="gap-tag yellow">核心</span> 用户画像系统</div>
            <div class="gap-desc">AI 自动学习用户偏好（代码风格、沟通方式、工作节奏），塑造成符合用户习惯的形态。</div>
        </div>
        <div class="gap-card important">
            <div class="gap-title"><span class="gap-tag yellow">核心</span> 跨项目知识循环</div>
            <div class="gap-desc">项目 A 的经验可以反哺项目 B。通过 harvest→evolve→sync 三步走，实现全局知识流动。</div>
        </div>
        <div class="gap-card important">
            <div class="gap-title"><span class="gap-tag yellow">核心</span> 新用户冷启动</div>
            <div class="gap-desc">前 10 次对话积极学习→生成初始画像→用户确认→正式启用个性化配置。</div>
        </div>
    </div>
</div>

</div>

<!-- ═══ Tab 5: 架构对标 ═══ -->
<div id="tab-bench" class="tab-content">

<div class="panels">
    <div class="panel full-width">
        <h2>规则系统对比</h2>
        <p style="color:#a6adc8;font-size:0.85em;margin-bottom:12px">基于 2026-02 对业界 5 大 AI 开发平台的深度研究</p>
        <table class="cmp-table">
            <thead><tr><th>能力</th><th>DevCatalyst</th><th>Claude Code</th><th>Cursor</th><th>Antigravity</th></tr></thead>
            <tbody>
                <tr><td>分层架构</td><td class="st-yes">✅ L0-L3 四层</td><td class="st-yes">✅ 用户/项目/本地</td><td class="st-yes">✅ Team/Project/User</td><td class="st-part">⚠️ 单层</td></tr>
                <tr><td>字符预算制</td><td class="st-yes">✅ 6000字符</td><td class="st-no">❌</td><td class="st-no">❌</td><td class="st-no">❌</td></tr>
                <tr><td>模块化规则文件</td><td class="st-no">❌ 单文件</td><td class="st-yes">✅ .claude/rules/</td><td class="st-yes">✅ .cursor/rules/</td><td class="st-no">❌</td></tr>
                <tr><td>路径条件激活</td><td class="st-no">❌</td><td class="st-yes">✅ glob patterns</td><td class="st-yes">✅ globs+alwaysApply</td><td class="st-no">❌</td></tr>
                <tr><td>规则变更协议</td><td class="st-yes">✅ 路由→冲突→预算</td><td class="st-no">❌</td><td class="st-no">❌</td><td class="st-no">❌</td></tr>
                <tr><td>远程规则同步</td><td class="st-no">❌</td><td class="st-part">⚠️ symlinks</td><td class="st-yes">✅ GitHub Remote</td><td class="st-no">❌</td></tr>
            </tbody>
        </table>
    </div>
</div>

<div class="panels">
    <div class="panel full-width">
        <h2>记忆与上下文对比</h2>
        <table class="cmp-table">
            <thead><tr><th>能力</th><th>DevCatalyst</th><th>Claude Code</th><th>Cursor</th><th>Antigravity</th></tr></thead>
            <tbody>
                <tr><td>持久记忆</td><td class="st-yes">✅ {memory_count}条</td><td class="st-yes">✅ MEMORY.md+auto</td><td class="st-part">⚠️ Notepad</td><td class="st-yes">✅ brain/</td></tr>
                <tr><td>自动记忆</td><td class="st-part">⚠️ 依赖AI主动</td><td class="st-yes">✅ 自动保存</td><td class="st-no">❌</td><td class="st-yes">✅ 自动学习</td></tr>
                <tr><td>上下文压缩</td><td class="st-no">❌</td><td class="st-yes">✅ /compact</td><td class="st-no">❌</td><td class="st-part">⚠️ 隐式</td></tr>
                <tr><td>结构化笔记</td><td class="st-no">❌</td><td class="st-yes">✅ NOTES.md/TODO</td><td class="st-no">❌</td><td class="st-no">❌</td></tr>
                <tr><td>蓝图/计划模式</td><td class="st-no">❌</td><td class="st-no">❌</td><td class="st-no">❌</td><td class="st-yes">✅ Plan-Review-Execute</td></tr>
            </tbody>
        </table>
    </div>
</div>

<div class="panels">
    <div class="panel full-width">
        <h2>工具与监控对比</h2>
        <table class="cmp-table">
            <thead><tr><th>能力</th><th>DevCatalyst</th><th>Claude Code</th><th>Cursor</th><th>Antigravity</th></tr></thead>
            <tbody>
                <tr><td>Skills/技能</td><td class="st-yes">✅ {skills_count}个</td><td class="st-yes">✅ skills+子代理</td><td class="st-yes">✅ Agent Skills</td><td class="st-no">❌</td></tr>
                <tr><td>MCP 服务器</td><td class="st-yes">✅ {mcp_count}个</td><td class="st-yes">✅ 原生支持</td><td class="st-yes">✅ 原生支持</td><td class="st-no">❌</td></tr>
                <tr><td>Hooks 事件</td><td class="st-yes">✅ 11个</td><td class="st-yes">✅ hooks</td><td class="st-no">❌</td><td class="st-no">❌</td></tr>
                <tr><td>可视化仪表盘</td><td class="st-yes">✅ 5Tab HTML</td><td class="st-no">❌</td><td class="st-part">⚠️ Team面板</td><td class="st-no">❌</td></tr>
                <tr><td>进化追踪</td><td class="st-yes">✅ 文件变更时间线</td><td class="st-no">❌</td><td class="st-no">❌</td><td class="st-no">❌</td></tr>
                <tr><td>经验进化管道</td><td class="st-yes">✅ harvest→evolve→sync</td><td class="st-no">❌</td><td class="st-no">❌</td><td class="st-no">❌</td></tr>
            </tbody>
        </table>
    </div>
</div>

<div class="panels">
    <div class="panel">
        <h2>差距分析</h2>
        <div class="gap-card critical">
            <div class="gap-title"><span class="gap-tag red">缺失</span> 模块化规则文件</div>
            <div class="gap-desc">Claude Code 用 .claude/rules/ 按主题拆分，Cursor 用 .mdc 条件激活。我们是单文件，维护成本高。</div>
        </div>
        <div class="gap-card critical">
            <div class="gap-title"><span class="gap-tag red">缺失</span> 结构化进度追踪 (Scratchpad)</div>
            <div class="gap-desc">Anthropic 推荐 AI 主动维护 NOTES.md，确保长周期任务的连贯性。</div>
        </div>
        <div class="gap-card critical">
            <div class="gap-title"><span class="gap-tag red">缺失</span> 蓝图模式 (Plan-Review-Execute)</div>
            <div class="gap-desc">Antigravity 的研究→计划→审查→执行，减少 AI 幻觉和架构错误。</div>
        </div>
        <div class="gap-card important">
            <div class="gap-title"><span class="gap-tag yellow">部分</span> 上下文压缩策略</div>
            <div class="gap-desc">Claude Code 的 /compact 自动压缩会话，保留关键信息。我们缺少这种机制。</div>
        </div>
        <div class="gap-card important">
            <div class="gap-title"><span class="gap-tag yellow">部分</span> 路径条件激活</div>
            <div class="gap-desc">规则根据当前操作的文件路径自动激活/停用，减少上下文浪费。</div>
        </div>
    </div>
    <div class="panel">
        <h2>领先优势</h2>
        <div class="gap-card leading">
            <div class="gap-title"><span class="gap-tag green">独创</span> 四层架构 + 预算制</div>
            <div class="gap-desc">比所有竞品更系统化的分层 + 6000字符防膨胀，Anthropic 论文验证了这个方向。</div>
        </div>
        <div class="gap-card leading">
            <div class="gap-title"><span class="gap-tag green">独创</span> 变更协议（路由→冲突→预算）</div>
            <div class="gap-desc">业界唯一的规则治理流程，防止规则无序增长。</div>
        </div>
        <div class="gap-card leading">
            <div class="gap-title"><span class="gap-tag green">独创</span> AI 观测站监控系统</div>
            <div class="gap-desc">业界唯一的 AI 行为全链路可视化监控，包含进化追踪。</div>
        </div>
        <div class="gap-card leading">
            <div class="gap-title"><span class="gap-tag green">独创</span> 经验进化管道</div>
            <div class="gap-desc">harvest→evolve→sync 三步走，跨项目知识循环，无竞品拥有。</div>
        </div>
        <div class="gap-card leading">
            <div class="gap-title"><span class="gap-tag green">独创</span> Skills + MCP + Hooks 三位一体</div>
            <div class="gap-desc">{skills_count} Skills + {mcp_count} MCP + 11 Hooks 全量部署，最完整的工具链。</div>
        </div>
    </div>
</div>

<div class="panels">
    <div class="panel full-width">
        <h2>升级路线图</h2>
        <div class="roadmap-item"><span class="roadmap-phase p1">Phase 1</span><span>新增 /blueprint 工作流（Plan-Review-Execute 模式）</span></div>
        <div class="roadmap-item"><span class="roadmap-phase p1">Phase 1</span><span>规则中加入 Scratchpad 指令（结构化进度追踪）</span></div>
        <div class="roadmap-item"><span class="roadmap-phase p1">Phase 1</span><span>上下文压缩策略文档化（参考 Anthropic 最佳实践）</span></div>
        <div class="roadmap-item"><span class="roadmap-phase p2">Phase 2</span><span>规则模块化拆分试点（参考 .claude/rules/ 模式）</span></div>
        <div class="roadmap-item"><span class="roadmap-phase p2">Phase 2</span><span>Hook 增强：危险命令拦截 + 自动记忆提取</span></div>
        <div class="roadmap-item"><span class="roadmap-phase p3">Phase 3</span><span>路径条件激活系统（规则按文件类型自动启用）</span></div>
        <div class="roadmap-item"><span class="roadmap-phase p3">Phase 3</span><span>子代理模式探索 + 规则效果分析</span></div>
    </div>
</div>

</div>

<div class="footer">
    生成时间: {generated_at} &mdash; 手动刷新（F5）保持当前 Tab &mdash; AI 观测站 v5.0
</div>

<script>
function switchTab(id,btn){{
    document.querySelectorAll('.tab-content').forEach(function(e){{e.classList.remove('active')}});
    document.querySelectorAll('.tab').forEach(function(e){{e.classList.remove('active')}});
    document.getElementById('tab-'+id).classList.add('active');
    btn.classList.add('active');
    location.hash=id;
}}
function toggleTree(hdr){{
    var body=hdr.nextElementSibling;
    var arrow=hdr.querySelector('.tree-arrow');
    if(body.style.display==='none'){{body.style.display='block';arrow.classList.add('open');}}
    else{{body.style.display='none';arrow.classList.remove('open');}}
}}
// 页面加载时恢复上次 Tab
(function(){{
    var h=location.hash.replace('#','');
    if(h){{var el=document.getElementById('tab-'+h);if(el){{
        document.querySelectorAll('.tab-content').forEach(function(e){{e.classList.remove('active')}});
        document.querySelectorAll('.tab').forEach(function(e){{e.classList.remove('active')}});
        el.classList.add('active');
        var tabs=document.querySelectorAll('.tab');
        var names=['monitor','arch','overview','evo','bench','intel'];
        var idx=names.indexOf(h);if(idx>=0&&tabs[idx])tabs[idx].classList.add('active');
    }}}}
}})();
</script>
</body>
</html>"""


# ─── Main Entry Point ────────────────────────────────────────────────────────

def main():
    """Main entry point — called by Windsurf hooks or manually."""
    # Manual dashboard regeneration mode
    if len(sys.argv) > 1 and sys.argv[1] == "--dashboard":
        stats = load_stats()
        generate_dashboard(stats)
        print(f"[Observatory] Dashboard regenerated → {DASHBOARD_FILE}")
        return

    # Normal hook mode: read JSON from stdin
    try:
        input_data = sys.stdin.read()
        data = json.loads(input_data)
    except json.JSONDecodeError as e:
        print(f"[Observatory] JSON parse error: {e}", file=sys.stderr)
        sys.exit(0)  # Never block Cascade on parse errors
    except Exception as e:
        print(f"[Observatory] Input error: {e}", file=sys.stderr)
        sys.exit(0)

    event = data.get("agent_action_name", "unknown")

    # Log the event
    log_event(data)

    # Update statistics
    stats = update_stats(data)

    # Regenerate dashboard: always if missing, otherwise only on cascade response
    should_gen = (event == "post_cascade_response") or (not DASHBOARD_FILE.exists())
    if should_gen:
        try:
            generate_dashboard(stats)
        except Exception as e:
            print(f"[Observatory] Dashboard error: {e}", file=sys.stderr)

    # Brief output for Cascade terminal
    print(f"[Observatory] {event} | total:{stats['total_events']}")


if __name__ == "__main__":
    main()
