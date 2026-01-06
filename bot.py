import discord
import os
from discord.ext import commands
from keep_alive import keep_alive 

TOKEN = os.getenv("DISCORD_TOKEN") 

# 語音頻道ID
VOICE_CHANNEL_ID = 911302671863021648 

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} 上線了！')
    
    # 防呆 1: 先檢查頻道存不存在
    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if not channel:
        print(f"錯誤：找不到 ID 為 {VOICE_CHANNEL_ID} 的語音頻道，請檢查 ID 是否正確。")
        return  # 找不到就停下來，不要硬執行

    # 防呆 2: 檢查機器人是否已經在語音頻道裡了 (避免重複加入導致崩潰)
    if bot.voice_clients:
        print("檢測到機器人已經在語音頻道中，跳過加入步驟。")
        return

    # 防呆 3: 嘗試加入，如果失敗(例如沒權限、滿員)則捕捉錯誤，不要讓程式掛掉
    try:
        await channel.connect()
        print(f"成功加入語音頻道：{channel.name}")
    except discord.ClientException:
        print("錯誤：機器人似乎已經連線了 (ClientException)")
    except discord.errors.Forbidden:
        print("錯誤：機器人沒有權限加入這個頻道 (請檢查 Discord 頻道權限設定)")
    except Exception as e:
        print(f"發生未知的錯誤，無法加入頻道：{e}")


keep_alive()

if TOKEN:
    bot.run(TOKEN)
else:
    print("錯誤：找不到 Token，請確認環境變數設定正確！")