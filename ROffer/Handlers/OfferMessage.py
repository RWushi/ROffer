from HelpFormating.FormatMSG import send_gpt
from OfferMaking.FileChange import change_file
from HelpFormating.Calculating import format_calculations, discount_price, merge_data
from HelpFormating.ConvertAudio import convert_audio
from Instruments.Sending import send_message, send_document
from Instruments.DB import check_info, check_price_determination as cpd
from Instruments.Config import set_state as ss

translations = {'phone':'номер телефона', 'address':'адрес', 'email':'адрес электронной почты',
                'name':'название фирмы', 'logo':'логотип', 'price_determination': 'определение цены'}

information = {}


async def checking(number, id_number, message=None, audio=None):
    company_data = await check_info(id_number)

    if company_data:
        russian_list = [translations[parameter] for parameter in company_data]
        formatted_list = ', '.join(russian_list)
        text = f'Коммерческое предложение не может быть сгенерировано из-за незаполненых данных: {formatted_list}.'
        await send_message(text, number)
        await ss(id_number, 'commands')

    else:
        if audio:
            message = await convert_audio(audio)
        pd = await cpd(id_number)
        if pd == '1':
            await handle_text(message, number, id_number)
        elif pd == '2':
            await calculate_square(message, number, id_number)


async def handle_text(message, number, id_number):
    result = await send_gpt(message)

    if isinstance(result, tuple):
        await send_message("Ваш файл готовится, ничего не отправляйте", number)
        await change_file(result, id_number)
        await send_document('Коммерческое предложение', '../OfferMaking/Files/Offer.pdf', number)

    else:
        await send_message(result, number)


async def calculate_square(message, number, id_number):
    result = await send_gpt(message, False)

    if isinstance(result, tuple):
        information[id_number] = result
        await send_message(await format_calculations(result), number)
        await ss(id_number, 'discount_price')

    else:
        await send_message(result, number)


async def handle_discount_price(message, number, id_number):
    result = await discount_price(message)

    if isinstance(result, tuple):
        data = await merge_data(*result, information[id_number])
        await send_message("Ваш файл готовится, ничего не отправляйте", number)
        await change_file(data, id_number)
        await send_document('Коммерческое предложение', 'OfferMaking/Files/Offer.pdf', number)
        await ss(id_number, 'text')

    else:
        await send_message(result, number)
