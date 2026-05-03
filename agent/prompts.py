from agent.tools import USER_TOOLS, BUILTIN_TOOLS

TOOL_DESCRIPTIONS = "\n".join(
    [f"  - {fn.__name__}: {(fn.__doc__ or '').strip()}" for fn in USER_TOOLS]
    + [f"  - {name} (built-in deepagents tool)" for name in BUILTIN_TOOLS]
)

SYSTEM_PROMPT = f"""You are a helpful assistant powered by deepagents.

You have access to the following tools:
{TOOL_DESCRIPTIONS}

Guidelines:
- For multi-step tasks, always start by calling write_todos to plan your work.
- Use the appropriate math tool instead of computing manually.
- Be concise in your final answers.
"""
