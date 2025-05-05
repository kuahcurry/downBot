# ⚡ downBot: Remote PC Shutdown & Power Control via Telegram

Ever wished you could shut down your PC from your bed?  
Now you can. **downBot** is a Telegram bot that lets you control your Windows computer's power state remotely whether its shutdown, restart, sleep, or hibernate — all from a simple tap in Telegram. Oh, and yes, she even comes with timers and cancel buttons. Pretty cool for a small insignificant project, no?

---

## ✨ Features

- 🛑 Schedule or trigger **immediate shutdown**
- 🔁 **Restart** your PC with one tap
- 😴 Put your system to **Sleep** or 🌙 **Hibernate**
- ⏳ **Set shutdown timer**: 10, 20, 30 minutes or custom input
- ❌ **Cancel shutdown** if you change your mind
- 🔐 **Authorization** system so only you can use it

---

## 🚀 Getting Started

### 1. Requirements
- Windows PC
- Python 3.10+
- Telegram account

### 2. 🛠 Installation

All you need to do is:

1. **Download the release version**  
   You'll get a file with the `.pyw` extension.

2. **Open the file using a code editor**  
   _⚠️ Do **not** double-click it._ If you do, it’ll just flash a CMD window and fail silently.

3. **Edit your credentials**  
   Replace the placeholder values with your own **Bot Token** and **User ID**.

---

### 🔧 How to Get Your Telegram Bot Token and User ID

#### 🪄 A. Create Your Bot
1. Open Telegram and search for [`@BotFather`](https://t.me/BotFather).
2. Type `/newbot` and follow the instructions to name and create your bot.
3. Once created, BotFather will give you a **Bot Token** — copy that!

#### 👤 B. Get Your Telegram User ID
1. Go to [@userinfobot](https://t.me/userinfobot) on Telegram.
2. Start the bot — it will reply with your **User ID**.

Once you have both, open the `.pyw` file and look for:

```python
BOT_TOKEN = 'your-telegram-bot-token-here'
AUTHORIZED_USER = 123456789  # your Telegram user ID
```

Replace the values with yours, save the file, and run the bot with just a double click and Voila!  
Your personal shutdown bot is ready to use!
