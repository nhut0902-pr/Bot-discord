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
    return "Bot spam 30000 đang chạy mẹ nó - Hacker Minh Nhựt"

# ============== DISCORD BOT ==============
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

insults = [
    "Đụ má mày @{} ngu vl",
    "Cặc lồn mẹ mày {} con chó",
    "Tao spam 30000 lần cho mày chết mẹ {}",
    "@everyone lồn mẹ server này"
]

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Spam cặc lồn 30000 lần"))
    print(f"Bot RAID ONLINE MÀU XANH - Logged as {bot.user}")
    print("Gõ !sync nếu slash chưa hiện")

@bot.command()
async def sync(ctx):
    if ctx.author.id != 1465342886303240385:
        return await ctx.send("Mày không phải owner, cút mẹ đi!")
    await bot.tree.sync()
    await ctx.send("Sync xong! Gõ /spam30000 đi thằng ngu.")

@bot.tree.command(name="spam30000", description="Spam 30000 lần")
async def spam30000_slash(interaction):
    await interaction.response.send_message("Bắt đầu spam...", ephemeral=True)
    for _ in range(100):
        for _ in range(300):
            try:
                msg = random.choice(insults).format("@everyone")
                await interaction.channel.send(msg)
                await asyncio.sleep(0.35)
            except:
                await asyncio.sleep(6)
        await asyncio.sleep(4)
    await interaction.followup.send("30000 lần xong! Server sập mẹ nó!", ephemeral=True)

@bot.command()
async def spam30000(ctx):
    await ctx.send("Bắt đầu spam 30000 lần cặc lồn...")
    for _ in range(100):
        for _ in range(300):
            try:
                msg = random.choice(insults).format("@everyone")
                await ctx.send(msg)
                await asyncio.sleep(0.35)
            except:
                await asyncio.sleep(6)
        await asyncio.sleep(4)
    await ctx.send("Spam xong! Server chết mẹ nó!")

# Chạy Flask và Bot song song
def run_flask():
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    bot.run(os.getenv("TOKEN"))