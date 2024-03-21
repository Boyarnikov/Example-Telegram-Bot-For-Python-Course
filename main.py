from telegram.ext import ContextTypes, CommandHandler, ConversationHandler
from telegram import Update

import Model

import logging
import BotSetup

from ListEditingConversation import create_conversation

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(message)s",
    level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)




if __name__ == "__main__":
    app = BotSetup.setup_app()


    app.add_handler(create_conversation())
    app.run_polling()
