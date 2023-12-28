import asyncio
async def fetchall_async(conn, query,*args):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None, lambda: conn.cursor().execute(query,args).fetchall())


async def fetchone_async(conn, query,*args):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None, lambda: conn.cursor().execute(query,args).fetchone())


async def sql_update_async(conn, query,*args):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(
        None, lambda: conn.cursor().execute(query,args))