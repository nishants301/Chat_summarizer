from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4
from src.database.mongodb import get_db
from src.models.chat import ChatMessage

router = APIRouter()

@router.post("/chats", status_code=201)
async def create_chat(chat_message: ChatMessage):
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection error")

    # Generate a new UUID for conversation_id if not provided
    if not chat_message.conversation_id:
        chat_message.conversation_id = str(uuid4())

    try:
        result = db.insert_one(chat_message.dict())
        return {"id": str(result.inserted_id), "conversation_id": chat_message.conversation_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inserting chat message: {str(e)}")

@router.get("/chats/")
async def get_conversation(conversation_id: Optional[str] = None):
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection error")

    try:
        if conversation_id is None:
            raise HTTPException(status_code=400, detail="conversation_id is required")
        
        messages = list(db.find({"conversation_id": conversation_id}))
        if not messages:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving conversation: {str(e)}")

@router.post("/chats/summarize")
async def summarize_conversation(conversation_id: Optional[str] = None):
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection error")

    try:
        if conversation_id is None:
            raise HTTPException(status_code=400, detail="conversation_id is required")
        
        messages = list(db.find({"conversation_id": conversation_id}))
        if not messages:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        summary = "This is a placeholder summary for the conversation."
        
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error summarizing conversation: {str(e)}")

@router.get("/users/{user_id}/chats")
async def get_user_chats(user_id: str, page: int = 1, limit: int = 10):
    db = get_db()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection error")

    skip = (page - 1) * limit
    
    try:
        chats = list(db.find({"user_id": user_id}).skip(skip).limit(limit))
        
        total_count = db.count_documents({"user_id": user_id})
        
        return {
            "data": chats,
            "pagination": {
                "total_count": total_count,
                "current_page": page,
                "limit": limit,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user's chat history: {str(e)}")
