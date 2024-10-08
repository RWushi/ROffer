from dotenv import load_dotenv
import os
from twilio.rest import Client
from fastapi import FastAPI
from openai import AsyncOpenAI
import aiohttp
import asyncpg

load_dotenv()

account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')
auth = aiohttp.BasicAuth(account_sid, auth_token)
from_number = f"whatsapp:{os.getenv('PHONE_NUMBER')}"
client_wa = Client(account_sid, auth_token)
server_url = os.getenv('SERVER_URL')

app = FastAPI()

states = {}
commands = ("start", "commands", "instructions", "help", "phone", "address", "email", "name", "logo", "price", "text", "voice")


async def set_state(id_number, state):
    states[id_number] = state


client_oai = AsyncOpenAI(api_key=os.getenv('OPENAI_KEY'))

folder_id = os.getenv('FOLDER_ID')
api_key = os.getenv('API_KEY')

public_key = os.getenv('PUBLIC_KEY')
secret_key = os.getenv('SECRET_KEY')

DATABASE_CONFIG = {
    'host': os.getenv("DB_HOST"),
    'database': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASS"),
    'port': os.getenv("DB_PORT")
}

class DB:
    async def __aenter__(self):
        self.conn = await asyncpg.connect(**DATABASE_CONFIG)
        return self.conn

    async def __aexit__(self, exc_type, exc, tb):
        await self.conn.close()
