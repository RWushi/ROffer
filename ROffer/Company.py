from Instruments.Config import commands, set_state as ss
from Instruments.DB import insert_info
from Instruments.Sending import send_message as sm
from Commands import handle_commands


async def success_message(entity):
    o = "о" if entity == "Название фирмы" else ""
    return f'{entity} успешно записан{o}, теперь он{o} будет отображаться в КП.'


async def handle_information(message, number, id_number, state):
    if message in commands:
        await ss(id_number, 'commands')
        await handle_commands(message, number, id_number)

    else:
        column = state

        if state == 'phone':
            entity = 'Номер телефона'
        elif state == 'address':
            entity = 'Адрес'
        elif state == 'email':
            entity = 'Адрес электронной почты'
        elif state == 'name':
            entity = 'Название фирмы'

        await insert_info(id_number, column, message)
        await sm(await success_message(entity), number)


