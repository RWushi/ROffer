from .Config import DB, set_state as ss


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


async def get_info(id_number):
    async with DB() as conn:
        result = await conn.fetchrow('''SELECT phone, address, email, name FROM user_information
                                        WHERE id_number = $1''', id_number)

        columns = ('phone', 'address', 'email', 'name')
        null_columns = [col for col in columns if result[col] is None]

        if null_columns:
            return null_columns
        else:
            return tuple(result)
