from . import TelegramClient, sessions, cfg

bot = TelegramClient(sessions.MemorySession(), cfg.API_ID, cfg.API_HASH)
bot.parse_mode = 'HTML'