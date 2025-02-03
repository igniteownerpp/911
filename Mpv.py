import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from datetime import datetime, timedelta
import json

# Bot Token (Replace with your actual token)
TELEGRAM_BOT_TOKEN = '7788814888:AAHQlW0cT2cHjwLmkr9_YCUVSn86b68rA2k'

# Allowed Group ID (Replace with your actual group/channel ID)
ALLOWED_GROUP_ID = -1002290907768  # Example: -100xxxxxxxxxx

# Global flag to track attack status
attack_in_progress = False

# Default Attack Duration (in seconds)
DEFAULT_DURATION = 150  # Default attack duration in seconds

# Daily attack limit
DAILY_ATTACK_LIMIT = 20

# Tracking user attacks
user_attack_data = {}

# Save attack data to a file
def save_attack_data():
    with open("user_attack_data.json", "w") as f:
        json.dump(user_attack_data, f)

# Load attack data from a file
def load_attack_data():
    global user_attack_data
    try:
        with open("user_attack_data.json", "r") as f:
            user_attack_data = json.load(f)
    except FileNotFoundError:
        user_attack_data = {}

# Function to check if the day has changed and reset user attacks
def reset_daily_limit():
    today = datetime.today().date()
    for user_id, data in user_attack_data.items():
        last_reset = datetime.strptime(data['last_reset'], "%Y-%m-%d").date()
        if last_reset < today:
            # Reset attack count and update the last reset date
            user_attack_data[user_id]['attacks'] = 0
            user_attack_data[user_id]['last_reset'] = str(today)
    save_attack_data()

# Load data on startup
load_attack_data()

async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    if chat_id != ALLOWED_GROUP_ID:
        await context.bot.send_message(chat_id=chat_id, text="⛔ You are not authorized to use this bot.")
        return

    message = (
        "*Ddos King No OneCan Beat 👑*\n\n"
        "*Welcome!*\n"
        "*Use the available commands to interact with the bot.*\n\n"
        "*𝗢𝗪𝗡𝗘𝗥 :- @lostboixd*"
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

async def run_attack(chat_id, ip, port, context):
    global attack_in_progress
    attack_in_progress = True

    try:
        # Simulating an attack process (Replace with actual safe functionality)
        await asyncio.sleep(DEFAULT_DURATION)  # Always use default duration

        # Inform the group after completion
        await context.bot.send_message(chat_id=chat_id, text="*🎗️ ATTACK SIMULATION COMPLETE 🎗️*", parse_mode='Markdown')

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"*⚠️ ERROR ⚠️: {str(e)}*", parse_mode='Markdown')

    finally:
        attack_in_progress = False

async def attack(update: Update, context: CallbackContext):
    global attack_in_progress, user_attack_data

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    args = context.args

    if chat_id != ALLOWED_GROUP_ID:
        await context.bot.send_message(chat_id=chat_id, text="⛔ You are not authorized to execute this command.")
        return

    if attack_in_progress:
        await context.bot.send_message(chat_id=chat_id, text="⚠️ Another attack is already running. Please wait.")
        return

    # Check the daily attack limit
    today = datetime.today().date()

    # Reset daily limits at 12 AM
    reset_daily_limit()

    if user_id not in user_attack_data:
        user_attack_data[user_id] = {'attacks': 0, 'last_reset': str(today)}
    
    if user_attack_data[user_id]['attacks'] >= DAILY_ATTACK_LIMIT:
        await context.bot.send_message(chat_id=chat_id, text=f"⚠️ Daily attack limit of {DAILY_ATTACK_LIMIT} reached. Please try again tomorrow.")
        return

    # Ensure the attack uses the default duration, ignore custom duration input
    if len(args) >= 2:
        ip, port = args
    elif len(args) == 1:
        ip = args[0]
        port = "80"  # Default port if not provided
    else:
        await context.bot.send_message(chat_id=chat_id, text="Usage: /attack <IP> <Port>", parse_mode='Markdown')
        return

    # Proceed with the attack using the default duration
    await context.bot.send_message(chat_id=chat_id, text=(
        f"*🚀 ATTACK STARTED 🚀*\n"
        f"*Target IP:* {ip}\n"
        f"*Port:* {port}\n"
        f"*Duration:* {DEFAULT_DURATION} sec (default duration)\n"
    ), parse_mode='Markdown')

    # Increment attack count
    user_attack_data[user_id]['attacks'] += 1
    save_attack_data()  # Save the updated data

    # Start the attack simulation
    asyncio.create_task(run_attack(chat_id, ip, port, context))

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("attack", attack))  # Restricted for approved group only
    application.run_polling()

if __name__ == '__main__':
    main()
                                       
