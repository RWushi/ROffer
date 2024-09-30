async def get_prompt(message, pd1=True):
    if pd1:
        return f"""!ВНИМАНИЕ! Все инструкции нужно соблюдать СТРОГО!
    Извлеки параметры из сообщения и верни один из следующих вариантов ответа в зависимости от ситуации:
    1. Если всё в порядке, верни параметры в формате: (скидка(тг), (длина(м), ширина(м), 'цвет', количество(шт), сумма(тг)), (...)).
    2. Если не указана скидка, значит скидка равна 0.
    3. Если не указана длина или она некорректна (например, слишком большое значение), верни "длина".
    4. Если не указана ширина или она некорректна, верни "ширина".
    5. Если не указан цвет, верни "цвет".
    6. Если указан цвет, который не относится к списку доступных (белый, темный орех, антрацит, комбинированный темный орех, комбинированный антрацит), верни "другой цвет".
    7. Если не указано количество, значит для этой группы окон количество равно 1.
    8. Если не указана сумма для группы окон, верни "сумма".
    9. Если не указано несколько параметров сразу (например, отсутствуют длина и ширина), верни "параметры".

    Учти, что сообщения скорее всего будут нечеткими: размеры могут быть указаны без явного упоминания единиц (например, "200 на 100" это очевидно сантиметры, которые нужно перевести в метры, или "3х4" это очевидно метры), а цвета могут быть описаны неявно (например, "светлый" = белый, "черный" = темный орех, "комбо антра" = комбинированный антрацит). Также суммы и скидка могут быть указаны в любом порядке или с опечатками. Может нарушаться порядок параметров, сообщение и сами параметры не будут иметь четкого формата, тебе придется проявить немного логики, потому что сообщения будут написаны в свободной и иногда неточной форме. Также возможно будет лишняя информация в виде ненужных слов.

    **Особые случаи**:
    - Скидка всегда одна для всех групп окон, но может быть указана неявно или с опечаткой.
    - Суммы для каждой группы окон могут быть указаны с ошибками (например, пропущены тг или суммы разделены пробелами), нужно быть готовым к анализу.

    ОТВЕТ СТРОГО ДОЛЖЕН БЫТЬ ТОЛЬКО ОДНИМ ИЗ ПЕРЕЧИСЛЕННЫХ ВАРИАНТОВ (без номера ответа и точек):
    1. (скидка(тг), (длина(м), ширина(м), 'цвет', количество(шт), сумма(тг)), (...)); - здесь НЕ нужно добавлять единицы измерения
    2. "длина";
    3. "ширина";
    4. "цвет";
    5. "другой цвет";
    6. "сумма";
    7. "параметры".

    Если ты не можешь извлечь несколько параметров или считаешь сообщение невалидным, просто верни ответ "параметры". Если возникла проблема с конкретным параметром, то верни соответствующий ответ. Не предоставляй никаких других пояснений!


    Сообщение: "{message}"
    """

    else:
        return f"""!ВНИМАНИЕ! Все инструкции нужно соблюдать СТРОГО!
        Извлеки параметры из сообщения и верни один из следующих вариантов ответа в зависимости от ситуации:
        1. Если всё в порядке, верни параметры в формате: ((длина(м), ширина(м), 'цвет', количество(шт)), (...)).
        2. Если не указана длина или она некорректна (например, слишком большое значение), верни "длина".
        3. Если не указана ширина или она некорректна, верни "ширина".
        4. Если не указан цвет, верни "цвет".
        5. Если указан цвет, который не относится к списку доступных (белый, темный орех, антрацит, комбинированный темный орех, комбинированный антрацит), верни "другой цвет".
        6. Если не указано количество, значит для этой группы окон количество равно 1.
        7. Если не указано несколько параметров сразу (например, отсутствуют длина и ширина), верни "параметры".

        Учти, что сообщения скорее всего будут нечеткими: размеры могут быть указаны без явного упоминания единиц (например, "200 на 100" это очевидно сантиметры, которые нужно перевести в метры, или "3х4" это очевидно метры), а цвета могут быть описаны неявно (например, "светлый" = белый, "черный" = темный орех, "комбо антра" = комбинированный антрацит). Может нарушаться порядок параметров, сообщение и сами параметры не будут иметь четкого формата, тебе придется проявить немного логики, потому что сообщения будут написаны в свободной и иногда неточной форме. Также возможно будет лишняя информация в виде ненужных слов.

        ОТВЕТ СТРОГО ДОЛЖЕН БЫТЬ ТОЛЬКО ОДНИМ ИЗ ПЕРЕЧИСЛЕННЫХ ВАРИАНТОВ (без номера ответа и точек):
        1. ((длина(м), ширина(м), 'цвет', количество(шт)), (...)); - здесь НЕ нужно добавлять единицы измерения
        2. "длина";
        3. "ширина";
        4. "цвет";
        5. "другой цвет";
        6. "параметры".

        Если ты не можешь извлечь несколько параметров или считаешь сообщение невалидным, просто верни ответ "параметры". Если возникла проблема с конкретным параметром, то верни соответствующий ответ. Не предоставляй никаких других пояснений!


        Сообщение: "{message}"
        """