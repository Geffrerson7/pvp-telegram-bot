from settings import config
from api import app
import uvicorn
from telegram import Update
from bot.ptb import ptb
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    filters,
)
from bot.handlers import error_handler, unknown_command, text_handler
from bot.commands import start_pvp_2500,start_pvp_1500, start_pvp_master_league,stop, start_pvp


def add_handlers(dp):
    dp.add_error_handler(error_handler)
    dp.add_handler(CommandHandler("pvp1500", start_pvp_1500))
    dp.add_handler(CommandHandler("pvp2500", start_pvp_2500))
    dp.add_handler(CommandHandler("pvpmaster", start_pvp_master_league))
    dp.add_handler(CommandHandler("pvp", start_pvp))
    dp.add_handler(CommandHandler("stoppvp", stop))
    #dp.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    #dp.add_handler(MessageHandler(filters.COMMAND, unknown_command))

add_handlers(ptb)


if __name__ == "__main__":
    if config.DEBUG == "True":
        ptb.run_polling(allowed_updates=Update.ALL_TYPES)
    else:
        uvicorn.run(app, host="0.0.0.0", port=8000)


