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

# Hệ thống quản lý dữ liệu bot
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
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0b0e14; color: #e2e8f0; margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; }
        .container { width: 100%; max-width: 480px; background: #161b22; padding: 30px; border-radius: 12px; border: 1px solid #30363d; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        h2 { color: #58a6ff; text-align: center; margin-top: 0; display: flex; align-items: center; justify-content: center; gap: 12px; font-weight: 600; }
        .label { font-size: 13px; color: #8b949e; margin-bottom: 6px; display: block; font-weight: 500; }
        input, textarea { width: 100%; padding: 12px; margin-bottom: 16px; border-radius: 6px; border: 1px solid #30363d; background: #0d1117; color: #c9d1d9; box-sizing: border-box; font-size: 14px; outline: none; }
        input:focus { border-color: #58a6ff; }
        .btn-group { display: flex; gap: 12px; margin-top: 8px; }
        button { flex: 1; padding: 14px; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 10px; transition: 0.2s; font-size: 14px; }
        .btn-run { background: #238636; color: white; }
        .btn-run:hover { background: #2ea043; }
        .btn-stop { background: #da3633; color: white; }
        .btn-stop:hover { background: #f85149; }
        .log-header { font-size: 12px; color: #8b949e; margin-top: 20px; margin-bottom: 5px; display: flex; align-items: center; gap: 5px; }
        .log-box { background: #0d1117; color: #39ff14; padding: 12px; border-radius: 6px; font-family: 'Consolas', 'Monaco', monospace; font-size: 12px; height: 130px; overflow-y: auto; border: 1px solid #30363d; line-height: 1.5; }
        .footer { margin-top: 25px; font-size: 12px; color: #484f58; text-align: center; border-top: 1px solid #30363d; padding-top: 15px; width: 100%; }
        .svg-icon { width: 20px; height: 20px; fill: currentColor; }
    </style>
</head>
<body>
    <div class="container">
        <h2>
            <svg class="svg-icon" viewBox="0 0 24 24"><path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4M12,6A6,6 0 0,0 6,12A6,6 0 0,0 12,18A6,6 0 0,0 18,12A6,6 0 0,0 12,6M12,8A4,4 0 0,1 16,12A4,4 0 0,1 12,16A4,4 0 0,1 8,12A4,4 0 0,1 12,8Z"/></svg>
            Nhutcoder AI System
        </h2>
        <form id="botForm">
            <span class="label">Discord Bot Token</span>
            <input type="password" id="token" name="token" required placeholder="Nhập token tại đây...">
            <span class="label">Gemini API Key</span>
            <input type="password" id="gemini_key" name="gemini_key" required placeholder="Nhập API key...">
            <span class="label">Từ khóa kích hoạt AI</span>
            <input type="text" id="trigger" name="trigger" value="AI" required>
            <span class="label">Phản hồi mặc định (Khi không dùng AI)</span>
            <textarea id="default_text" name="default_text" rows="2" placeholder="Ví dụ: Đang chờ lệnh từ Nhutcoder..."></textarea>
            
            <div class="btn-group">
                <button type="button" class="btn-run" onclick="actionBot('run')">
                    <svg class="svg-icon" viewBox="0 0 24 24"><path d="M8,5.14V19.14L19,12.14L8,5.14Z"/></svg> Kích hoạt
                </button>
                <button type="button" class="btn-stop" onclick="actionBot('stop')">
                    <svg class="svg-icon" viewBox="0 0 24 24"><path d="M18,18H6V6H18V18Z"/></svg> Ngừng chạy
                </button>
            </div>
        </form>

        <div class="log-header">
            <svg style="width:14px;height:14px" viewBox="0 0 24 24"><path fill="currentColor" d="M13,9H11V7H13M13,17H11V11H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z"/></svg>
            Bảng điều khiển Log
        </div>
        <div class="log-box" id="logs">Sẵn sàng...</div>
        
        <div class="footer">
            Powered By Nhutcoder &copy; 2026
        </div>
    </div>

    <script>
        function actionBot(type) {
            const formData = new FormData(document.getElementById('botForm'));
            fetch('/' + type + '-bot', { method: 'POST', body: formData })
            .then(res => res.json()).then(data => console.log(data.message));
        }

        setInterval(() => {
            const t = document.getElementById('token').value;
            if(t) {
                fetch('/get-logs?token=' + t).then(res => res.json())
                .then(data => { if(data.logs) document.getElementById('logs').innerHTML = data.logs.join('<br>'); });
            }
        }, 2000);
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

async def start_bot_process(token, key, trigger, default):
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-3.1-pro')
        bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

        # Lệnh Spam Toàn Cầu
        @bot.tree.command(name="spamall", description="Lệnh spam chuyên dụng của Nhutcoder")
        async def spamall(interaction: discord.Interaction, count: int, content: str):
            await interaction.response.send_message("Hệ thống đang thực hiện lệnh spam...", ephemeral=True)
            add_log(token, f"Lệnh spam thực thi tại: {interaction.guild.name}")
            limit = min(count, 1000000000000)
            for _ in range(limit):
                await interaction.channel.send(content)
                await asyncio.sleep(0.5)

        @bot.event
        async def on_ready():
            await bot.tree.sync()
            add_log(token, f"Bot {bot.user} đã trực tuyến.")

        @bot.event
        async def on_message(message):
            if message.author.bot: return
            if trigger.lower() in message.content.lower():
                add_log(token, f"Xử lý AI cho {message.author}")
                query = message.content.lower().replace(trigger.lower(), "").strip()
                res = model.generate_content(query)
                await message.reply(res.text)
            elif default:
                await message.reply(default)

        running_bots[token] = bot
        await bot.start(token)
    except Exception as e:
        add_log(token, f"Lỗi hệ thống: {str(e)}")

@app.route('/run-bot', methods=['POST'])
def handle_run():
    t, k, tr, df = request.form.get('token'), request.form.get('gemini_key'), request.form.get('trigger'), request.form.get('default_text')
    if t in running_bots: return jsonify({"message": "Đang chạy"})
    add_log(t, "Đang khởi tạo kết nối...")
    Thread(target=lambda: asyncio.run(start_bot_process(t, k, tr, df)), daemon=True).start()
    return jsonify({"message": "Khởi động thành công"})

@app.route('/stop-bot', methods=['POST'])
def handle_stop():
    t = request.form.get('token')
    if t in running_bots:
        asyncio.run_coroutine_threadsafe(running_bots[t].close(), asyncio.get_event_loop())
        del running_bots[t]
        add_log(t, "Tiến trình đã dừng.")
        return jsonify({"message": "Đã tắt"})
    return jsonify({"message": "Không tìm thấy bot"})

@app.route('/get-logs')
def get_logs():
    return jsonify({"logs": bot_logs.get(request.args.get('token'), ["Trống"])})

if __name__ == "__main__":
    # Dùng port 10000 cho Render, sửa thành 5000 nếu test Pydroid
    app.run(host='0.0.0.0', port=10000)
