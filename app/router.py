import asyncio

from aiohttp import web

from app.handlers import *


async def request_logger_middleware(app, handler):
    async def middleware_handler(request):
        print(f"Запрос: {request.method} {request.rel_url}")
        # Для более детальной информации можно добавить:
        print(f"Заголовки: {request.headers}")
        print(f"Тело запроса: {await request.text()}")
        response = await handler(request)
        return response

    return middleware_handler


app = web.Application(middlewares=[request_logger_middleware])


async def routes():
    app.router.add_post('/', await new_message_handler)
    app.router.add_post('/send-message/', await send_message_handler)
    app.router.add_post('/get-info/', await get_info_handler)
    app.router.add_post('/connect/', await connect_handler)
    app.router.add_post('/get-lead/', await get_lead_handler)
    app.router.add_post('/set-field/', await set_field_handler)


asyncio.run(routes())
