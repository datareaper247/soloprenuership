---
last_updated: 2026-02-23
---

# Development Environment

## System
- **Machine**: M1 Mac arm64, macOS 15.7 Sequoia
- **Shell**: zsh
- **Package manager**: Homebrew 5.0.13

## Core Tools
| Tool | Version | Notes |
|---|---|---|
| Node.js | v22.20.0 | via nvm |
| Python | 3.11.7 | via pyenv |
| npm global prefix | nvm-managed | Fine, don't change |
| git | system | — |
| tmux | system | Session management |
| jq | homebrew | JSON processing |
| sqlite3 | homebrew | Local DBs |

## AI Tools Installed
| Tool | Location | Status |
|---|---|---|
| Claude Code | global npm | Active — primary tool |
| Gemini CLI | nvm node bin | Active — large files + visual |
| memory-keeper MCP | npm | Active — persistence |
| soloos-core MCP | local | Active — 33 tools |
| openclaw | global npm | Installed, needs API keys |
| codex-cli | global npm | Installed, needs OAuth |

## MCP Servers (Active)
- `soloos-core` — founder intelligence (33 tools)
- `memory-keeper` — context persistence
- `gemini-cli` — Gemini Pro/Flash access
- `jina` — web scraping (free, no API key)
- `hackernews` — HN stories
- `reddit` — Reddit (needs REDDIT_CLIENT_ID)
- `context7` — library documentation
- `happy` — chat title management

## Projects Layout
```
~/Projects/
├── soloprenuership/     # SoloOS + GovProcure (active)
├── taptap/              # iOS tutorial app for seniors
├── snoozetales/         # AI bedtime stories (if exists)
├── ideas-project/       # Idea vetting + research
├── personal-finance/    # Financial analysis + docs
└── openclaw/            # OpenClaw AI agent setup
```

## OpenClaw Setup (Partial — 2026-02-23)
Status: Files created (69 files, commit f36661e), API keys NOT filled in
Blockers: Replace CHANGEME values in `~/.openclaw/.env`
Full status: `/Users/fsd/Projects/openclaw/.claude/context/session-2026-02-23-openclaw-hq-setup.md`
