import discord
from discord.ext import commands
import os
import google.generativeai as genai
from flask import Flask, request, render_template_string
from threading import Thread
import asyncio

app = Flask('')
running_bots = {}

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>AI Bot System - Nhutcoder</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: white; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .card { background: #1e293b; padding: 2rem; border-radius: 1rem; width: 100%; max-width: 400px; border: 1px solid #334155; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.5); }
        h2 { color: #38bdf8; text-align: center; margin-bottom: 1.5rem; }
        input { width: 100%; padding: 0.75rem; margin-bottom: 1rem; border-radius: 0.5rem; border: 1px solid #334155; background: #0f172a; color: white; box-sizing: border-box; }
        button { width: 100%; padding: 0.75rem; background: #0284c7; color: white; border: none; border-radius: 0.5rem; font-weight: bold; cursor: pointer; }
        button:hover { background: #0369a1; }
        .label { font-size: 0.85rem; color: #94a3b8; margin-bottom: 0.3rem; display: block; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Nhutcoder AI Tool</h2>
        <form method="POST" action="/run-bot">
            <span class="label">Discord Token</span>
            <input type="password" name="token" required>
            <span class="label">Gemini API Key</span>
            <input type="password" name="gemini_key" required>
            <span class="label">Từ khóa kích hoạt (Tránh tốn Token)</span>
            <input type="text" name="trigger" placeholder="Ví dụ: AI, Bot, @TenBot..." required>
            <button type="submit">Kích hoạt ngay</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_FORM)

async def start_bot_logic(token, gemini_key, trigger):
    try:
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        intents = discord.Intents.default()
        intents.message_content = True
        bot = commands.Bot(command_prefix='!', intents=intents)

        @bot.event
        async def on_message(message):
            if message.author.bot: return

            # KIỂM TRA TỪ KHÓA ĐỂ TRÁNH SPAM TỐN TOKEN
            if trigger.lower() in message.content.lower():
                # Loại bỏ từ khóa khỏi câu hỏi để AI trả lời chuẩn
                query = message.content.lower().replace(trigger.lower(), "").strip()
                if query:
                    async with message.channel.typing():
                        try:
                            response = model.generate_content(query)
                            await message.reply(response.text)
                            await asyncio.sleep(1) # Cooldown nhẹ
                        except Exception as e:
                            print(f"Lỗi API: {e}")

        await bot.start(token)
    except Exception as e:
        print(f"Lỗi: {e}")

def run_loop(t, k, tr):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_bot_logic(t, k, tr))

@app.route('/run-bot', methods=['POST'])
def handle_run():
    t = request.form.get('token')
    k = request.form.get('gemini_key')
    tr = request.form.get('trigger')
    
    thread = Thread(target=run_loop, args=(t, k, tr))
    thread.daemon = True
    thread.start()
    return f"<h3>✅ Đã chạy bot!</h3><p>Từ khóa kích hoạt: <b>{tr}</b></p><a href='/'>Quay lại</a>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
