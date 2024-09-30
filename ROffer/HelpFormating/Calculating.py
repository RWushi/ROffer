import re

right_dp_msg = 'Нужно ввести только общую сумму скидки и цену за 1 м² (порядок важен). Числа должны быть целыми. Например: 50000, 70000.'


async def format_calculations(parameters):
    text = "Расчеты общей площади:\n"

    if isinstance(parameters[0], tuple):
        areas = []
        for i, group in enumerate(parameters, 1):
            length, width, colour, quantity = group
            area =  float(length) * float(width) * int(quantity)
            text += f"\nПлощадь группы {i}: {length}м × {width}м × {quantity} = {area}м², цвет: {colour}"
            areas.append(area)

        total_area = sum(areas)
        add_text = 'м² +'.join(str(area) for area in areas)
        text += f"\nИтоговая площадь: {add_text} = {total_area}м², цвет: {colour}"

    else:
        length, width, colour, quantity = parameters
        area =  float(length) * float(width) * int(quantity)
        text += f"\nПлощадь: {length}м × {width}м × {quantity} = {area}м², цвет: {colour}"

    return f'{text}\n\n{right_dp_msg}.'


async def discount_price(message):
    numbers = re.findall(r'\d+', message)
    if len(numbers) == 0:
        return f'Вы не ввели ни одного параметра. {right_dp_msg}'
    elif len(numbers) == 1:
        return f'Вы не ввели второй параметр. {right_dp_msg}'
    elif len(numbers) > 2:
        return f'Вы ввели больше двух параметров. {right_dp_msg}'
    elif len(numbers) == 2:
        return tuple(map(int, numbers))


async def merge_data(discount, price, order_information):
    if isinstance(order_information[0], tuple):
        transformed = (discount,) + tuple((
            (length, width, color, quantity, price * length * width * quantity)
            for length, width, color, quantity in order_information))

    else:
        length, width, color, quantity = order_information
        transformed = (discount, (length, width, color, quantity, price * length * width * quantity))

    return transformed
