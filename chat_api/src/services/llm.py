import os
from openai import OpenAI
from dotenv import load_dotenv
from fastapi import HTTPException
from src.models.chat import ConversationSummary
from src.database.mongodb import get_db
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    # This is the default and can be omitted
    api_key=OPENAI_API_KEY,
)


def generate_summary(converation_id: str) -> ConversationSummary:
    try:
        messages = list(get_db.find({"conversation_id": conversation_id}))
        if not messages:
            raise HTTPException(status_code=404, detail="Conversation not found")
        response = client.responses.create(
            model="gpt-4o-mini",
            instructions="Summarize the conversation",
            input="\n\n".join(messages),
        )
        return ConversationSummary(
            summary=response.output_text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
