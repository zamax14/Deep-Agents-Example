import chainlit as cl

from agent.chat import process_stream_async


@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("messages", [])
    await cl.Message(
        content="Hola! Soy tu asistente powered by **DeepAgents**."
    ).send()


@cl.on_message
async def on_message(message: cl.Message):
    messages: list = cl.user_session.get("messages", [])
    messages.append({"role": "user", "content": message.content})

    thinking = cl.Message(content="")
    await thinking.send()

    updated_messages, final_text = await process_stream_async(messages)

    cl.user_session.set("messages", updated_messages)
    thinking.content = final_text
    await thinking.update()
