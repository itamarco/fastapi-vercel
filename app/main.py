import logging

from fastapi import FastAPI
from pydantic import BaseModel
import requests

from fastapi.logger import logger

from app.db import reminder_dao

app = FastAPI()

API_TOKEN = '7485608813:AAFcFEZm4fSy3aHxntUR7ou9scQ9VQfJWSs'
TELEGRAM_API_URL = f"https://api.telegram.org/bot{API_TOKEN}"


class TelegramWebhook(BaseModel):
    message: dict


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/db")
async def db():
    reminder_dao.find_by_user("LOLO")
    return {"message": "Database is ready"}

@app.post("/webhook")
async def webhook(telegram_webhook: TelegramWebhook):
    message = telegram_webhook.message
    chat_id = message['chat']['id']
    text = message.get('text', '')

    reply_text = f"Hello, {text}"
    send_message(chat_id, reply_text)

    return {"status": "ok"}


@app.get("/periodic_hello")
async def cron():
    logger.info("Sending periodic hello message")
    send_message("549326175", "אהלן סהלן")


def send_message(chat_id, text):
    url = f"{TELEGRAM_API_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
