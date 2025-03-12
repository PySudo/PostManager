from .. import (
    events,
    db, 
    checkJoin, 
    getJoinText, 
    submit, 
    menu, 
    panel, 
    back_admin, 
    channelString, 
    channelsButton, 
    getLink, 
    createPostButton,
    cfg,
    yes_no,
    channelsButtonUser,
    getLinkUser
)

from ..bot import bot
from ..decorator import ManageDecorators

async def edit(chat_id, message_id, text, buttons=None):
    return await bot.edit_message(chat_id, message_id, text, buttons=buttons)

Decorators = ManageDecorators()
messageDecorator = Decorators.unpackMessage
callbackDecorator = Decorators.unpackCallback
message = events.NewMessage
callback = events.CallbackQuery