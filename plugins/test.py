import google.generativeai as genai
import requests
from pyrogram import *
from pyrogram import Client, filters
from pyrogram.types import *
from RyuzakiLib import FaceAI, FullStackDev, GeminiLatest, RendyDevChat
from pyUltroid.dB.database import db
from pyUltroid.dB.handler import *
from pyUltroid.dB.logger import LOGS

async def mistraai(messagestr):
    url = "https://randydev-ryuzaki-api.hf.space/api/v1/akeno/mistralai"
    payload = {"args": messagestr}
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        return None
    return response.json()

async def chatgptold(messagestr):
    url = "https://randydev-ryuzaki-api.hf.space/ryuzaki/chatgpt-old"
    payload = {"query": messagestr}
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        return None
    return response.json()
    

@ultroid_cmd(pattern="ask$")
async def ask(client, message):
    if len(message.command) > 1:
        prompt = message.text.split(maxsplit=1)[1]
    elif message.reply_to_message:
        prompt = message.reply_to_message.text
    else:
        return await message.reply_text("Give ask from CHATGPT-4O")
    try:
        messager = await chat_message(prompt)
        if len(messager) > 4096:
            with open("chat.txt", "w+", encoding="utf8") as out_file:
                out_file.write(messager)
            await message.reply_document(
                document="chat.txt",
                disable_notification=True
            )
            os.remove("chat.txt")
        else:
            await message.reply_text(messager)
    except Exception as e:
        LOGS.error(str(e))
        return await message.reply_text(str(e))