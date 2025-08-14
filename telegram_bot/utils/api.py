import aiohttp
from telegram_bot.config import BASE_URL

async def api_request(method, endpoint, token=None, data=None, params=None):
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.request(method, f"{BASE_URL}{endpoint}", json=data, params=params) as response:
            if response.status in (200, 201):
                return await response.json()
            else:
                return {'error': response.status, 'message': await response.text()}
