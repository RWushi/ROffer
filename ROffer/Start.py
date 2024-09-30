from Instruments.Config import app, states, commands
from fastapi import Request
import uvicorn
from fastapi.staticfiles import StaticFiles
from Handlers.Commands import handle_commands
from Handlers.Company import handle_information, handle_price_determination
from Handlers.OfferMessage import checking, handle_discount_price
from Instruments.DB import check_add_new_user as canu
from Instruments.Sending import send_message as sm

photo_error = ("Вам нужно отправить изображение логотипа Вашей фирмы.\nЕсли Вы его уже отправили, "
               "значит произошел сбой при загрузке медиа, попробуйте выбрать другое фото.")
audio_error = ("Вам нужно отправить голосовое сообщение, содержащее параметры заказа.\nЕсли Вы его уже отправили, "
               "значит произошел сбой при загрузке медиа, попробуйте еще раз.")

@app.post("/")
async def handle_messages(request: Request):
    form = await request.form()
    message = form.get('Body')
    number = form.get('From')
    id_number = int(number.split('+')[1])

    await canu(id_number)

    state = states[id_number]

    if state == 'commands' or message.lower().lstrip('/\\') in commands:
        await handle_commands(message, number, id_number)
    elif state in ('phone', 'address', 'email', 'name'):
        await handle_information(message, number, id_number, state)

    elif state == 'logo':
        num_media = int(form.get("NumMedia", 0))
        media_url = form.get("MediaUrl0")
        media_type = form.get("MediaContentType0")
        if num_media > 0 and media_type and media_type.startswith("image/"):
            await checking(number, id_number, media_url)
        else:
            await sm(audio_error, number)

    elif state == 'price':
        await handle_price_determination(message, number, id_number)

    elif state == 'text':
        await checking(number, id_number, message)

    elif state == 'voice':
        num_media = int(form.get("NumMedia", 0))
        media_url = form.get("MediaUrl0")
        media_type = form.get("MediaContentType0")
        if num_media > 0 and media_type and media_type.startswith("audio/"):
            await checking(number, id_number, audio=media_url)
        else:
            await sm(audio_error, number)

    elif state == 'discount_price':
        await handle_discount_price(message, number, id_number)


app.mount("/", StaticFiles(directory="."), name="root")


if __name__ == "__main__":
    uvicorn.run(app, port=8080)
