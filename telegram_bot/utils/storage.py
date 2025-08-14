user_tokens = {}

async def save_token(user_id, token):
    user_tokens[user_id] = token


async def get_token(user_id):
    return user_tokens.get(user_id)
