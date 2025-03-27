import os
import sys
from fastapi import FastAPI # type: ignore

# Add the 'src' directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.database.mongodb import get_db
from src.models.chat import ConversationSummary
from src.routes.chats import router as chats_router

app = FastAPI()

# Include the routers in the app
app.include_router(chats_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn # type: ignore
    uvicorn.run(app, host="0.0.0.0", port=8000)