from .config import cfg
from . import db

class ManageDecorators:
    def unpackMessage(self, handler):
        async def unpack(event):
            sender = event.sender_id
            return (await handler(event.raw_text, sender, event.id, sender in cfg.ADMINS, (await db.getUserInfo(sender)), [n for i in (await db.getChannels()) for n in i], event))
        return unpack
    
    def unpackCallback(self, handler):
        async def unpack(event):
            sender = event.sender_id
            return (await handler(event.data.decode(), sender, sender in cfg.ADMINS, (await db.getUserInfo(sender)), [n for i in (await db.getChannels()) for n in i], event))
        return unpack