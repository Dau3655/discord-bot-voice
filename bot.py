import discord
import os  # 新增這個
from discord.ext import commands
from keep_alive import keep_alive # 匯入剛剛寫的假網站功能

# === 安全性修改 ===
# 這裡改成讀取環境變數，不要直接貼密碼！
# 如果你在自己電腦跑，它會讀不到，沒關係，我們等等在雲端設定
TOKEN = os.getenv("DISCORD_TOKEN") 

# 你的語音頻道 ID (記得填數字)
VOICE_CHANNEL_ID = 911302671863021648 

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} 上線了！')
    # 啟動後自動加入頻道
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if channel:
        await channel.connect()
        print(f"已加入語音頻道：{channel.name}")
    else:
        print("找不到語音頻道 ID")

# === 啟動假網站伺服器 ===
keep_alive()

# === 啟動機器人 ===
if TOKEN:
    bot.run(TOKEN)
else:
    print("錯誤：找不到 Token，請確認環境變數設定正確！")