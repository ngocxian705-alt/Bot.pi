import discord
from discord.ext import commands
import requests
import json
import os

# ===== CONFIG =====
TOKEN = os.getenv("DISCORD_TOKEN")   # Render ENV
PREFIX = "!"
API_URL = "https://sikibidiapilike8.onrender.com/like"  # mặc định VN

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN not set")

# ===== INTENTS =====
intents = discord.Intents.default()
intents.message_content = True
intents.dm_messages = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

# ===== READY =====
@bot.event
async def on_ready():
    print(f"✅ Bot online: {bot.user}")

# ===== BLOCK DM =====
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if isinstance(message.channel, discord.DMChannel):
        return  # cấm DM

    await bot.process_commands(message)

# ===== LIKE COMMAND =====
@bot.command()
@commands.guild_only()
async def like(ctx, uid: str):
    await ctx.reply("⏳ Đang gọi API...")

    try:
        r = requests.get(
            API_URL,
            params={
                "uid": uid,
                "server_name": "VN"  # 🔥 mặc định VN
            },
            timeout=20
        )

        try:
            data = r.json()
            raw = json.dumps(data, indent=2, ensure_ascii=False)
        except:
            raw = r.text

        if len(raw) > 1900:
            raw = raw[:1900] + "\n... (truncated)"

        await ctx.reply(
            "📦 **JSON GỐC API**\n"
            f"```json\n{raw}\n```"
        )

    except Exception:
        await ctx.reply("❌ Lỗi gọi API")

# ===== RUN =====
bot.run(TOKEN)