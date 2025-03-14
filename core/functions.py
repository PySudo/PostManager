from requests import get
from .config import cfg

def isJoin(channel, user):
    res = get(f'https://api.telegram.org/bot{cfg.TOKEN}/getChatMember', {'chat_id': channel, 'user_id': user}).json()
    if res['ok']:
        return res['result']['status'] != 'left'

def checkJoin(user, channels):
    ch = list()
    for channel in channels:
        if not isJoin(channel, user):
            ch.append(channel)
    return ch

def channelString(channels):
    return '\n'.join(i if i[0] == '@' else '@'+i for i in channels)

def getJoinText(channels):
    text = "❗️ لطفا اول توی کانال {} جوین شو :\n{}"
    ch = channelString(channels)
    if len(channels) == 1:
        return text.format('های ما', ch)
    return text.format('ما', ch)

def getLinkUser(username, data):
    username = username.replace('@', '')
    return {k:f'https://t.me/{cfg.USERNAME}?start={username}_{i}' for k,i in data.items()}

def getLink(username, data):
    username = username.replace('@', '')
    return {k:f'https://t.me/{username}/{i}' for k,i in data.items()}