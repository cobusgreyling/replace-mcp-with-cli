# Replace MCP With CLI

The best AI agent interface already exists — the command line.

This repo accompanies the blog post exploring why CLI tools may be a simpler, more robust alternative to MCP for many AI agent integrations.

## Files

- **`replace-mcp-with-cli-blog.md`** — Full blog post
- **`cli_agent_demo.py`** — Working MVP: an AI agent that uses CLI tools directly instead of MCP servers

## Quick Start

```bash
pip install openai
export GROK_API_KEY="your-key-here"
python3 cli_agent_demo.py
```

## Architecture

```
┌────────────────────────────────────┐
│           CLI AGENT                │
│                                    │
│  User Prompt                       │
│       │                            │
│       ▼                            │
│  ┌──────────┐    ┌──────────────┐  │
│  │   LLM    │───▶│  Generates   │  │
│  │  (Grok)  │    │  CLI command │  │
│  └──────────┘    └──────┬───────┘  │
│                         │          │
│                         ▼          │
│                  ┌──────────────┐  │
│                  │  Executes    │  │
│                  │  in shell    │  │
│                  └──────┬───────┘  │
│                         │          │
│                         ▼          │
│                  ┌──────────────┐  │
│                  │  Returns     │  │
│                  │  result      │  │
│                  └──────────────┘  │
└────────────────────────────────────┘
```

No MCP servers. No SDKs. No schemas. Just an LLM + the command line.
