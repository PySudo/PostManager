from telethon import TelegramClient, Button, events, sessions
from .config import cfg
from .database import ManageDB
from .functions import *

submit = lambda channel: [Button.inline('✅', 'submit/'+str(channel))]
menu = [
    [Button.inline('🔖 دریافت پست 🔖', 'getpost')],
    [Button.inline('ارسال پست 📌', 'sendpost'), Button.inline('📝 پست های من', 'myposts')],
    [Button.inline('❗️ نوتیفکشن ❗️', 'notifaction')]
]
panel = [
    [Button.inline('افزودن چنل ➕', 'addchannel') ,Button.inline('➖ حذف چنل', 'removechannel')],
    [Button.inline('📝 مدیریت پست ها 📝', 'manageposts')]
]
back_admin = [Button.inline('🔙', 'backA')]
back = [Button.inline('🔙', 'back')]

def channelsButton(channels):
    buttons = list()
    for i in channels:
        buttons.append([Button.inline(i, 'channel/'+i)])
    buttons.append(back_admin)
    return buttons

def channelsButtonUser(channels):
    buttons = list()
    for i in channels:
        buttons.append([Button.inline(i, 'uchannel/'+i)])
    buttons.append(back)
    return buttons

def createPostButton(links, page, channel, admin=True):
    txt = 'page/' if admin else 'upage/'
    key,value = list(links.keys()), list(links.values())
    buttons = list()
    idx1 = page*10
    idx0 = idx1-10
    for k,i in enumerate(value[idx0:idx1]):
        buttons.append([Button.url(key[idx0:idx1][k], i)])
    if len(key) >= 11:
        if page == 1:
            buttons.append([Button.inline('➡️', txt+str(page+1)+'/'+channel)])
        elif key[idx1:]:
            buttons.append([Button.inline('⬅️', txt+str(page-1)+'/'+channel), Button.inline('➡️', txt+str(page+1)+'/'+channel)])
        else:
            buttons.append([Button.inline('⬅️', txt+str(page-1)+'/'+channel)])
    if admin:
        buttons.append(back_admin)
    else:
        buttons.append(back)
    return buttons

def yes_no(channel, message_id):
    return [Button.inline('✅', 'yes/'+channel+'/'+str(message_id)), Button.inline('❌', 'no/'+channel+'/'+str(message_id))]

db = ManageDB(cfg.DB)