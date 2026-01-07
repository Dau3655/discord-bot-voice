import discord
import os
import asyncio
import datetime
import random
from discord.ext import commands, tasks
from keep_alive import keep_alive

# === 設定區 ===
TOKEN = os.getenv("DISCORD_TOKEN")
VOICE_CHANNEL_ID = 911302671863021648  # 你的語音頻道 ID

# === 機器人初始化 ===
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 記錄啟動時間 (用來計算 uptime)
start_time = datetime.datetime.now()

# === 功能 1: 綜合狀態顯示 (實況燈 + 運作時間 + 趣味文字) ===
# 每 5 分鐘更新一次狀態
@tasks.loop(minutes=5)
async def status_task():
    # 1. 計算運作時間
    now = datetime.datetime.now()
    uptime = now - start_time
    days = uptime.days
    hours, remainder = divmod(uptime.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_str = f"{days}天 {hours}小時 {minutes}分"

    # 2. 設定狀態清單 (包含技術資訊 & 趣味文字)
    statuses = [
        f"已持續運作: {uptime_str}",        # 顯示時間
        f"守護紫花海: {len(bot.voice_clients)} 個頻道", # 顯示連線數
        "系統狀態: 🟢 良好",
        "掛機積分計算中...",
        "練習 24 小時不眨眼",
        "監控大家的睡眠時間",
        "數羊... 1隻... 2隻..."
    ]
    
    # 3. 隨機選一個並顯示 (使用 Streaming 模式顯示紫燈)
    current_status = random.choice(statuses)
    
    await bot.change_presence(
        activity=discord.Streaming(
            name=current_status, 
            url="https://www.twitch.tv/discord" # 這是騙 Discord 顯示紫燈用的連結
        )
    )

# === 功能 2: 斷線重連巡邏隊 (核心掛機功能) ===
# 每 3 分鐘檢查一次，確保機器人永遠在語音頻道內
@tasks.loop(minutes=3) 
async def check_voice_connection():
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
            
    # 情況 C: 一切正常
    else:
        pass

# === 啟動區 ===
@bot.event
async def on_ready():
    print(f'{bot.user} 上線了！')
    
    # 1. 啟動斷線重連巡邏隊
    if not check_voice_connection.is_running():
        check_voice_connection.start()
        print("✅ 斷線重連巡邏隊已啟動！")

    # 2. 啟動狀態變換 (實況燈)
    if not status_task.is_running():
        status_task.start()
        print("✅ 變色龍實況狀態已啟動！")

# 保持網頁喚醒
keep_alive()

if TOKEN:
    bot.run(TOKEN)
else:
    print("錯誤：找不到 Token")