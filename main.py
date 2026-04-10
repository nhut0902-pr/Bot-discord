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
    return "Bot spam 30000 + Hack sex đang chạy mẹ nó - Hacker Minh Nhựt"

# ============== DISCORD BOT ==============
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

insults = [
    "Đụ má mày @{} ngu vl", "Cặc lồn mẹ mày {} con chó",
    "Tao đụ mẹ mày {} óc chó", "@everyone lồn mẹ server này"
]

sex_chat = [
    "Muốn tao gửi ảnh lồn không @{}?", "Cặc tao cứng vl, ai muốn bú @everyone",
    "Lồn mày ướt chưa {}? Tao gửi video bú cặc đây", "Đụ nhau đi, tag @here ai dám chơi",
    "Spam ảnh sex 30000 lần cho server nóng bỏng"
]

porn_images = [
    "https://i.imgur.com/NSp1v7K.jpeg",  # ảnh sex mặc định
    "https://i.imgur.com/8v4v4v4.jpeg",   # mày thay link thật vào đây nếu có
]

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Spam cặc lồn + Hack server"))
    print(f"Bot RAID ONLINE MÀU XANH - Logged as {bot.user}")
    print("Gõ !commands để xem tất cả lệnh")

# Sync command
@bot.command()
async def sync(ctx):
    if ctx.author.id != 1465342886303240385:
        return await ctx.send("Mày không phải owner, cút mẹ đi thằng ngu!")
    await bot.tree.sync()
    await ctx.send("Đã sync tất cả slash command!")

# Spam 30000 lần cũ
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

# Chat sex
@bot.tree.command(name="sex", description="Spam chat sex")
async def sex_chat_cmd(interaction, amount: int = 50):
    await interaction.response.send_message("Đang spam sex...", ephemeral=True)
    for _ in range(amount):
        try:
            msg = random.choice(sex_chat).format("@everyone")
            await interaction.channel.send(msg)
            await asyncio.sleep(0.4)
        except:
            await asyncio.sleep(5)
    await interaction.followup.send("Spam sex xong!", ephemeral=True)

# Gửi ảnh sex
@bot.tree.command(name="porn", description="Gửi ảnh sex")
async def send_porn(interaction, amount: int = 10):
    await interaction.response.send_message(f"Gửi {amount} ảnh sex...", ephemeral=True)
    for _ in range(amount):
        try:
            await interaction.channel.send(random.choice(porn_images))
            await asyncio.sleep(1.5)
        except:
            await asyncio.sleep(5)
    await interaction.followup.send("Gửi ảnh sex xong!", ephemeral=True)

# Kick
@bot.tree.command(name="kick", description="Kick thành viên")
async def kick_member(interaction, member: discord.Member, reason: str = "Đụ má mày bị kick"):
    if not interaction.user.guild_permissions.kick_members:
        return await interaction.response.send_message("Mày không có quyền!", ephemeral=True)
    await member.kick(reason=reason)
    await interaction.response.send_message(f"Đã kick {member.mention}")

# Ban
@bot.tree.command(name="ban", description="Ban thành viên")
async def ban_member(interaction, member: discord.Member, reason: str = "Cặc lồn mẹ mày bị ban"):
    if not interaction.user.guild_permissions.ban_members:
        return await interaction.response.send_message("Không có quyền!", ephemeral=True)
    await member.ban(reason=reason)
    await interaction.response.send_message(f"Đã ban {member.mention}")

# Mass mention chửi
@bot.tree.command(name="mass", description="Mass mention + chửi")
async def mass_mention(interaction, amount: int = 20):
    await interaction.response.send_message("Mass mention đang chạy...", ephemeral=True)
    members = [m.mention for m in interaction.guild.members if not m.bot][:30]
    for _ in range(amount):
        try:
            tag = " ".join(random.sample(members, min(8, len(members))))
            await interaction.channel.send(f"{tag} Đụ lồn mẹ chúng mày! @everyone")
            await asyncio.sleep(0.6)
        except:
            await asyncio.sleep(5)

# Clear tin nhắn
@bot.tree.command(name="clear", description="Xóa tin nhắn")
async def clear_cmd(interaction, amount: int = 100):
    await interaction.response.send_message("Đang xóa...", ephemeral=True)
    await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f"Đã xóa {amount} tin nhắn!", ephemeral=True)

# Nuke server
@bot.tree.command(name="nuke", description="Nuke server (xóa + tạo channel spam)")
async def nuke_server(interaction):
    if not interaction.user.guild_permissions.administrator:
        return await interaction.response.send_message("Cần quyền Admin!", ephemeral=True)
    await interaction.response.send_message("Bắt đầu NUKE SERVER...", ephemeral=True)
    for channel in list(interaction.guild.channels):
        try:
            await channel.delete()
            await asyncio.sleep(0.5)
        except:
            pass
    for i in range(30):
        try:
            await interaction.guild.create_text_channel(f"spam-cặc-lồn-{i}")
            await asyncio.sleep(0.8)
        except:
            pass
    await interaction.followup.send("NUKE HOÀN TẤT! Server thành đống lồn!", ephemeral=True)

# Danh sách lệnh
@bot.command()
async def commands(ctx):
    await ctx.send("**Danh sách lệnh mạnh:**\n"
                   "!spam30000 → Spam 30000 lần\n"
                   "/sex → Spam chat sex\n"
                   "/porn → Gửi ảnh sex\n"
                   "/kick @user → Kick\n"
                   "/ban @user → Ban\n"
                   "/mass → Mass mention chửi\n"
                   "/clear 100 → Xóa tin\n"
                   "/nuke → Nuke server\n"
                   "!sync → Sync slash\n"
                   "Invite bot với quyền Administrator để dùng hết!")

# Chạy Flask + Bot song song
def run_flask():
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    bot.run(os.getenv("TOKEN"))