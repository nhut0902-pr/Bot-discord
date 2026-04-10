import discord
from discord.ext import commands
import asyncio
import random
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

insults = [
    "Đụ má mày @{} ngu vl",
    "Cặc lồn mẹ mày {} con chó",
    "Tao spam 30000 lần cho mày chết mẹ {}",
    "@everyone lồn mẹ server này"
]

@bot.event
async def on_ready():
    print(f"Bot raid sẵn sàng - Logged as {bot.user}")
    print("Gõ !sync để sync slash command nếu chưa hiện")

@bot.command()
async def sync(ctx):
    if ctx.author.id != 1465342886303240385:  # Thay bằng ID Discord của mày nếu muốn
        await ctx.send("Mày không phải owner, cút!")
        return
    try:
        await bot.tree.sync()
        await ctx.send("Đã sync slash command global! Gõ /spam hoặc /spam30000 thử đi thằng ngu.")
        print("Sync command thành công!")
    except Exception as e:
        await ctx.send(f"Lỗi sync: {e}")

@bot.tree.command(name="spam", description="Spam chửi nhanh")
async def spam_slash(interaction, amount: int = 100):
    await interaction.response.send_message("Đang spam...", ephemeral=True)
    for i in range(amount):
        try:
            msg = random.choice(insults).format("@everyone")
            await interaction.channel.send(msg)
            await asyncio.sleep(0.35)
        except:
            await asyncio.sleep(5)
    await interaction.followup.send("Spam xong!", ephemeral=True)

@bot.tree.command(name="spam30000", description="Spam cực mạnh 30000 lần")
async def spam30000_slash(interaction):
    await interaction.response.send_message("Bắt đầu spam 30000 lần...", ephemeral=True)
    for _ in range(100):
        for i in range(300):
            try:
                msg = random.choice(insults).format("@everyone")
                await interaction.channel.send(msg)
                await asyncio.sleep(0.3)
            except:
                await asyncio.sleep(5)
        await asyncio.sleep(3)
    await interaction.followup.send("Spam 30000 lần xong! Server sập mẹ nó!", ephemeral=True)

@bot.command()
async def spam(ctx, amount: int = 100):
    await ctx.send("Đang spam...")
    for i in range(amount):
        try:
            msg = random.choice(insults).format("@everyone")
            await ctx.send(msg)
            await asyncio.sleep(0.35)
        except:
            await asyncio.sleep(5)
    await ctx.send("Spam xong!")

@bot.command()
async def spam30000(ctx):
    await ctx.send("Bắt đầu spam 30000 lần...")
    for _ in range(100):
        for i in range(300):
            try:
                msg = random.choice(insults).format("@everyone")
                await ctx.send(msg)
                await asyncio.sleep(0.3)
            except:
                await asyncio.sleep(5)
        await asyncio.sleep(3)
    await ctx.send("Spam 30000 lần xong! Server chết mẹ nó!")

bot.run(os.getenv("TOKEN", "PASTE_TOKEN_VAO_DAY_NEU_CHAY_LOCAL"))