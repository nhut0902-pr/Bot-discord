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
running_bots = {} 
bot_logs = {}

def add_log(token, message):
    time_str = datetime.now().strftime("%H:%M:%S")
    if token not in bot_logs: bot_logs[token] = []
    bot_logs[token].append(f"[{time_str}] {message}")
    if len(bot_logs[token]) > 15: bot_logs[token].pop(0)

HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Nhutcoder AI System v3.1</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0b0e14; color: #e2e8f0; margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; }
        .container { width: 100%; max-width: 500px; background: #161b22; padding: 30px; border-radius: 12px; border: 1px solid #30363d; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        h2 { color: #58a6ff; text-align: center; margin-top: 0; display: flex; align-items: center; justify-content: center; gap: 12px; }
        .label { font-size: 13px; color: #8b949e; margin-bottom: 6px; display: block; }
        input, textarea { width: 100%; padding: 12px; margin-bottom: 16px; border-radius: 6px; border: 1px solid #30363d; background: #0d1117; color: #c9d1d9; box-sizing: border-box; outline: none; }
        .btn-group { display: flex; gap: 12px; }
        button { flex: 1; padding: 14px; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; transition: 0.2s; }
        .btn-run { background: #238636; color: white; }
        .btn-stop { background: #da3633; color: white; }
        .log-box { background: #0d1117; color: #39ff14; padding: 12px; border-radius: 6px; font-family: monospace; font-size: 12px; height: 150px; overflow-y: auto; border: 1px solid #30363d; margin-top: 15px; line-height: 1.6; }
        .footer { margin-top: 25px; font-size: 11px; color: #484f58; text-align: center; border-top: 1px solid #30363d; padding-top: 15px; }
        .svg-icon { width: 20px; height: 20px; fill: #58a6ff; }
    </style>
</head>
<body>
    <div class="container">
        <h2>
            <svg class="svg-icon" viewBox="0 0 24 24"><path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4Z"/></svg>
            Nhutcoder AI Premium
        </h2>
        <form id="botForm">
            <span class="label">Discord Token</span>
            <input type="password" id="token" name="token" required>
            <span class="label">Gemini API Key</span>
            <input type="password" id="gemini_key" name="gemini_key" required>
            <span class="label">Từ khóa AI</span>
            <input type="text" id="trigger" name="trigger" value="AI">
            <span class="label">Phản hồi mặc định</span>
            <textarea id="default_text" name="default_text" rows="2"></textarea>
            <div class="btn-group">
                <button type="button" class="btn-run" onclick="actionBot('run')">Kích hoạt Hệ thống</button>
                <button type="button" class="btn-stop" onclick="actionBot('stop')">Dừng hoạt động</button>
            </div>
        </form>
        <div class="log-box" id="logs">Sẵn sàng thực thi...</div>
        <div class="footer">Phát triển bởi Nhutcoder &copy; 2026 - v3.1 Flash</div>
    </div>
    <script>
        function actionBot(type) {
            const formData = new FormData(document.getElementById('botForm'));
            fetch('/' + type + '-bot', { method: 'POST', body: formData });
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

async def start_bot_process(token, key, trigger, default):
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-3.1-flash')
        bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

        # --- LỆNH TRA CỨU NGOÀI ---
        @bot.tree.command(name="search", description="Tìm kiếm thông tin tổng hợp từ AI")
        async def search(interaction: discord.Interaction, query: str):
            await interaction.response.send_message(f"Dang truy xuat: {query}", ephemeral=True)
            res = model.generate_content(f"Tom tat ngan gon thong tin ve: {query}")
            embed = discord.Embed(title="Ket qua tim kiem", description=res.text, color=0x58a6ff)
            await interaction.channel.send(embed=embed)

        @bot.tree.command(name="wiki", description="Tra cuu dinh nghia Wikipedia")
        async def wiki(interaction: discord.Interaction, subject: str):
            await interaction.response.send_message(f"Tra cuu thu vien: {subject}", ephemeral=True)
            res = model.generate_content(f"Dinh nghia ngan gon ve '{subject}' theo phong cach Wikipedia")
            await interaction.channel.send(f"**Dinh nghia {subject}:**\n{res.text}")

        @bot.tree.command(name="weather", description="Xem thoi tiet tinh thanh")
        async def weather(interaction: discord.Interaction, city: str):
            await interaction.response.send_message(f"Kiem tra thoi tiet: {city}", ephemeral=True)
            res = model.generate_content(f"Thoi tiet hien tai tai {city}. Ngan gon: Nhiet do, trang thai.")
            await interaction.channel.send(f"**Thoi tiet {city}:**\n{res.text}")

        # --- LỆNH QUẢN TRỊ ---
        @bot.tree.command(name="clear", description="Xoa tin nhan")
        async def clear(interaction: discord.Interaction, amount: int):
            if not interaction.user.guild_permissions.manage_messages:
                return await interaction.response.send_message("Thieu quyen.", ephemeral=True)
            await interaction.response.send_message(f"Dang xoa {amount} tin nhan...", ephemeral=True)
            await interaction.channel.purge(limit=amount)

        @bot.tree.command(name="kick", description="Kick thanh vien")
        async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "Vi pham"):
            if not interaction.user.guild_permissions.kick_members:
                return await interaction.response.send_message("Thieu quyen.", ephemeral=True)
            await member.kick(reason=reason)
            await interaction.response.send_message(f"Da Kick: {member.name}")

        @bot.tree.command(name="ban", description="Ban thanh vien")
        async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "Vi pham"):
            if not interaction.user.guild_permissions.ban_members:
                return await interaction.response.send_message("Thieu quyen.", ephemeral=True)
            await member.ban(reason=reason)
            await interaction.response.send_message(f"Da Ban: {member.name}")

        # --- LỆNH HỆ THỐNG & SPAM ---
        @bot.tree.command(name="infobot", description="Thong so he thong")
        async def infobot(interaction: discord.Interaction):
            ping = round(bot.latency * 1000)
            await interaction.response.send_message(f"Ping: {ping}ms | Server: {len(bot.guilds)} | Model: Gemini 3.1 Flash")

        @bot.tree.command(name="say", description="Bot noi ho")
        async def say(interaction: discord.Interaction, content: str):
            await interaction.response.send_message("Da gui", ephemeral=True)
            await interaction.channel.send(content)

        @bot.tree.command(name="spamall", description="Tool spam chuyen nghiep")
        async def spamall(interaction: discord.Interaction, count: int, content: str):
            await interaction.response.send_message("Trien khai...", ephemeral=True)
            for _ in range(min(count, 50)):
                await interaction.channel.send(content)
                await asyncio.sleep(0.5)

        @bot.event
        async def on_ready():
            await bot.tree.sync()
            add_log(token, f"He thong {bot.user} v3.1 Online")

        @bot.event
        async def on_message(message):
            if message.author.bot: return
            if trigger.lower() in message.content.lower():
                prompt = message.content.lower().replace(trigger.lower(), "").strip()
                if not prompt: return
                async with message.channel.typing():
                    try:
                        res = model.generate_content(prompt)
                        await message.reply(res.text)
                    except Exception as e:
                        add_log(token, f"Loi AI: {str(e)}")
            elif default:
                await message.reply(default)
            await bot.process_commands(message)

        running_bots[token] = bot
        await bot.start(token)
    except Exception as e:
        add_log(token, f"Loi: {str(e)}")

@app.route('/run-bot', methods=['POST'])
def handle_run():
    t, k, tr, df = request.form.get('token'), request.form.get('gemini_key'), request.form.get('trigger'), request.form.get('default_text')
    if t in running_bots: return jsonify({"status": "exists"})
    add_log(t, "Khoi tao phien ban v3.1 Flash...")
    Thread(target=lambda: asyncio.run(start_bot_process(t, k, tr, df)), daemon=True).start()
    return jsonify({"status": "ok"})

@app.route('/stop-bot', methods=['POST'])
def handle_stop():
    t = request.form.get('token')
    if t in running_bots:
        asyncio.run_coroutine_threadsafe(running_bots[t].close(), asyncio.get_event_loop())
        del running_bots[t]
        add_log(t, "He thong da dung.")
    return jsonify({"status": "ok"})

@app.route('/get-logs')
def get_logs():
    return jsonify({"logs": bot_logs.get(request.args.get('token'), ["Dang cho..."])})

@app.route('/ping')
def ping():
    return "PONG", 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
