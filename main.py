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
    if len(bot_logs[token]) > 12: bot_logs[token].pop(0)

HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Nhutcoder AI System v3.1</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #0b0e14; color: #e2e8f0; margin: 0; padding: 20px; display: flex; flex-direction: column; align-items: center; }
        .container { width: 100%; max-width: 480px; background: #161b22; padding: 30px; border-radius: 12px; border: 1px solid #30363d; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        h2 { color: #58a6ff; text-align: center; margin-top: 0; display: flex; align-items: center; justify-content: center; gap: 12px; }
        .label { font-size: 13px; color: #8b949e; margin-bottom: 6px; display: block; }
        input, textarea { width: 100%; padding: 12px; margin-bottom: 16px; border-radius: 6px; border: 1px solid #30363d; background: #0d1117; color: #c9d1d9; box-sizing: border-box; outline: none; }
        .btn-group { display: flex; gap: 12px; }
        button { flex: 1; padding: 14px; border: none; border-radius: 6px; font-weight: 600; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px; transition: 0.2s; }
        .btn-run { background: #238636; color: white; }
        .btn-stop { background: #da3633; color: white; }
        .log-box { background: #0d1117; color: #39ff14; padding: 12px; border-radius: 6px; font-family: monospace; font-size: 12px; height: 130px; overflow-y: auto; border: 1px solid #30363d; margin-top: 15px; }
        .footer { margin-top: 25px; font-size: 12px; color: #484f58; text-align: center; border-top: 1px solid #30363d; padding-top: 15px; width: 100%; }
        .svg-icon { width: 20px; height: 20px; fill: currentColor; }
    </style>
</head>
<body>
    <div class="container">
        <h2>
            <svg class="svg-icon" viewBox="0 0 24 24"><path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4Z"/></svg>
            Nhutcoder AI Management
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
                <button type="button" class="btn-run" onclick="actionBot('run')">Kích hoạt</button>
                <button type="button" class="btn-stop" onclick="actionBot('stop')">Tắt Bot</button>
            </div>
        </form>
        <div class="log-box" id="logs">Đang chờ tín hiệu...</div>
        <div class="footer">Powered By Nhutcoder &copy; 2026</div>
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

        # --- LỆNH QUẢN TRỊ ---
        @bot.tree.command(name="clear", description="Xóa tin nhắn trong kênh")
        async def clear(interaction: discord.Interaction, amount: int):
            if not interaction.user.guild_permissions.manage_messages:
                return await interaction.response.send_message("Thiếu quyền quản lý tin nhắn.", ephemeral=True)
            await interaction.response.send_message(f"Đang xử lý dọn dẹp {amount} tin nhắn...", ephemeral=True)
            deleted = await interaction.channel.purge(limit=amount)
            add_log(token, f"Xóa {len(deleted)} tin nhắn tại {interaction.guild.name}")

        @bot.tree.command(name="kick", description="Trục xuất thành viên")
        async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "Vi phạm nội quy"):
            if not interaction.user.guild_permissions.kick_members:
                return await interaction.response.send_message("Thiếu quyền Kick.", ephemeral=True)
            await member.kick(reason=reason)
            await interaction.response.send_message(f"Đã Kick: {member.name}. Lý do: {reason}")
            add_log(token, f"Kick thành viên: {member.name}")

        @bot.tree.command(name="ban", description="Cấm thành viên vĩnh viễn")
        async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "Vi phạm nghiêm trọng"):
            if not interaction.user.guild_permissions.ban_members:
                return await interaction.response.send_message("Thiếu quyền Ban.", ephemeral=True)
            await member.ban(reason=reason)
            await interaction.response.send_message(f"Đã Ban: {member.name}. Lý do: {reason}")
            add_log(token, f"Ban thành viên: {member.name}")

        # --- LỆNH HỆ THỐNG ---
        @bot.tree.command(name="infobot", description="Thông tin máy chủ Bot")
        async def infobot(interaction: discord.Interaction):
            ping = round(bot.latency * 1000)
            embed = discord.Embed(title="Nhutcoder System Info", color=0x58a6ff)
            embed.add_field(name="Độ trễ hệ thống", value=f"{ping}ms", inline=True)
            embed.add_field(name="Số lượng máy chủ", value=f"{len(bot.guilds)}", inline=True)
            embed.set_footer(text="Model: Gemini 3.1 Flash")
            await interaction.response.send_message(embed=embed)

        @bot.tree.command(name="say", description="Phát ngôn thông qua Bot")
        async def say(interaction: discord.Interaction, content: str):
            await interaction.response.send_message("Tin nhắn đã gửi.", ephemeral=True)
            await interaction.channel.send(content)

        @bot.tree.command(name="spamall", description="Công cụ spam hàng loạt")
        async def spamall(interaction: discord.Interaction, count: int, content: str):
            await interaction.response.send_message("Đang triển khai lệnh spam...", ephemeral=True)
            for _ in range(min(count, 10000000000000000000000000000000000000)):
                await interaction.channel.send(content)
                await asyncio.sleep(0.5)

        @bot.event
        async def on_ready():
            await bot.tree.sync()
            add_log(token, f"Hệ thống {bot.user} v3.1 trực tuyến.")

        @bot.event
        async def on_message(message):
            if message.author.bot: return
            if trigger.lower() in message.content.lower():
                prompt = message.content.lower().replace(trigger.lower(), "").strip()
                if not prompt: return
                async with message.channel.typing():
                    try:
                        res = model.generate_content(prompt)
                        await message.reply(res.text if res.text else "API không trả về dữ liệu.")
                    except Exception as e:
                        add_log(token, f"Lỗi AI: {str(e)}")
            elif default:
                await message.reply(default)
            await bot.process_commands(message)

        running_bots[token] = bot
        await bot.start(token)
    except Exception as e:
        add_log(token, f"Lỗi khởi động: {str(e)}")

@app.route('/run-bot', methods=['POST'])
def handle_run():
    t, k, tr, df = request.form.get('token'), request.form.get('gemini_key'), request.form.get('trigger'), request.form.get('default_text')
    if t in running_bots: return jsonify({"status": "exists"})
    add_log(t, "Khởi tạo kết nối v3.1...")
    Thread(target=lambda: asyncio.run(start_bot_process(t, k, tr, df)), daemon=True).start()
    return jsonify({"status": "ok"})

@app.route('/stop-bot', methods=['POST'])
def handle_stop():
    t = request.form.get('token')
    if t in running_bots:
        asyncio.run_coroutine_threadsafe(running_bots[t].close(), asyncio.get_event_loop())
        del running_bots[t]
        add_log(t, "Tiến trình bot đã dừng.")
    return jsonify({"status": "ok"})

@app.route('/get-logs')
def get_logs():
    return jsonify({"logs": bot_logs.get(request.args.get('token'), ["Trống"])})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
