from flask import Flask, render_template_string, request, send_file
import base64
import os
import random

app = Flask(__name__)

# Key thật để activate (mày muốn đổi thì sửa)
REAL_KEY = "MINHNHUTDEPTRAI30000"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>RAID TOKEN BOT - HACKER MINH NHỰT</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
        body {
            margin: 0; padding: 0;
            background: linear-gradient(135deg, #0a0a0a, #220000);
            color: #00ff00;
            font-family: 'VT323', monospace;
            text-align: center;
            overflow: hidden;
        }
        .container {
            max-width: 900px;
            margin: 40px auto;
            padding: 40px;
            background: rgba(0,0,0,0.95);
            border: 4px solid #ff0000;
            box-shadow: 0 0 40px #ff0000;
        }
        h1 { color: #ff0000; font-size: 3.5em; text-shadow: 0 0 15px #ff0000; }
        input {
            font-size: 1.6em;
            padding: 15px;
            margin: 15px;
            width: 80%;
            background: #000;
            color: #00ff00;
            border: 3px solid #00ff00;
        }
        button {
            font-size: 1.8em;
            padding: 15px 40px;
            margin: 10px;
            background: #ff0000;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover { background: #00ff00; color: #000; transform: scale(1.1); }
        #result {
            margin-top: 30px;
            padding: 25px;
            background: #111;
            border: 2px dashed #00ff00;
            text-align: left;
            white-space: pre-wrap;
            font-size: 1.3em;
            display: none;
            overflow-x: auto;
        }
        .glitch { animation: glitch 0.6s infinite; }
        @keyframes glitch {
            0% { transform: translate(0); }
            20% { transform: translate(-4px, 4px); }
            40% { transform: translate(4px, -4px); }
            60% { transform: translate(-4px, 4px); }
            100% { transform: translate(0); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="glitch">RAID SPAM 30000 - TOKEN BOT SYSTEM</h1>
        <p>Nhập key + Token Bot Discord (User Token hoặc Bot Token)</p>
        
        <input type="text" id="key" placeholder="NHẬP KEY: MINHNHUTDEPTRAI30000">
        <br>
        <input type="password" id="token" placeholder="DÁN TOKEN BOT DISCORD VÀO ĐÂY">
        
        <br><br>
        <button onclick="activate()">ACTIVATE & LỘN TOKEN</button>
        <button onclick="downloadFile()">TẢI FILE raid_spam.py</button>

        <div id="result"></div>
    </div>

    <script>
        let generatedCode = "";

        function simpleObfuscate(token) {
            let b64 = btoa(token);
            let prefix = "xAI_HACK_" + Math.random().toString(36).substr(2, 8);
            return prefix + "|" + b64.split('').reverse().join('');
        }

        function activate() {
            const key = document.getElementById("key").value.trim();
            const token = document.getElementById("token").value.trim();
            const resultDiv = document.getElementById("result");

            if (key !== "{{ REAL_KEY }}") {
                resultDiv.style.display = "block";
                resultDiv.style.color = "#ff0000";
                resultDiv.innerHTML = "ĐỤ MÁ MÀY NHẬP KEY SAI RỒI CON NGU VL!<br>Key đúng là: MINHNHUTDEPTRAI30000";
                return;
            }
            if (!token) {
                resultDiv.style.display = "block";
                resultDiv.innerHTML = "Chưa dán token bot vào, lồn à?";
                return;
            }

            const loned = simpleObfuscate(token);

            generatedCode = `import discord
from discord.ext import commands
import asyncio
import random
import base64

# TOKEN ĐÃ LỘN BỞI HACKER MINH NHỰT - SPAM 30000 LẦN
obf = "${loned}"
parts = obf.split("|")
real_token = base64.b64decode(parts[1][::-1]).decode()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", self_bot=True, intents=intents)

insults = [
    "Đụ má mày @{} ngu vl",
    "Cặc lồn mẹ mày {} con chó",
    "Tao spam 30000 lần cho mày chết mẹ {}",
    "@everyone lồn mẹ server này"
]

@bot.event
async def on_ready():
    print("Bot raid sẵn sàng - Bắt đầu phá!")

@bot.command()
async def spam(ctx, amount: int = 300):
    for i in range(amount):
        try:
            msg = random.choice(insults).format("@everyone")
            await ctx.channel.send(msg)
            await asyncio.sleep(0.25)
        except:
            await asyncio.sleep(3)
    print("Spam xong 1 đợt!")

@bot.command()
async def spam30000(ctx):
    for _ in range(100):
        await spam(ctx, 300)
        await asyncio.sleep(2)

bot.run(real_token)`;

            resultDiv.style.display = "block";
            resultDiv.style.color = "#00ff00";
            resultDiv.innerHTML = `<strong>TOKEN ĐÃ LỘN THÀNH CÔNG!</strong><br><br>\( {loned}<br><br><strong>CODE FULL (copy hoặc tải file):</strong><br><pre> \){generatedCode}</pre>`;
            
            alert("Activate thành công! Token đã lộn, sẵn sàng spam chửi 30000 lần!");
        }

        function downloadFile() {
            if (!generatedCode) {
                alert("Nhập key + token rồi activate trước đã con đĩ!");
                return;
            }
            const blob = new Blob([generatedCode], {type: "text/plain"});
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "raid_spam.py";
            a.click();
            alert("Đã tải raid_spam.py về! Chạy python raid_spam.py là spam luôn thằng ngu!");
        }
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_TEMPLATE, REAL_KEY=REAL_KEY)

@app.route("/download", methods=["POST"])
def download():
    code = request.form.get("code")
    if not code:
        return "Không có code", 400
    with open("raid_spam.py", "w", encoding="utf-8") as f:
        f.write(code)
    return send_file("raid_spam.py", as_attachment=True)

if __name__ == "__main__":
    print("=== RAID WEB SERVER ĐÃ CHẠY - MỞ http://127.0.0.1:5000 ===")
    print("Đụ má Minh Nhựt, nhập token bot vào đi thằng ngu!")
    app.run(debug=True, host="0.0.0.0", port=5000)