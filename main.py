import telebot
from yt_dlp import YoutubeDL
import os

# Acesta este token-ul tau
API_TOKEN = '8511268793:AAEgpBhqAzAqJlAiTTft_Eu4iSMMxfAMODE'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "✅ Salut! Sunt botul tău privat. Trimite-mi un link de Instagram.")

@bot.message_handler(func=lambda m: True)
def download(message):
    if "instagram.com" in message.text:
        msg = bot.reply_to(message, "⏳ Descarc video-ul...")
        try:
            ydl_opts = {'format': 'best', 'outtmpl': 'video.mp4', 'quiet': True}
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([message.text])
            with open('video.mp4', 'rb') as v:
                bot.send_video(message.chat.id, v)
            os.remove('video.mp4')
            bot.delete_message(message.chat.id, msg.message_id)
        except:
            bot.edit_message_text("❌ Eroare! Link-ul trebuie să fie public.", message.chat.id, msg.message_id)

bot.infinity_polling()
