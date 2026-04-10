from flask import Flask, render_template_string, request, send_file
import random

app = Flask(__name__)

REAL_KEY = "MINHNHUTDEPTRAI30000"

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
        <h1>RAID SPAM 30000 - BOT TOKEN</h1>
        <p>Nhập key + Bot Token Discord (không phải user token)</p>
        
        <input type="text" id="key" placeholder="KEY: MINHNHUTDEPTRAI30000">
        <br>
        <input type="password" id="token" placeholder="DÁN BOT TOKEN VÀO ĐÂY">
        
        <br><br>
        <button onclick="activate()">ACTIVATE</button>
        <button onclick="downloadFile()">TẢI FILE raid_spam.py</button>

        <div id="result"></div>
    </div>

    <script>
        let generatedCode = "";

        function activate() {
            const key = document.getElementById("key").value.trim();
            const token = document.getElementById("token").value.trim();
            const resultDiv = document.getElementById("result");

            if (key !== "{{ REAL_KEY }}") {
                resultDiv.style.display = "block";
                resultDiv.style.color = "#ff0000";
                resultDiv.innerHTML = "KEY SAI RỒI CON NGU!<br>Key đúng là: MINHNHUTDEPTRAI30000";
                return;
            }
            if (!token) {
                resultDiv.style.display = "block";
                resultDiv.innerHTML = "Dán Bot Token vào đi thằng ngu!";
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

@bot.event
async def on_ready():
    print(f"Bot raid sẵn sàng - Logged as {bot.user}")

@bot.command()
async def spam(ctx, amount: int = 100):
    for i in range(amount):
        try:
            msg = random.choice(insults).format("@everyone")
            await ctx.channel.send(msg)
            await asyncio.sleep(0.35)
        except Exception as e:
            print(f"Lỗi: {e}")
            await asyncio.sleep(5)
    print("Spam xong đợt này!")

@bot.command()
async def spam30000(ctx):
    print("Bắt đầu spam 30000 lần - Server sắp sập mẹ nó!")
    for _ in range(100):
        await spam(ctx, 300)
        await asyncio.sleep(3)

bot.run("${token}")`;

            resultDiv.style.display = "block";
            resultDiv.style.color = "#00ff00";
            resultDiv.innerHTML = `<strong>BOT TOKEN ĐÃ NHẬP OK!</strong><br><br><strong>CODE FULL:</strong><br><pre>${generatedCode}</pre>`;
            alert("Activate thành công! Tải file và chạy python raid_spam.py");
        }

        function downloadFile() {
            if (!generatedCode) {
                alert("Nhập key + Bot Token rồi nhấn ACTIVATE trước đã con đĩ!");
                return;
            }
            const blob = new Blob([generatedCode], {type: "text/plain"});
            const a = document.createElement("a");
            a.href = URL.createObjectURL(blob);
            a.download = "raid_spam.py";
            a.click();
            alert("Tải xong raid_spam.py! Chạy python raid_spam.py rồi invite bot vào server và gõ !spam30000");
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, REAL_KEY=REAL_KEY)

if __name__ == "__main__":
    print("=== RAID BOT TOKEN SERVER ĐÃ CHẠY ===")
    print("Mở trình duyệt: http://127.0.0.1:5000")
    print("Dùng Bot Token thật (tạo ở https://discord.com/developers/applications)")
    app.run(debug=True, host="0.0.0.0", port=5000)