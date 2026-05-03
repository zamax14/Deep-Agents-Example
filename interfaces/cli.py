from agent.chat import process_stream
from agent.prompts import TOOL_DESCRIPTIONS

COMMANDS = {
    "/tools":   "listar todas las herramientas disponibles",
    "/clear":   "limpiar el historial de conversación",
    "/history": "mostrar el historial de mensajes",
    "/help":    "mostrar esta ayuda",
    "/exit":     "salir del chat",
}

# --- Chat loop -----------------------------------------------------------

print("----------------------------------------------------")
print("| Deep Agent chat                                   |")
print("| Escribe /help para ver los comandos disponibles  |")
print("----------------------------------------------------")
print()

messages: list = []

while True:
    try:
        user_input = input("You: ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
        break

    if not user_input:
        continue

    if user_input.lower() == "/exit":
        print("Goodbye!")
        break

    if user_input.lower() == "/help":
        print("\nComandos disponibles:")
        for cmd, desc in COMMANDS.items():
            print(f"  {cmd:<12} {desc}")
        print()
        continue

    if user_input.lower() == "/tools":
        print("\nHerramientas disponibles:")
        print(TOOL_DESCRIPTIONS)
        print()
        continue

    if user_input.lower() == "/clear":
        messages = []
        print("\nHistorial limpiado.\n")
        continue

    if user_input.lower() == "/history":
        if not messages:
            print("\n(sin mensajes aún)\n")
        else:
            print()
            for msg in messages:
                if isinstance(msg, dict):
                    role = msg.get("role", "?")
                    content = str(msg.get("content", ""))
                else:
                    role = getattr(msg, "type", type(msg).__name__)
                    content = str(getattr(msg, "content", msg))
                short = content[:120] + ("…" if len(content) > 120 else "")
                print(f"  [{role}] {short}")
            print()
        continue

    messages.append({"role": "user", "content": user_input})

    print()
    messages, final_text = process_stream(messages)
    print(f"\n\033[32mAgent:\033[0m {final_text}\n")
