from OfferMaking.FormatMSG import send_gpt
from OfferMaking.FileChange import change_file
from Instruments.DB import get_info
import asyncio


async def format(id_number):
    company_data = await get_info(id_number)

    if isinstance(company_data, list):
        text = f'Коммерческое предложение не может быть сгенерировано из-за незавполненых данных: {company_data}'
        print(text)
    else:
        result = await send_gpt(input("Сообщение:"))

        if isinstance(result, tuple):
            await change_file(result, company_data)
            print("Удачно")

        else:
            print(result)


asyncio.run(format(77011895969))
