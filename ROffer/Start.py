from Instruments.Config import app, states
from fastapi import Request
import uvicorn
from fastapi.staticfiles import StaticFiles
from Commands import handle_commands
from Company import handle_information
from OfferMessage import handle_text, handle_voice
from Instruments.DB import check_add_new_user as canu


@app.post("/")
async def handle_messages(request: Request):
    form = await request.form()
    message = form.get('Body')
    number = form.get('From')
    id_number = int(number.split('+')[1])

    await canu(id_number)

    state = states[id_number]

    if state == 'commands':
        await handle_commands(message, number, id_number)
    elif state in ('phone', 'address', 'email', 'name'):
        await handle_information(message, number, id_number, state)
    elif state == 'text':
        await handle_text(message, number, id_number)
    elif state == 'voice':
        await handle_voice(message, number, id_number)


app.mount("/", StaticFiles(directory="."), name="root")


if __name__ == "__main__":
    uvicorn.run(app, port=8080)
