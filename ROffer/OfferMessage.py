from OfferMaking.FormatMSG import send_gpt
from OfferMaking.FileChange import change_file
from Instruments.Sending import send_message, send_document
from Instruments.Config import commands, set_state as ss
from Commands import handle_commands
from Instruments.DB import get_info


async def handle_text(message, number, id_number):
    if message in commands:
        await ss(id_number, 'commands')
        await handle_commands(message, number, id_number)

    else:
        company_data = await get_info(id_number)
        if isinstance(company_data, list):
            text = f'Коммерческое предложение не может быть сгенерировано из-за незавполненых данных: {company_data}'
            await send_message(text, number) #нужно преобразовать в нормальный формат перед отправкой данных

        else:
            result = await send_gpt(message)

            if isinstance(result, tuple):
                await send_message("Ваш файл готовится, ничего не отправляйте", number)
                await change_file(result, company_data)
                await send_document('Коммерческое предложение', 'OfferMaking/Offer.pdf', number)

            else:
                await send_message(result, number)


async def handle_voice(message, number, id_number):
    if message in commands:
        await ss(id_number, 'commands')
        await handle_commands(message, number, id_number)

    else:
        await send_message('Эта функция не готова', number)

