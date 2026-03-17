import discord
from discord.ext import commands
from discord import app_commands
import os
import google.generativeai as genai
from flask import Flask, request, render_template_string
from threading import Thread
import asyncio

app = Flask('')
running_bots = {}

# Giao diện Web chuyên nghiệp cho Nhutcoder
HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Nhutcoder AI System</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: white; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }
        .card { background: #1e293b; padding: 2rem; border-radius: 1rem; width: 100%; max-width: 450px; border: 1px solid #334155; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); }
        h2 { color: #38bdf8; text-align: center; margin-bottom: 1.5rem; }
        .label { font-size: 0.85rem; color: #94a3b8; margin-bottom: 0.3rem; display: block; }
        input, textarea { width: 100%; padding: 0.75rem; margin-bottom: 1rem; border-radius: 0.5rem; border: 1px solid #334155; background: #0f172a; color: white; box-sizing: border-box; }
        button { width: 100%; padding: 1rem; background: #0284c7; color: white; border: none; border-radius: 0.5rem; font-weight: bold; cursor: pointer; transition: 0.3s; }
        button:hover { background: #0369a1; }
    </style>
</head>
<body>
    <div class="card">
        <h2> AI Bot Manager</h2>
        <form method="POST" action="/run-bot">
            <span class="label">Discord Token</span>
            <input type="password" name="token" required>
            <span class="label">Gemini API Key</span>
            <input type="password" name="gemini_key" required>
            <span class="label">Từ khóa kích hoạt AI (VD: Bot)</span>
            <input type="text" name="trigger" placeholder="Chat kèm từ này mới dùng AI" required>
            <span class="label">Câu trả lời mặc định (Khi không dùng AI)</span>
            <textarea name="default_text" rows="2" placeholder="VD: Chào bạn, tôi là bot của Nhutcoder!"></textarea>
            <button type="submit">Kích hoạt Tool</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_FORM)

async def start_bot_logic(token, gemini_key, trigger, default_text):
    try:
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        intents = discord.Intents.default()
        intents.message_content = True
        bot = commands.Bot(command_prefix='!', intents=intents)

        # Lệnh Slash Command /spamall chuẩn (Không bị lỗi đỏ)
        @bot.tree.command(name="spamall", description="Spam tin nhắn hàng loạt")
        async def spamall(interaction: discord.Interaction, count: int, content: str):
            await interaction.response.send_message(f"✅ Đang thực hiện...", ephemeral=True)
            limit = min(count, 100000) # Giới hạn 30 lần để an toàn
            for _ in range(limit):
                await interaction.channel.send(content)
                await asyncio.sleep(0.6)

        @bot.event
        async def on_ready():
            await bot.tree.sync() # Đồng bộ lệnh /
            print(f'Bot Online: {bot.user}')

        @bot.event
        async def on_message(message):
            if message.author.bot: return

            # Nếu có từ khóa -> Dùng AI
            if trigger.lower() in message.content.lower():
                query = message.content.lower().replace(trigger.lower(), "").strip()
                if query:
                    async with message.channel.typing():
                        try:
                            response = model.generate_content(query)
                            await message.reply(response.text)
                        except Exception as e:
                            await message.reply(f"Lỗi AI: {e}")
            
            # Nếu KHÔNG có từ khóa -> Trả lời bằng "Chữ" mặc định đã cài trên Web
            else:
                if default_text:
                    await message.reply(default_text)

        await bot.start(token)
    except Exception as e:
        print(f" Lỗi: {e}")

def run_it(t, k, tr, df):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_bot_logic(t, k, tr, df))

@app.route('/run-bot', methods=['POST'])
def handle():
    t = request.form.get('token')
    k = request.form.get('gemini_key')
    tr = request.form.get('trigger')
    df = request.form.get('default_text')
    
    thread = Thread(target=run_it, args=(t, k, tr, df))
    thread.daemon = True
    thread.start()
    return f"<h3> Bot đã chạy!</h3><p>Từ khóa: {tr}</p><a href='/'>Quay lại</a>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
