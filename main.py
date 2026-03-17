import discord
from discord.ext import commands
import os
import google.generativeai as genai
from flask import Flask, request, render_template_string
from threading import Thread

# --- CẤU HÌNH WEB QUẢN LÝ ---
app = Flask('')

# Giao diện HTML đơn giản để nhập Key
HTML_FORM = '''
<!DOCTYPE html>
<html>
<head><title>Nhutcoder Bot Manager</title></head>
<body>
    <h2>Cài đặt Bot của Nhutcoder</h2>
    <form method="POST" action="/update">
        <label>Discord Token:</label><br>
        <input type="text" name="discord_token" style="width:300px"><br><br>
        <label>Gemini API Key:</label><br>
        <input type="text" name="gemini_key" style="width:300px"><br><br>
        <button type="submit">Cập nhật & Khởi chạy</button>
    </form>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_FORM)

@app.route('/update', methods=['POST'])
def update():
    d_token = request.form.get('discord_token')
    g_key = request.form.get('gemini_key')
    
    # Ở đây bạn có thể lưu vào file hoặc khởi chạy bot trực tiếp
    # Lưu ý: Trên Render, việc khởi chạy lại bot từ web cần kỹ thuật xử lý luồng (Thread)
    return "Đã nhận thông tin! Hãy kiểm tra log hệ thống."

def run_web():
    app.run(host='0.0.0.0', port=8080)

# --- CẤU HÌNH BOT DISCORD + GEMINI ---
def start_bot(discord_token, gemini_key):
    genai.configure(api_key=gemini_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        print(f'Bot {bot.user} đã trực tuyến!')

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        
        # Nếu tin nhắn bắt đầu bằng !ask, bot sẽ dùng Gemini trả lời
        if message.content.startswith('!ask '):
            prompt = message.content[5:]
            response = model.generate_content(prompt)
            await message.reply(response.text)

        await bot.process_commands(message)

    bot.run(discord_token)

# Chạy Web server ở luồng riêng
Thread(target=run_web).start()
