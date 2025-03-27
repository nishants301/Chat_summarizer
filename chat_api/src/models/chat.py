from datetime import datetime
from pydantic import BaseModel

class ChatMessage(BaseModel):
    conversation_id: str
    user_id: str
    message: str


class ConversationSummary(BaseModel):
    summary: str
