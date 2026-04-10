from flask import Flask, render_template_string, send_file
import random

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>RAID BOT TOKEN - HACKER MINH NHỰT</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
        body { 
            margin:0; padding:0; 
            background:linear-gradient(135deg,#0a0a0a,#220000); 
            color:#00ff00; 
            font-family:'VT323',monospace; 
            text-align:center; 
        }
        .container { 
            max-width:900px; 
            margin:40px auto; 
            padding:40px; 
            background:rgba(0,0,0,0.95); 
            border:4px solid #ff0000; 
            box-shadow:0 0 40px #ff0000; 
        }
        h1 { color:#ff0000; font-size:3.5em; text-shadow:0 0 15px #ff0000; }
        input { 
            font-size:1.6em; 
            padding:15px; 
            margin:15px; 
            width:80%; 
            background:#000; 
            color:#00ff00; 
            border:3px solid #00ff00; 
        }
        button { 
            font-size:1.8em; 
            padding:15px 40px; 
            margin:10px; 
            background:#ff0000; 
            color:white; 
            border:none; 
            cursor:pointer; 
        }
        button:hover { 
            background:#00ff00; 
            color:#000; 
            transform:scale(1.1); 
        }
        #result { 
            margin-top:30px; 
            padding:25px; 
            background:#111; 
            border:2px dashed #00ff00; 
            text-align:left; 
            white-space:pre-wrap; 
            font-size:1.3em; 
            display:none; 
            overflow-x:auto; 
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>RAID SPAM 30000</h1>
        <p>Dán Bot Token vào rồi ACTIVATE để tạo file</p>
        
        <input type="password" id="token" placeholder="DÁN BOT TOKEN VÀO ĐÂY">
        
        <br><br>
        <button onclick="activate()">ACTIVATE</button>
        <button onclick="downloadFile()">TẢI FILE raid_spam.py</button>

        <div id="result"></div>
    </div>

    <script>
        let generatedCode = "";

        function activate() {
            const token = document.getElementById("token").value.trim();
            const resultDiv = document.getElementById("result");

            if (!token) {
                resultDiv.style.display = "block";
                resultDiv.style.color = "#ff0000";
                resultDiv.innerHTML = "Đụ má mày dán token vào đi con ngu!";
                return;
            }

            generatedCode = `import discord
from discord.ext import commands
import asyncio
import random

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

insults = [
    "Đụ má mày @{} ngu vl",
    "Cặc lồn mẹ mày {} con chó",
    "Tao spam 30000 lần cho mày chết mẹ {}",
    "@everyone lồn mẹ server này"
]

tree = bot.tree

@bot.event
async def on_ready():
    await tree.sync()
    print(f"Bot sẵn sàng - Logged as {bot.user}")
    print("Slash command đã sync! Gõ /spam hoặc !spam30000")

@tree.command(name="spam", description="Spam chửi nhanh")
async def spam_slash(interaction, amount: int = 100):
    await interaction.response.send_message("Đang spam...", ephemeral=True)
    for i in range(amount):
        try:
            msg = random.choice(insults).format("@everyone")
            await interaction.channel.send(msg)
            await asyncio.sleep(0.35)
        except:
            await asyncio.sleep(5)
    await interaction.followup.send("Spam xong đợt này!", ephemeral=True)

@tree.command(name="spam30000", description="Spam cực mạnh 30000 lần")
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
    await interaction.followup.send("Đã spam xong 30000 lần! Server sập mẹ nó rồi!", ephemeral=True)

@bot.command()
async def spam(ctx, amount: int = 100):
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

bot.run("${token}")`;

            resultDiv.style.display = "block";
            resultDiv.style.color = "#00ff00";
            resultDiv.innerHTML = `<strong>CODE ĐÃ SẴN - CÓ SLASH COMMAND!</strong><br><br><strong>CODE FULL:</strong><br><pre>${generatedCode}</pre>`;
            alert("Tạo file thành công! Invite bot vào server rồi gõ /spam hoặc !spam30000");
        }

        function downloadFile() {
            if (!generatedCode) {
                alert("Nhấn ACTIVATE trước đã con đĩ!");
                return;
            }
            const blob = new Blob([generatedCode], {type: "text/plain"});
            const a = document.createElement("a");
            a.href = URL.createObjectURL(blob);
            a.download = "raid_spam.py";
            a.click();
            alert("Tải xong raid_spam.py! Invite bot → gõ /spam30000 hoặc !spam30000");
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    print("=== RAID BOT SERVER CHẠY ===")
    print("Mở: http://127.0.0.1:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)