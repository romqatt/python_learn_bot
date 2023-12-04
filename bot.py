import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

import settings

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='bot.log',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(update)
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = f"Hello, {update.effective_user.name}. I'm a bot, please talk to me!"
    )

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(update)
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        reply_to_message_id = update.effective_message.message_id,
        text = f"I'm help you, {update.effective_user.name}"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(update)
    await context.bot.send_message(
        chat_id = update.effective_chat.id,
        reply_to_message_id = update.effective_message.message_id,
        text = update.message.text
    )

if __name__ == '__main__':
    application = ApplicationBuilder().token(settings.bot_token).build()
    
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)
    echo_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(echo_handler)
    
    application.run_polling()