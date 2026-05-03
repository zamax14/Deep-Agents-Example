import json

from deepagents import create_deep_agent

from agent.config import model
from agent.prompts import SYSTEM_PROMPT
from agent.tools import USER_TOOLS

agent = create_deep_agent(
    model=model,
    tools=USER_TOOLS,
    system_prompt=SYSTEM_PROMPT,
)


def _fmt_args(args: dict) -> str:
    return json.dumps(args, ensure_ascii=False)


def process_stream(input_messages: list) -> tuple[list, str]:
    """
    Stream the agent response, printing internal activity.
    Returns (updated_messages, final_text).
    """
    final_text = ""
    new_messages: list = []

    for chunk in agent.stream({"messages": input_messages}):
        for _, data in chunk.items():
            if not isinstance(data, dict):
                continue
            for msg in data.get("messages", []):
                new_messages.append(msg)
                msg_type = type(msg).__name__

                if msg_type == "AIMessage":
                    tool_calls = getattr(msg, "tool_calls", [])
                    if tool_calls:
                        for tc in tool_calls:
                            name = tc.get("name", "?")
                            args = tc.get("args", {})
                            print(f"  \033[33m[tool call]\033[0m  {name}({_fmt_args(args)})")
                    elif msg.content:
                        final_text = msg.content

                elif msg_type == "ToolMessage":
                    tool_name = getattr(msg, "name", "tool")
                    raw = str(msg.content)
                    result = raw[:300] + ("…" if len(raw) > 300 else "")
                    print(f"  \033[36m[tool result]\033[0m {tool_name} → {result}")

    updated_messages = list(input_messages) + new_messages
    return updated_messages, final_text


async def process_stream_async(input_messages: list) -> tuple[list, str]:
    """
    Async version: stream the agent response and collect the final text.
    Returns (updated_messages, final_text).
    """
    final_text = ""
    new_messages: list = []

    async for chunk in agent.astream({"messages": input_messages}):
        for _, data in chunk.items():
            if not isinstance(data, dict):
                continue
            for msg in data.get("messages", []):
                new_messages.append(msg)
                msg_type = type(msg).__name__
                if msg_type == "AIMessage":
                    tool_calls = getattr(msg, "tool_calls", [])
                    if not tool_calls and msg.content:
                        final_text = msg.content

    updated_messages = list(input_messages) + new_messages
    return updated_messages, final_text
