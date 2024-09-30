from Instruments.Config import DB, set_state as ss


async def check_add_new_user(id_number):
    async with DB() as conn:
        exists = await conn.fetchval('SELECT EXISTS(SELECT 1 FROM user_information WHERE id_number = $1)', id_number)
        if not exists:
            await conn.execute('INSERT INTO user_information (id_number) VALUES ($1)', id_number)
            await ss(id_number, 'commands')


async def insert_info(id_number, column, value):
    async with DB() as conn:
        query = f'UPDATE user_information SET {column} = $2 WHERE id_number = $1'
        await conn.execute(query, id_number, value)

        if column != 'logo':
            result = await conn.fetchrow('''SELECT phone, address, email, name FROM
                                            user_information WHERE id_number = $1''', id_number)
            if all(result.values()):
                return tuple(result.values())


async def insert_price_determination(id_number, value):
    async with DB() as conn:
        await conn.execute('''UPDATE user_information SET price_determination = $2 WHERE id_number = $1''', id_number, value)


async def check_info(id_number):
    async with DB() as conn:
        result = await conn.fetchrow('''SELECT phone IS NOT NULL AS phone,
                                               address IS NOT NULL AS address,
                                               email IS NOT NULL AS email,
                                               name IS NOT NULL AS name,
                                               logo IS TRUE AS logo,
                                               price_determination IS NOT NULL AS price_determination
                                        FROM user_information
                                        WHERE id_number = $1''', id_number)

        columns = ('phone', 'address', 'email', 'name', 'logo', 'price_determination')
        null_columns = [col for col in columns if result[col] is False]

        return null_columns


async def check_price_determination(id_number):
    async with DB() as conn:
        return await conn.fetchval('SELECT price_determination FROM user_information WHERE id_number = $1', id_number)
