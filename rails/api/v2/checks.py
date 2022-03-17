import quart
from .database import users, members, user_agent_tracking


async def check_session_(session_id):
    user = await users.find_one({'session_ids': [session_id]})

    if user == None:
        return None
    else:
        return user


async def check_if_in_guild(ver):
    member = await members.find_one({'id': ver['id']})

    if member == None:
        return None
    else:
        return member

async def log_user_agent(req: quart.Request):
    user_agent = req.headers.get('User-Agent', '')
    if user_agent in (None, ''):
        return
    
    possible = await user_agent_tracking.find_one({'name': user_agent})

    if possible == None:
        await user_agent_tracking.insert_one({'name': user_agent, 'used': 1})
        return

    used: int = possible['used'] + 1

    await user_agent_tracking.update_one({'name': user_agent}, {'used': used})