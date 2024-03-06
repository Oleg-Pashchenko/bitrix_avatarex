import json
import time
from functools import wraps

from aiohttp import web


async def request_processing(func):
    @wraps(func)
    async def wrapper(request):
        start_time = time.time()
        try:
            try:
                data = dict(json.loads(await request.text()))
            except Exception as e:
                print(e)
            answer = await func(data)
            status = True
        except Exception as e:
            answer, status = {'error': str(e)}, False

        return web.json_response(
            {
                'status': status,
                'answer': answer,
                'execution_time': round(time.time() - start_time, 2)
            },
            status=200 if status else 500
        )

    return wrapper
