from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse

from app.db import create_all
from app.message_dao import MessageDAO
from app.models import MessageCreate, MessageResponse
from app.schema import Message

import logging
import sys

# Workaround for logging in Vercel
logging.basicConfig(
    stream=sys.stderr,  # Redirect logs to stdout
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

def get_message_dao() -> MessageDAO:
    return MessageDAO()

def lifespan(_: FastAPI):
    create_all()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root() -> dict[str, str]:   
    return {"status": "ok"}


@app.post("/messages")
async def create_message(
    msg: MessageCreate, 
    message_dao: MessageDAO = Depends(get_message_dao)
) -> MessageResponse:
    return message_dao.create(msg.message)

@app.get("/messages")
async def get_message(
    message_dao: MessageDAO = Depends(get_message_dao)
) -> list[MessageResponse]:
    return message_dao.get_all()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
