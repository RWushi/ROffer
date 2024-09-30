from Instruments.DB import insert_info, insert_price_determination
from Instruments.Sending import send_message as sm
from OfferMaking.Company import logo, company_information


async def success_message(entity):
    o = "о" if entity == "Название фирмы" else ""
    return f'{entity} успешно записан{o}, теперь он{o} будет отображаться в КП.'


async def handle_information(message, number, id_number, state):
    column = state

    if state == 'phone':
        entity = 'Номер телефона'
    elif state == 'address':
        entity = 'Адрес'
    elif state == 'email':
        entity = 'Адрес электронной почты'
    elif state == 'name':
        entity = 'Название фирмы'

    company_data = await insert_info(id_number, column, message)
    if company_data:
        await company_information(company_data, id_number)
    await sm(await success_message(entity), number)


async def handle_logo(number, id_number, media_url):
    column, entity = 'logo', 'Логотип'
    await logo(media_url, id_number)
    await insert_info(id_number, column, True)
    await sm(await success_message(entity), number)


async def handle_price_determination(message, number, id_number):
    if message == '1':
        str_digit = 'первый'
    elif message == '2':
        str_digit = 'второй'
    else:
        await sm('Введите 1 или 2', number)
        return

    await insert_price_determination(id_number, message)
    await sm(f'Вы выбрали {str_digit} способ определения цены', number)
