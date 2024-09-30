from Instruments.Config import client_oai
from .Prompt import get_prompt
import ast


async def convert_msg(msg):
    if msg.lower().strip('"') == "длина":
        return "Длина не указана либо указана неверно"
    elif msg.lower().strip('"') == "ширина":
        return "Ширина не указана либо указана неверно"
    elif msg.lower().strip('"') == "цвет":
        return "Цвет не указан"
    elif msg.lower().strip('"') == "другой цвет":
        return """Указан неверный цвет (доступные: белый, темный орех, антрацит, комбинированный \
темный орех, комбинированный антрацит)"""
    elif msg.lower().strip('"') == "сумма":
        return """Сумма не указана либо указана неверно"""
    elif msg.lower().strip('"') == "параметры":
        return """Не удалось распознать некоторые параметры, попробуйте ввести еще раз. Посмотрите \
инструкцию по команде /instructions"""

    else:
        try:
            parameters = ast.literal_eval(msg)
        except:
            return """Не удалось распознать некоторые параметры, попробуйте ввести еще раз. Посмотрите \
инструкцию по команде /instructions"""

        return parameters


async def send_gpt(message, pd1=True):
    prompt = await get_prompt(message) if pd1 else await get_prompt(message, False)

    response = await client_oai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        n=1)

    formatted_msg = response.choices[0].message.content
    return await convert_msg(formatted_msg)
