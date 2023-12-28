import sqlite3
from async_sql import *


db = sqlite3.connect('data.db',check_same_thread=False)
cursor = db.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY,
    name TEXT
    )""")


cursor.execute("""CREATE TABLE IF NOT EXISTS cabinets (
    id INT,
    seats INT
    )""")


cursor.execute("""CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY,
    name TEXT
    )""")


cursor.execute("""CREATE TABLE IF NOT EXISTS shedule (
    id INTEGER PRIMARY KEY,
    teacher_id INT,
    name_id INT,
    cab_id INT,
    time_id INT,
    date TEXT
    )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS time (
    id INTEGER PRIMARY KEY,
    value TEXT
    )""")


db.commit()
async def insert_new_values(table:str,data_columns:list,data:list):
    args = []
    i = 0
    for col_info in data_columns:
        if col_info[5] == 1:
            args.append(None)
        else:
            args.append(data[i])
            i+=1
    query = (f"INSERT INTO {table} VALUES "
            f"({','.join(['?' for i in range(len(args))])})")
    await sql_update_async(db,
                           query,
                           *args)
    db.commit()

async def get_values(table:str,columns:list,id:str):
    return await fetchone_async(db,f"SELECT {','.join(columns)} "
                                   f"FROM {table} "
                                   f"WHERE id = ?",id)

async def edit_values(table:str,cols:list,vals:list,id:str):
    try:
        vals.append(id)
        query = (f"UPDATE {table} "
                               f"SET {', '.join([f'{col} = ?' for col in cols])}"
                               f"WHERE id = ?")
        await sql_update_async(db,
                               query,*vals)
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False

async def remove_from_db(table:str,id:str):
    await sql_update_async(db,f"DELETE FROM {table} "
                              f"WHERE id = ?",id)
    db.commit()
    return True

async def get_collumn_names(table:str):
    return await fetchall_async(db,f"PRAGMA table_info({table});",)

async def get_table_data(table:str):
    return await fetchall_async(db,f"SELECT * "
                                   f"FROM {table}",)

async def get_shedule(date:str):
    return await fetchall_async(db,f"SELECT * "
                                   f"FROM shedule "
                                   f"WHERE date = ?",date)
