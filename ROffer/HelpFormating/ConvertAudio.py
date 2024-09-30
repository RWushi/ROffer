import aiohttp
from Instruments.Config import api_key, folder_id, auth
import io

url = f"https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?folderId={folder_id}&lang=ru-RU"
headers = {"Authorization": f"Api-Key {api_key}"}


async def convert_audio(audio_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(audio_url, auth=auth) as response:
            file_data = await response.read()
            audio = io.BytesIO(file_data)
        async with session.post(url, headers=headers, data=audio) as response:
            result = await response.json()
            return result['result']
