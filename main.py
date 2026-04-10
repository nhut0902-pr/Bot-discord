import discord
from discord.ext import commands
import asyncio
import random
import os

intents = discord.Intents.default()
intents.message_content = True   # Bắt buộc cho prefix command
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
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Đang spam 30000 lần cặc lồn"))
    print(f"Bot RAID ONLINE MÀU XANH - Logged as {bot.user}")
    print("Gõ !sync nếu slash command chưa hiện")

@bot.command()
async def sync(ctx):
    if ctx.author.id != 1465342886303240385:  # ID Discord của mày
        return await ctx.send("Mày không phải owner ngu vl!")
    await bot.tree.sync()
    await ctx.send("Đã sync slash command! Giờ gõ /spam30000 thử đi thằng đĩ.")

@bot.tree.command(name="spam", description="Spam chửi")
async def spam_slash(interaction, amount: int = 100):
    await interaction.response.send_message("Đang spam...", ephemeral=True)
    for _ in range(amount):
        try:
            msg = random.choice(insults).format("@everyone")
            await interaction.channel.send(msg)
            await asyncio.sleep(0.4)
        except:
            await asyncio.sleep(6)
    await interaction.followup.send("Spam xong!", ephemeral=True)

@bot.tree.command(name="spam30000", description="Spam cực mạnh 30000 lần")
async def spam30000_slash(interaction):
    await interaction.response.send_message("Bắt đầu spam 30000 lần - Server sắp sập!", ephemeral=True)
    for _ in range(100):
        for _ in range(300):
            try:
                msg = random.choice(insults).format("@everyone")
                await interaction.channel.send(msg)
                await asyncio.sleep(0.35)
            except:
                await asyncio.sleep(6)
        await asyncio.sleep(4)
    await interaction.followup.send("30000 lần xong! Server chết mẹ nó rồi!", ephemeral=True)

@bot.command()
async def spam30000(ctx):
    await ctx.send("Bắt đầu spam 30000 lần...")
    for _ in range(100):
        for _ in range(300):
            try:
                msg = random.choice(insults).format("@everyone")
                await ctx.send(msg)
                await asyncio.sleep(0.35)
            except:
                await asyncio.sleep(6)
        await asyncio.sleep(4)
    await ctx.send("Spam 30000 lần xong! Server nổ tung mẹ nó!")

bot.run(os.getenv("TOKEN"))