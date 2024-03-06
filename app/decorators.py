import json
import time
from functools import wraps

from aiohttp import web
from urllib.parse import parse_qs


async def request_processing(func):
    @wraps(func)
    async def wrapper(request):
        start_time = time.time()
        try:
            try:
                data = dict(json.loads(await request.text()))
            except Exception as e:
                url_encoded_data = await request.read()
                parsed_data = parse_qs(url_encoded_data.decode('utf-8'))
                data = {key: value[0] for key, value in parsed_data.items()}
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
