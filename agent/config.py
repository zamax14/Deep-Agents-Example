import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise EnvironmentError("OPENAI_API_KEY not found. Copy .env.example to .env and add your key.")

model = init_chat_model(model="openai:gpt-4o", temperature=0.0)
