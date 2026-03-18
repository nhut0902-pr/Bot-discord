import discord
from discord.ext import commands
import os
import google.generativeai as genai
from flask import Flask, request, render_template_string, jsonify
from threading import Thread
import asyncio
from datetime import datetime

app = Flask('')

# Biến lưu trữ trạng thái các bot
running_bots = {} 
bot_logs = {} # Lưu log cho từng bot

def add_log(token, message):
    time_str = datetime.now().strftime("%H:%M:%S")
    if token not in bot_logs: bot_logs[token] = []
    bot_logs[token].append(f"[{time_str}] {message}")
    if len(bot_logs[token]) > 10: bot_logs[token].pop(0)

HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Nhutcoder AI Management</title>
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
        .btn-run:hover { background: #0369a1; }
        .btn-stop { background: #ef4444; color: white; }
        .btn-stop:hover { background: #dc2626; }
        .log-box { background: #000; color: #10b981; padding: 10px; border-radius: 8px; font-family: 'Courier New', monospace; font-size: 12px; height: 120px; overflow-y: auto; margin-top: 15px; border: 1px solid #334155; }
        .footer { margin-top: 20px; font-size: 0.8rem; color: #64748b; text-align: center; }
        .svg-icon { width: 18px; height: 18px; fill: currentColor; }
    </style>
</head>
<body>
    <div class="container">
        <h2>
            <svg class="svg-icon" viewBox="0 0 24 24"><path d="M13,2V4H11V2H13M17,4L15.59,5.41L17,6.83L18.41,5.41L17,4M9,4L7.59,5.41L9,6.83L10.41,5.41L9,4M12,6A6,6 0 0,0 6,12C6,15.31 8.69,18 12,18A6,6 0 0,0 18,12C18,8.69 15.31,6 12,6M12,16A4,4 0 0,1 8,12A4,4 0 0,1 12,8A4,4 0 0,1 16,12A4,4 0 0,1 12,16M12,20V22H14V20H12M18,20L16.59,18.59L18,17.17L19.41,18.59L18,20M6,20L4.59,18.59L6,17.17L7.41,18.59L6,20Z"/></svg>
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
                    <svg class="svg-icon" viewBox="0 0 24 24"><path d="M8,5.14V19.14L19,12.14L8,5.14Z"/></svg> Chạy Bot
                </button>
                <button type="button" class="btn-stop" onclick="actionBot('stop')">
                    <svg class="svg-icon" viewBox="0 0 24 24"><path d="M18,18H6V6H18V18Z"/></svg> Tắt Bot
                </button>
            </div>
        </form>

        <div class="log-box" id="logs">Đang chờ lệnh...</div>
        <div class="footer">Powered By Nhutcoder © 2026</div>
    </div>

    <script>
        function actionBot(type) {
            const formData = new FormData(document.getElementById('botForm'));
            fetch('/' + type + '-bot', { method: 'POST', body: formData })
            .then(res => res.json())
            .then(data => alert(data.message));
        }

        setInterval(() => {
            const token = document.getElementById('token').value;
            if(token) {
                fetch('/get-logs?token=' + token)
                .then(res => res.json())
                .then(data => {
                    if(data.logs) document.getElementById('logs').innerHTML = data.logs.join('<br>');
                });
            }
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
        model = genai.GenerativeModel('gemini-1.5-flash')
        bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

        @bot.event
        async def on_ready():
            await bot.tree.sync()
            add_log(token, f"Bot {bot.user} đã Online!")

        @bot.event
        async def on_message(message):
            if message.author.bot: return
            if trigger.lower() in message.content.lower():
                add_log(token, f"Dùng AI cho: {message.author}")
                query = message.content.lower().replace(trigger.lower(), "").strip()
                res = model.generate_content(query)
                await message.reply(res.text)
            elif default:
                await message.reply(default)

        # Lưu bot vào dict để có thể tắt
        running_bots[token] = bot
        await bot.start(token)
    except Exception as e:
        add_log(token, f"Lỗi: {str(e)}")

@app.route('/run-bot', methods=['POST'])
def handle_run():
    t, k, tr, df = request.form.get('token'), request.form.get('gemini_key'), request.form.get('trigger'), request.form.get('default_text')
    if t in running_bots: return jsonify({"message": "Bot đang chạy rồi!"})
    add_log(t, "Đang khởi động...")
    Thread(target=lambda: asyncio.run(start_bot(t, k, tr, df)), daemon=True).start()
    return jsonify({"message": "Lệnh chạy đã gửi!"})

@app.route('/stop-bot', methods=['POST'])
def handle_stop():
    t = request.form.get('token')
    if t in running_bots:
        asyncio.run_coroutine_threadsafe(running_bots[t].close(), asyncio.get_event_loop())
        del running_bots[t]
        add_log(t, "Bot đã dừng.")
        return jsonify({"message": "Đã tắt bot!"})
    return jsonify({"message": "Bot không hoạt động."})

@app.route('/get-logs')
def get_logs():
    token = request.args.get('token')
    return jsonify({"logs": bot_logs.get(token, ["Trống"])})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
