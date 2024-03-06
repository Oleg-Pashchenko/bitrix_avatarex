import asyncio

from aiohttp import web

from app.handlers import *

app = web.Application()


async def routes():
    app.router.add_post('/', await new_message_handler)
    app.router.add_post('/send-message/', await send_message_handler)
    app.router.add_post('/get-info/', await get_info_handler)
    app.router.add_post('/connect/', await connect_handler)
    app.router.add_post('/get-lead/', await get_lead_handler)


asyncio.run(routes())
