from core.handlers import MessageHandler, Query
from core.bot import bot
from core import cfg

bot.start(bot_token=cfg.TOKEN)
bot.run_until_disconnected()