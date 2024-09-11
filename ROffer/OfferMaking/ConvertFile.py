import aiohttp
from .Token import generate_token

file_path = "OfferMaking/КП.docx"
original_filename = "КП.docx"
final_file = "OfferMaking/Offer.pdf"


async def start_task(headers):
    url = 'https://api.ilovepdf.com/v1/start/officepdf'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            result = await response.json()
            server = result['server']
            task = result['task']
            return server, task


async def upload_file(headers, server, task):
    url = f'https://{server}/v1/upload'
    data = aiohttp.FormData()
    data.add_field('task', task)

    file = open(file_path, 'rb')
    data.add_field('file', file, filename=original_filename)

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=data) as response:
            result = await response.json()
            file.close()
            return result['server_filename']


async def process_file(headers, server, task, server_filename):
    url = f'https://{server}/v1/process'

    data = {
        'task': task,
        'tool': 'officepdf',
        'files': [{
            'server_filename': server_filename,
            'filename': original_filename
        }]
    }

    async with aiohttp.ClientSession() as session:
        await session.post(url, headers=headers, json=data)


async def download_file(headers, server, task):
    url = f'https://{server}/v1/download/{task}'

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            content = await response.read()
            with open(final_file, 'wb') as f:
                f.write(content)


async def convert_file():
    token = await generate_token()
    headers = {
        'Authorization': f'Bearer {token}'
    }
    server, task = await start_task(headers)
    server_filename = await upload_file(headers, server, task)
    await process_file(headers, server, task, server_filename)
    await download_file(headers, server, task)
