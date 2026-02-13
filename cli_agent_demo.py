"""
CLI Agent MVP — Replace MCP With CLI
=====================================

This demonstrates an AI Agent that uses CLI tools directly
instead of MCP servers. The agent reasons about what to do,
generates shell commands, executes them, and interprets results.

No MCP servers. No SDKs. No schemas.
Just an LLM + the command line.

Architecture:
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

Requirements:
    pip install openai
    # GROK_API_KEY must be set or in ~/.grok/user-settings.json

Usage:
    python3 cli_agent_demo.py
"""

import json
import os
import subprocess

from openai import OpenAI


# --- Configuration ---

def get_api_key():
    key = os.environ.get("GROK_API_KEY")
    if key:
        return key
    settings_path = os.path.expanduser("~/.grok/user-settings.json")
    if os.path.exists(settings_path):
        with open(settings_path) as f:
            return json.load(f).get("apiKey")
    raise ValueError("Set GROK_API_KEY or add apiKey to ~/.grok/user-settings.json")


client = OpenAI(
    api_key=get_api_key(),
    base_url="https://api.x.ai/v1",
)

# --- Allowed CLI tools (security whitelist) ---

ALLOWED_COMMANDS = {"git", "ls", "cat", "wc", "head", "tail", "find", "grep",
                    "echo", "date", "whoami", "uname", "python3", "pip3",
                    "which", "file", "du", "df", "ps", "uptime", "sw_vers",
                    "sort", "awk", "sed", "cut", "tr", "uniq", "xargs", "jq",
                    "curl"}

SYSTEM_PROMPT = """You are a CLI Agent. You accomplish tasks by executing shell commands.

RULES:
1. When you need information or want to perform an action, respond with a
   shell command inside a ```bash code block.
2. Only use ONE command per response (you can use pipes).
3. After seeing the command output, interpret the results for the user.
4. If no command is needed, just respond normally.
5. You are running on macOS. Available tools: git, ls, cat, wc, head, tail,
   find, grep, echo, date, whoami, uname, python3, pip3, which, file, du, df,
   ps, uptime, sw_vers.
6. Do NOT use sudo or rm. Do NOT modify or delete files.
7. Be concise. Explain what the command does and what the output means.
"""


def extract_command(response_text: str) -> str | None:
    """Extract a bash command from the LLM response."""
    if "```bash" not in response_text:
        return None
    start = response_text.index("```bash") + len("```bash")
    end = response_text.index("```", start)
    return response_text[start:end].strip()


def is_command_allowed(command: str) -> bool:
    """Check if the command's base tool is in the whitelist."""
    base_cmd = command.strip().split()[0]
    # Handle pipes — check all commands in the pipeline
    parts = command.split("|")
    for part in parts:
        cmd = part.strip().split()[0]
        if cmd not in ALLOWED_COMMANDS:
            return False
    return True


def execute_command(command: str, timeout: int = 15) -> str:
    """Execute a shell command and return output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = result.stdout
        if result.stderr:
            output += f"\n[stderr]: {result.stderr}"
        if result.returncode != 0:
            output += f"\n[exit code]: {result.returncode}"
        return output.strip() or "(no output)"
    except subprocess.TimeoutExpired:
        return "[error]: Command timed out after 15 seconds"


def run_agent(user_prompt: str) -> None:
    """Run the CLI agent for a single user prompt."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    max_rounds = 5  # Prevent infinite loops

    for round_num in range(max_rounds):
        # Get LLM response
        response = client.chat.completions.create(
            model="grok-3-fast",
            messages=messages,
            temperature=0.3,
        )

        assistant_msg = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_msg})

        # Check if the response contains a command
        command = extract_command(assistant_msg)

        if command is None:
            # No command — this is the final answer
            print(f"\nAgent: {assistant_msg}")
            return

        # Validate command
        if not is_command_allowed(command):
            print(f"\n  [BLOCKED] Command not in whitelist: {command}")
            messages.append({
                "role": "user",
                "content": f"That command is not allowed. Only these tools are permitted: {', '.join(sorted(ALLOWED_COMMANDS))}. Try a different approach.",
            })
            continue

        # Execute command
        print(f"\n  $ {command}")
        output = execute_command(command)
        print(f"  {output[:500]}")

        # Feed output back to the LLM
        messages.append({
            "role": "user",
            "content": f"Command output:\n```\n{output}\n```\nInterpret this result for the user.",
        })

    print("\nAgent: (max rounds reached)")


# --- Demo ---

SEPARATOR = "=" * 60

DEMOS = [
    "What operating system and hardware am I running on?",
    "How many Python files are in the current directory and its subdirectories?",
    "Show me the 5 largest files in the current directory tree.",
    "What is today's date, who am I logged in as, and how long has this machine been running?",
]


def main():
    print(SEPARATOR)
    print("  CLI Agent MVP — No MCP, Just Shell Commands")
    print("  LLM: Grok 3 Fast  |  Interface: CLI tools")
    print(SEPARATOR)

    for i, prompt in enumerate(DEMOS, 1):
        print(f"\n{'─' * 60}")
        print(f"  Demo {i}: {prompt}")
        print(f"{'─' * 60}")
        run_agent(prompt)

    print(f"\n{SEPARATOR}")
    print("  Done. The agent used CLI tools directly — no MCP servers.")
    print(SEPARATOR)


if __name__ == "__main__":
    main()
