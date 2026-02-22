import telebot
from yt_dlp import YoutubeDL
import os

API_TOKEN = '8511268793:AAEgpBhqAzAqJlAiTTft_Eu4iSMMxfAMODE'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "🤖 Online. Trimite link public de Insta.")

@bot.message_handler(func=lambda m: True)
def handle_download(message):
    if "instagram.com" in message.text:
        # Nu mai folosim reply_to ca sa evitam eroarea 400
        status = bot.send_message(message.chat.id, "⏳ Verific...")
        
        ydl_opts = {
            'outtmpl': 'file_%(id)s.%(ext)s',
            'quiet': True,
            'writethumbnail': True,
            'nocheckcertificate': True,
            'geo_bypass': True, # Incearca sa ocoleasca blocajele regionale
            'user_agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1'
        }
        
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(message.text, download=True)
                filename = ydl.prepare_filename(info)

            # Fix extensie poze
            if not os.path.exists(filename):
                for ext in ['.jpg', '.png', '.jpeg']:
                    if os.path.exists(os.path.splitext(filename)[0] + ext):
                        filename = os.path.splitext(filename)[0] + ext
                        break

            with open(filename, 'rb') as f:
                if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                    bot.send_photo(message.chat.id, f)
                else:
                    bot.send_video(message.chat.id, f)
            
            os.remove(filename)
        except Exception as e:
            bot.send_message(message.chat.id, "❌ Instagram a blocat conexiunea. Serverul este momentan restrictionat.")
    else:
        bot.send_message(message.chat.id, "⚠️ Link invalid.")

bot.infinity_polling()
