import discord
import os
import asyncio
from discord.ext import commands, tasks # 1. 多匯入 tasks
from keep_alive import keep_alive
import random

TOKEN = os.getenv("DISCORD_TOKEN")
# 你的語音頻道 ID
VOICE_CHANNEL_ID = 911302671863021648

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# === 新增功能：變色龍狀態 (每 10 分鐘換一次狀態) ===
@tasks.loop(minutes=10)
async def status_task():
    # 這裡可以自訂你想讓機器人顯示的狀態
    statuses = [
        f"幫 {len(bot.voice_clients)} 個伺服器顧家",
        "計算掛機時間中...",
        "練習 24 小時不眨眼",
        "在紫花海發呆",
        "監控大家的睡眠時間",
        "數羊... 1隻... 2隻..."
    ]
    # 隨機選一個
    status = random.choice(statuses)
    # 設定狀態 (Game=正在玩, Watching=正在看, Listening=正在聽)
    await bot.change_presence(activity=discord.Game(name=status))


# === 新增功能：斷線重連巡邏隊 ===
# 每 3 分鐘執行一次檢查，確保機器人永遠在語音頻道內
@tasks.loop(minutes=3) 
async def check_voice_connection():
    # 確保機器人核心已經準備好，才開始檢查
    if not bot.is_ready():
        return

    channel = bot.get_channel(VOICE_CHANNEL_ID)
    if not channel:
        print("巡邏隊報告：找不到目標頻道，無法執行重連。")
        return

    # 檢查機器人目前是否連接在該伺服器的語音頻道
    voice_client = discord.utils.get(bot.voice_clients, guild=channel.guild)
    
    # 情況 A: 機器人根本不在任何語音頻道 -> 立刻加入
    if not voice_client:
        print("巡邏隊發現：機器人不在頻道內，正在嘗試重新加入...")
        try:
            await channel.connect()
            print("重連成功！掛機繼續！")
        except Exception as e:
            print(f"重連失敗: {e}")
    
    # 情況 B: 機器人連著，但連錯房間了 -> 強制移動過去
    elif voice_client.channel.id != VOICE_CHANNEL_ID:
        print("巡邏隊發現：機器人跑錯房間了，正在移動中...")
        try:
            await voice_client.move_to(channel)
        except Exception as e:
            print(f"移動失敗: {e}")
            
    # 情況 C: 一切正常 -> 默默守護，不做任何事
    else:
        pass

@bot.event
async def on_ready():
    print(f'{bot.user} 上線了！')
    
    # 啟動巡邏隊 (確保只啟動一次)
    if not check_voice_connection.is_running():
        check_voice_connection.start()
        print("斷線重連巡邏隊已啟動！24小時監控中...")

# 保持網頁喚醒
keep_alive()

if TOKEN:
    bot.run(TOKEN)
else:
    print("錯誤：找不到 Token")

@bot.event
async def on_ready():
    print(f'{bot.user} 上線了！')

    # 啟動斷線重連巡邏隊
    if not check_voice_connection.is_running():
        check_voice_connection.start()
        print("斷線重連巡邏隊已啟動！")
        
    # 啟動變色龍狀態 (新增這段)
    if not status_task.is_running():
        status_task.start()
        print("變色龍狀態已啟動！")