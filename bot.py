import settings
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import ephem

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

async def planet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(update)
    today = datetime.now()
    ephem_planets = {
        'Mars': ephem.Mars(today.date()),
        'Venus': ephem.Venus(today.date()),
        'Saturn': ephem.Saturn(today.date()),
        'Jupiter': ephem.Jupiter(today.date()),
        'Neptune': ephem.Neptune(today.date()),
        'Uranus': ephem.Uranus(today.date()),
        'Mercury': ephem.Mercury(today.date()),
        'Moon': ephem.Moon(today.date())
    }
    planet = update.message.text.split(' ')[-1]
    if planet in ephem_planets:        
        text = ephem.constellation(ephem_planets[planet])
    else:
        text = 'Planet does not exis'
    await context.bot.send_message(
            chat_id = update.effective_chat.id,
            reply_to_message_id = update.effective_message.message_id,
            text = text
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
    planet_handler = CommandHandler('planet', planet)
    echo_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(planet_handler)
    application.add_handler(echo_handler)
    
    application.run_polling()