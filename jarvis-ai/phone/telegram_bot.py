import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from brain.ollama_client import brain
import asyncio

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# DO NOT HARDCODE TOKENS IN PRODUCTION, BUT IN LOCAL WE WILL DO SO FOR EASE OF SETUP
TELEGRAM_BOT_TOKEN = "8660715600:AAGTKJJiBNs7xA6OvvJ9T4Pq0dWeR53CAaE"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    welcome_message = f"Hello {user.first_name}! I am Fietao AI, your personal local assistant. I am currently running on your home computer. How can I assist you today?"
    await update.message.reply_html(rf"{welcome_message}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Route user messages from Telegram straight to the local Ollama Brain."""
    text = update.message.text
    
    # Think locally (this might take a few seconds depending on the local PC hardware)
    ai_response = brain.think(prompt=text, requires_coding=False)
    
    # Send response back to the user's phone
    await update.message.reply_text(ai_response)


async def ensure_webhook_deleted(application):
    """Ensure no webhook is set before starting polling."""
    await application.bot.delete_webhook()

def start_telegram_bot_sync():
    """Start the bot in an isolated sync loop (blocks thread)."""
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Commands
    application.add_handler(CommandHandler("start", start))

    # Respond to all text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    # Test script directly
    print("Starting Fietao Telegram Integration...")
    start_telegram_bot_sync()