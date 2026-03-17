import discord
from discord.ext import commands
import os
import google.genai as genai
from flask import Flask, request, render_template_string
from threading import Thread
import asyncio

app = Flask('')

# Danh sách để quản lý các bot đang chạy (để tránh chạy đè lên nhau)
running_bots = {}

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Nhutcoder Multi-Bot Manager</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: sans-serif; text-align: center; padding: 20px; background: #f4f4f9; }
        .card { background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); max-width: 400px; margin: auto; }
        input { width: 90%; padding: 10px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; }
        button { background: #5865F2; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
        button:hover { background: #4752c4; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🚀 Discord AI Bot Runner</h2>
        <p>Nhập thông tin để kích hoạt bot của bạn</p>
        <form method="POST" action="/run-bot">
            <input type="text" name="token" placeholder="Discord Bot Token" required><br>
            <input type="text" name="gemini_key" placeholder="Gemini API Key" required><br>
            <button type="submit">Kích hoạt Bot</button>
        </form>
        <div id="status"></div>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_FORM)

# Hàm logic của Bot Discord
def run_discord_bot(token, gemini_key):
    try:
        # Thiết lập Gemini cho luồng này
        client = genai.Client(api_key=gemini_key)
        
        intents = discord.Intents.default()
        intents.message_content = True
        bot = commands.Bot(command_prefix='!', intents=intents)

        @bot.event
        async def on_ready():
            print(f'✅ Bot {bot.user} đã Online!')

        @bot.command()
        async def ask(ctx, *, prompt):
            try:
                response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
                await ctx.reply(response.text)
            except Exception as e:
                await ctx.send(f"❌ Lỗi Gemini: {e}")

        # Chạy bot (Mỗi bot chạy trong một Event Loop riêng của luồng đó)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        bot.run(token)
    except Exception as e:
        print(f"❌ Lỗi khi chạy bot: {e}")

@app.route('/run-bot', methods=['POST'])
def handle_run():
    token = request.form.get('token')
    key = request.form.get('gemini_key')

    if token in running_bots:
        return "⚠️ Bot với Token này đã đang chạy rồi!"

    # Tạo một luồng mới cho bot của người dùng này
    t = Thread(target=run_discord_bot, args=(token, key))
    t.daemon = True
    t.start()
    
    running_bots[token] = t
    return f"<h3>🔥 Đang khởi tạo bot...</h3><p>Hãy kiểm tra Discord của bạn sau vài giây!</p><a href='/'>Quay lại</a>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
