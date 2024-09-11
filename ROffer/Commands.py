from Instruments.Sending import send_message as sm, send_document as sd
from Instruments.Config import set_state as ss

warning = ("⚠️Внимание!⚠️: Перед тем, как отправлять сообщения для создания КП, мы настоятельно "
           "рекомендуем сначала ознакомиться с простой инструкцией о том, как это делать правильно "
           "для максимально продуктивной работы бота. Чтобы получить инструкцию, введите /instructions.\n\n")


async def handle_commands(message, number, id_number):
    if message == '/start':
        await sm("Добро пожаловать в ROffer! Этот бот нужен для того чтобы "
                           "автоматизировать и упростить создание Коммерческого Предложения для каждого "
                           "клиента с уникальными параметрами. Введите команду /commands для "
                           "описания всех команд бота.", number)

    elif message == '/commands':
        await sm("Список доступных команд:\n\n"
                           "/start: Запуск/Перезапуск бота\n"
                           "/commands: Описание всех доступных команд бота\n"
                           "/instructions: Инструкции по применению бота\n"
                           "/help: Обратиться в поддержку\n\n"
                           "/phone: Ввести номер телефона\n"
                           "/address: Ввести адрес\n"
                           "/email: Ввести адрес электронной почты\n"
                           "/name: Ввести название фирмы\n\n"
                           "/text: Ввести текстовое сообщение для создания КП\n"
                           "/voice: Отправить голосовое сообщение для создания КП",
                           number)

    elif message == '/instructions':
        await sd('Инструкция по применению бота', 'Instructions.pdf', number)

    elif message == '/help':
        await sm("https://wa.me/77078798265", number)

    elif message == '/phone':
        await sm("Введите номер телефона, который нужно отображать в КП. Пример: +77000000000.", number)
        await ss(id_number, 'phone')

    elif message == '/address':
        await sm("Введите адрес, который нужно отображать в КП. Пример: г. Тараз Койгельды 398.", number)
        await ss(id_number, 'address')

    elif message == '/email':
        await sm("Введите адрес электронной почты, который нужно отображать в КП. Пример: apsokna@gmail.com.", number)
        await ss(id_number, 'email')

    elif message == '/name':
        await sm("Введите название фирмы, которое нужно отображать в КП. Пример: Asia Group.", number)
        await ss(id_number, 'name')

    elif message == '/text':
        await sm(f"{warning}Если Вы с ней уже ознакомлены, введите текстовове сообщение, на основе которого нужно создать КП.", number)
        await ss(id_number, 'text')

    elif message == '/voice':
        await sm(f"{warning}Если Вы с ней уже ознакомлены, отправьте голосовое сообщение, на основе которого нужно создать КП.", number)
        await ss(id_number, 'voice')

    else:
        await sm("Такой команды не существует, воспользуйтесь командами бота. Если Вы их "
                           "не знаете, введите: /commands", number)
