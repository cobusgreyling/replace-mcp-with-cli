# Replace MCP With CLI — The Best AI Agent Interface Already Exists

## The Most Powerful Tool Protocol For AI Agents Has Been On Every Unix System Since 1971

I have been thinking about this for a while, and a recent interview crystallised something I have been observing across the agentic AI landscape.

**What if the best interface for AI Agents is not a new protocol at all?**

What if it is the command line — the same interface that has been powering software for over fifty years?

---

### The Shift That Is Already Happening

As Jensen Huang put it, traditional software is essentially **pre-recorded**. Humans write algorithms, define recipes, and let the computer execute them. The output is deterministic and fixed.

> **"For the first time, we now have a computer that is not pre-recorded but it's processing in real time."** — Jensen Huang, NVIDIA

This has implications far beyond GPUs. I really see **structure collapsing**. The rigid layers of SaaS, APIs, integration platforms, middleware — all of it was built for a world of pre-recorded software. When processing happens in real time, when an AI Agent can reason about what to do next, the integration layer does not need to be pre-built. It happens on the fly.

And that is where CLI enters the picture.

---

### MCP — The Problem It Solves And The Overhead It Creates

Anthropic's Model Context Protocol is an important step. It standardises how LLMs connect to external tools and data sources. Think of it as a USB-C port for AI — one protocol, many integrations.

But here is the reality on the ground:

- Every new integration **requires building and maintaining an MCP server**
- Each server needs **SDKs, schemas, edge case handling, version management**
- The ecosystem depends on **adoption** — the protocol's value is only as good as the number of available servers
- State management across sessions adds **complexity**

MCP solves the right problem. But the implementation overhead is significant. And for many common tasks, a simpler pattern already exists.

---

### CLI — The Interface LLMs Already Understand

Here is what makes the command line so compelling for AI Agents:

**It already exists.** Every major service ships a CLI — `gh` for GitHub, `aws` for AWS, `kubectl` for Kubernetes, `docker`, `terraform`, `git`, `npm`. These are not toy tools. They are production-grade, battle-tested, and maintained by the service providers themselves.

**LLMs are trained on it.** AI models have ingested vast amounts of shell scripts, documentation, man pages, and Stack Overflow answers. The CLI is deeply embedded in their training data. They know how to use it.

**It is self-documenting.** Every CLI tool ships with `--help`. An agent can discover capabilities at runtime without external schema definitions.

**It is composable.** The Unix philosophy — small tools that do one thing well, connected through pipes — is exactly how agents should work. Chain `grep`, `awk`, `jq`, `curl` together and you have an integration pipeline that no MCP server needs to define.

```
HOST
├── AI Agent (LLM reasoning)
│   │
│   ├── "I need to list open PRs"
│   │   └── gh pr list --state open
│   │
│   ├── "I need to check pod health"
│   │   └── kubectl get pods --all-namespaces
│   │
│   ├── "I need to find large files in git"
│   │   └── git rev-list --objects --all | ...
│   │
│   └── No MCP server needed. No SDK. No schema.
│       Just shell commands the model already knows.
```

What I find interesting is the inversion. With MCP, you build the bridge **to** the tool. With CLI, the bridge **already exists**. The agent just needs permission to cross it.

---

### The Benchmarks Back It Up

A recent benchmark comparing CLI against MCP for browser automation tasks showed:

| Metric | CLI | MCP |
|--------|-----|-----|
| **Effectiveness Score** | 77/100 | 60/100 |
| **Token Efficiency** | 202.1 | 152.3 |
| **Token Usage** | ~38.1K | ~39.4K |

CLI achieved **28% higher effectiveness** with similar token usage, and **33% better token efficiency**. The reason? CLI tools allow selective queries. MCP servers tend to dump entire data structures — accessibility trees, full page content — consuming tokens even when the agent only needs a small slice.

---

### This Is Structure Collapsing

I think what we are witnessing is the collapse of integration infrastructure. Consider what traditionally sits between an AI system and a service:

```
TRADITIONAL (Pre-recorded)          EMERGING (Real-time)
──────────────────────────          ────────────────────

Application                         AI Agent
    │                                   │
    ▼                                   │
REST API Client                         │
    │                                   │
    ▼                                   │
Authentication Layer                    │
    │                                   │
    ▼                                   │
Integration Platform                    │
    │                                   │
    ▼                                   │
API Gateway                             │
    │                                   │
    ▼                                   ▼
Service                             $ gh pr list
                                    $ kubectl get pods
                                    $ aws s3 ls
```

Six layers collapse into one. The agent reasons about the intent, generates the command, and executes it. No middleware. No integration platform. No pre-built connectors.

This is what Jensen Huang means by real-time processing replacing pre-recorded software. The integration is not defined ahead of time — it emerges from the agent's reasoning at the moment it is needed.

SaaS itself starts to look different in this world. If an AI Agent can interact with any service through its CLI, what is the value of a polished dashboard? The interface shifts from human-facing UIs to agent-facing command lines.

---

### Security — The Honest Trade-Off

I should be honest about the trade-offs. CLI access is powerful, which means it is dangerous.

- An agent with shell access has **user-level permissions** — it can do anything you can do
- **Prompt injection** can trick an agent into running destructive commands
- There is **no granular permission model** at the command level

MCP arguably has an advantage here — you can restrict what each server exposes. With CLI, you need to enforce boundaries differently:

- **Command whitelisting** — only allow specific tools
- **Sandboxing** — run CLI commands inside containers
- **Human-in-the-loop** — require approval for destructive operations
- **Audit logging** — track every command the agent runs

Neither approach is secure by default. Both require deliberate engineering.

---

### When To Use What

This is not an either-or debate. It is a spectrum:

| Scenario | Use CLI | Use MCP |
|----------|---------|---------|
| Well-known tools (`gh`, `aws`, `docker`) | ✓ | |
| One-off tasks and exploration | ✓ | |
| Composable multi-tool pipelines | ✓ | |
| Custom internal business logic | | ✓ |
| Stateful multi-turn interactions | | ✓ |
| Real-time streaming responses | | ✓ |
| Services without a CLI | | ✓ |

The decision framework is simple: **if a CLI exists and the model knows it, use it. Build an MCP server only when you must.**

---

### Where This Goes

The trajectory I see:

1. **CLI-first becomes the default** for agent-to-service interaction
2. **MCP remains important** for custom, stateful, and streaming use cases
3. **SaaS dashboards decline** as agents become the primary interface
4. **Integration platforms lose relevance** as agents compose tools on the fly
5. **The Unix philosophy wins again** — small, composable tools connected by convention

The best agent interface was never going to be a new protocol. It was always going to be the one that every tool already speaks.

> **The humble command line is proving to be the most robust, universal, and battle-tested way for agents to interact with the world.**

I think we are only at the beginning of this shift.

⭐️ Follow me on [LinkedIn](https://www.linkedin.com/in/cobusgreyling) for more on Agentic AI, LLMs and NLP.
