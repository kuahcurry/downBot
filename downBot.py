import os
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes, MessageHandler, filters
)

BOT_TOKEN = 'YOUR_BOT_TOKEN'
AUTHORIZED_USER = YOUR_TELEGRAM_USER_ID

# Global shutdown timer
shutdown_timer = None
shutdown_start_time = None

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER:
        await update.message.reply_text("Access Denied.")
        return

    keyboard = [
        [InlineKeyboardButton("🛑 Shutdown", callback_data='shutdown')],
        [InlineKeyboardButton("🔁 Restart", callback_data='restart')],
        [InlineKeyboardButton("💤 Sleep", callback_data='sleep')],
        [InlineKeyboardButton("🌙 Hibernate", callback_data='hibernate')],
        [InlineKeyboardButton("📊 Check Shutdown Timer", callback_data='check_timer')],
        [InlineKeyboardButton("❌ Remove Shutdown Timer", callback_data='remove_shutdown')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("What will you do with your beloved PC, dear?", reply_markup=reply_markup)

# Action handler
async def handle_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if update.effective_user.id != AUTHORIZED_USER:
        await query.edit_message_text("Access Denied.")
        return

    action = query.data

    if action == 'shutdown':
        keyboard = [
            [InlineKeyboardButton("⚠️ Shutdown Immediately?", callback_data='confirm_shutdown')],
            [InlineKeyboardButton("10 Minutes", callback_data='shutdown_10')],
            [InlineKeyboardButton("20 Minutes", callback_data='shutdown_20')],
            [InlineKeyboardButton("30 Minutes", callback_data='shutdown_30')],
            [InlineKeyboardButton("🖊 Custom Time", callback_data='shutdown_custom')],
            [InlineKeyboardButton("❌ Remove Shutdown Timer", callback_data='remove_shutdown')],
            [InlineKeyboardButton("🔙 Back", callback_data='back_to_main')]
        ]
        await query.edit_message_text("How long until the shutdown?", reply_markup=InlineKeyboardMarkup(keyboard))

    elif action == 'confirm_shutdown':
        confirm_keyboard = [
            [InlineKeyboardButton("✅ Yes, shut it down now!", callback_data='shutdownI')],
            [InlineKeyboardButton("❌ No, I'll prolly go back", callback_data='shutdown')]
        ]
        await query.edit_message_text("Are you *really* sure you want to shutdown now?", reply_markup=InlineKeyboardMarkup(confirm_keyboard))

    elif action == 'restart':
        os.system("shutdown /r /t 0")
        await query.edit_message_text("🔁 Restarting now...")

    elif action == 'sleep':
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        await query.edit_message_text("😴 Going to sleep...")

    elif action == 'hibernate':
        os.system("shutdown /h")
        await query.edit_message_text("🌙 Hibernating now...")

    elif action == 'check_timer':
        global shutdown_timer, shutdown_start_time
        if shutdown_timer is not None:
            elapsed = int(time.time() - shutdown_start_time)
            remaining = shutdown_timer - elapsed
            if remaining > 0:
                minutes = remaining // 60
                seconds = remaining % 60
                await query.edit_message_text(f"⏱ Remaining shutdown timer: {minutes} min {seconds} sec")
            else:
                shutdown_timer = None
                await query.edit_message_text("No shutdown scheduled.")
        else:
            await query.edit_message_text("No shutdown timer is active.")

    elif action == 'remove_shutdown':
        if shutdown_timer:
            os.system("shutdown /a")
            shutdown_timer = None
            await query.edit_message_text("🛑 Shutdown timer removed.")
        else:
            await query.edit_message_text("There’s no timer to remove, u silly")

    elif action == 'back_to_main':
        await start(update, context)

# Shutdown time handler
async def handle_shutdown_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global shutdown_timer, shutdown_start_time
    query = update.callback_query
    await query.answer()
    action = query.data

    time_map = {
        'shutdown_10': 600,
        'shutdown_20': 1200,
        'shutdown_30': 1800
    }

    if action in time_map:
        seconds = time_map[action]
        os.system(f"shutdown /s /t {seconds}")
        shutdown_timer = seconds
        shutdown_start_time = time.time()
        await query.edit_message_text(f"💤 Shutting down in {seconds // 60} minutes...")
    elif action == 'shutdownI':
        os.system("shutdown /s /t 0")
        shutdown_timer = None
        await query.edit_message_text(" Your PC is shutting down now... farewell~")
    elif action == 'shutdown_custom':
        await query.edit_message_text("Type how many *minutes* until shutdown (example: `15`).")

# Custom time input
async def handle_custom_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global shutdown_timer, shutdown_start_time
    if update.effective_user.id != AUTHORIZED_USER:
        return

    try:
        minutes = int(update.message.text.strip())
        if minutes <= 0:
            await update.message.reply_text("Thus value must be filled by more than 0, my dear~")
            return
        seconds = minutes * 60
        os.system(f"shutdown /s /t {seconds}")
        shutdown_timer = seconds
        shutdown_start_time = time.time()
        await update.message.reply_text(f"🕒 Shutting down in {minutes} minutes, tick tock~")
    except ValueError:
        await update.message.reply_text("That's not a valid value, dear")

# /status command
async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global shutdown_timer, shutdown_start_time
    if update.effective_user.id != AUTHORIZED_USER:
        await update.message.reply_text("Access Denied.")
        return

    if shutdown_timer is not None:
        elapsed = int(time.time() - shutdown_start_time)
        remaining = shutdown_timer - elapsed
        if remaining > 0:
            minutes = remaining // 60
            seconds = remaining % 60
            await update.message.reply_text(f"⏱ Remaining shutdown time: {minutes} min {seconds} sec")
        else:
            shutdown_timer = None
            await update.message.reply_text("There's no active shutdown right now.")
    else:
        await update.message.reply_text("No shutdown is scheduled.")

# Setup Bot
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Set slash commands
async def set_commands(app):
    await app.bot.set_my_commands([
        BotCommand("start", "Show main menu"),
        BotCommand("status", "Check shutdown timer"),
    ])

# Register handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("status", status))
app.add_handler(CallbackQueryHandler(handle_action, pattern="^(shutdown|confirm_shutdown|restart|sleep|hibernate|remove_shutdown|check_timer|back_to_main)$"))
app.add_handler(CallbackQueryHandler(handle_shutdown_time, pattern="^shutdown_"))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_custom_time))

print("Bot is running...")
app.post_init = set_commands
app.run_polling()
