import discord
from discord.ext import commands
from discord import app_commands
import os
import google.generativeai as genai
from flask import Flask, request, render_template_string, jsonify
from threading import Thread
import asyncio
from datetime import datetime

app = Flask('')

# Quản lý trạng thái
running_bots = {} 
bot_logs = {}

def add_log(token, message):
    time_str = datetime.now().strftime("%H:%M:%S")
    if token not in bot_logs: bot_logs[token] = []
    bot_logs[token].append(f"[{time_str}] {message}")
    if len(bot_logs[token]) > 10: bot_logs[token].pop(0)

HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Nhutcoder AI System</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Inter', sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; }
        .container { width: 100%; max-width: 500px; background: #1e293b; padding: 25px; border-radius: 16px; border: 1px solid #334155; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); }
        h2 { color: #38bdf8; text-align: center; margin-top: 0; display: flex; align-items: center; justify-content: center; gap: 10px; }
        .label { font-size: 0.8rem; color: #94a3b8; margin-bottom: 4px; display: block; }
        input, textarea { width: 100%; padding: 12px; margin-bottom: 12px; border-radius: 8px; border: 1px solid #334155; background: #0f172a; color: white; box-sizing: border-box; font-size: 14px; }
        .btn-group { display: flex; gap: 10px; }
        button { flex: 1; padding: 12px; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; transition: 0.2s; }
        .btn-run { background: #0284c7; color: white; }
        .btn-stop { background: #ef4444; color: white; }
        .log-box { background: #000; color: #10b981; padding: 10px; border-radius: 8px; font-family: 'Courier New', monospace; font-size: 12px; height: 120px; overflow-y: auto; margin-top: 15px; border: 1px solid #334155; }
        .footer { margin-top: 20px; font-size: 0.8rem; color: #64748b; text-align: center; }
        .svg-icon { width: 18px; height: 18px; fill: currentColor; }
    </style>
</head>
<body>
    <div class="container">
        <h2>
            <svg class="svg-icon" viewBox="0 0 24 24"><path d="M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22A10,10 0 0,1 2,12A10,10 0 0,1 12,2M12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4M12,6A6,6 0 0,1 18,12A6,6 0 0,1 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6M12,8A4,4 0 0,0 8,12A4,4 0 0,0 12,16A4,4 0 0,0 16,12A4,4 0 0,0 12,8Z"/></svg>
            Nhutcoder AI System
        </h2>
        <form id="botForm">
            <span class="label">Discord Token</span>
            <input type="password" id="token" name="token" required>
            <span class="label">Gemini API Key</span>
            <input type="password" id="gemini_key" name="gemini_key" required>
            <span class="label">Từ khóa AI</span>
            <input type="text" id="trigger" name="trigger" placeholder="Ví dụ: AI" required>
            <span class="label">Chữ mặc định (Khi không dùng AI)</span>
            <textarea id="default_text" name="default_text" rows="2"></textarea>
            
            <div class="btn-group">
                <button type="button" class="btn-run" onclick="actionBot('run')">
                    <svg class="svg-icon" viewBox="0 0 24 24"><path d="M8,5V19L19,12L8,5Z"/></svg> Chạy Bot
                </button>
                <button type="button" class="btn-stop" onclick="actionBot('stop')">
                    <svg class="svg-icon" viewBox="0 0 24 24"><path d="M18,18H6V6H18V18Z"/></svg> Tắt Bot
                </button>
            </div>
        </form>
        <div class="log-box" id="logs">Sẵn sàng chờ lệnh...</div>
        <div class="footer">Powered By Nhutcoder © 2026</div>
    </div>
    <script>
        function actionBot(type) {
            const formData = new FormData(document.getElementById('botForm'));
            fetch('/' + type + '-bot', { method: 'POST', body: formData })
            .then(res => res.json()).then(data => alert(data.message));
        }
        setInterval(() => {
            const t = document.getElementById('token').value;
            if(t) fetch('/get-logs?token=' + t).then(res => res.json())
            .then(data => { if(data.logs) document.getElementById('logs').innerHTML = data.logs.join('<br>'); });
        }, 2000);
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

async def start_bot(token, key, trigger, default):
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-3.0-flash')
        bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

        # --- TÍNH NĂNG SPAM NẰM Ở ĐÂY ---
        @bot.tree.command(name="spamall", description="Spam tin nhắn hàng loạt chuyên nghiệp")
        @app_commands.describe(count="Số lần", content="Nội dung")
        async def spamall(interaction: discord.Interaction, count: int, content: str):
            await interaction.response.send_message(f"Nhutcoder Tool: Đang spam {count} lần...", ephemeral=True)
            add_log(token, f"Đang chạy spam cho {interaction.user}")
            limit = min(count, 100000) 
            for _ in range(limit):
                await interaction.channel.send(content)
                await asyncio.sleep(0.5)

        @bot.event
        async def on_ready():
            await bot.tree.sync()
            add_log(token, f"Bot {bot.user} đã Online!")

        @bot.event
        async def on_message(message):
            if message.author.bot: return
            if trigger.lower() in message.content.lower():
                add_log(token, f"AI đang trả lời {message.author}")
                query = message.content.lower().replace(trigger.lower(), "").strip()
                res = model.generate_content(query)
                await message.reply(res.text)
            elif default:
                await message.reply(default)

        running_bots[token] = bot
        await bot.start(token)
    except Exception as e:
        add_log(token, f"Lỗi: {str(e)}")

@app.route('/run-bot', methods=['POST'])
def handle_run():
    t, k, tr, df = request.form.get('token'), request.form.get('gemini_key'), request.form.get('trigger'), request.form.get('default_text')
    if t in running_bots: return jsonify({"message": "Bot đang chạy rồi!"})
    add_log(t, "Khởi động...")
    Thread(target=lambda: asyncio.run(start_bot(t, k, tr, df)), daemon=True).start()
    return jsonify({"message": "Đã gửi lệnh chạy!"})

@app.route('/stop-bot', methods=['POST'])
def handle_stop():
    t = request.form.get('token')
    if t in running_bots:
        # Cách tắt bot an toàn cho Pydroid/Render
        bot_to_stop = running_bots[t]
        asyncio.run_coroutine_threadsafe(bot_to_stop.close(), asyncio.get_event_loop())
        del running_bots[t]
        add_log(t, "Đã tắt bot.")
        return jsonify({"message": "Đã tắt bot!"})
    return jsonify({"message": "Không tìm thấy bot đang chạy."})

@app.route('/get-logs')
def get_logs():
    return jsonify({"logs": bot_logs.get(request.args.get('token'), ["Đang chờ..."])})

if __name__ == "__main__":
    # Pydroid dùng port 5000, Render dùng 10000
    app.run(host='0.0.0.0', port=10000)
