from .Config import from_number, client_wa, server_url


async def send_message(text, number):
    client_wa.messages.create(body=text, from_=from_number, to=number)


async def send_document(text, file, number):
    client_wa.messages.create(
        body=text,
        from_=from_number,
        to=number,
        media_url=f"{server_url}/{file}"
        )
