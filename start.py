import os
import threading
import requests
import discord
from discord.ext import commands
from flask import Flask

# ================== FLASK (MỞ PORT CHO RENDER) ==================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot alive"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web).start()

# ================== CONFIG ==================
TOKEN = os.getenv("DISCORD_TOKEN")
API_URL = "https://sikibidiapiemote.onrender.com/join"

# ================== EMOTES ==================
EMOTES = {
    "m60": "909051003",
    "soka": "909000068",
    "mangxa": "909000075",
    "longtoc": "909000081",
    "phomat": "909000090",
    "m4a1": "909033001",
    "camco": "909000034",
    "xm8": "909000085",
    "ump": "909000098",
    "mp5": "909033002",
    "m1887": "909035007",
    "m1014lv8": "909039011",
    "thomson": "909038010",
    "g18": "909038012",
    "an94": "909035012",
    "goda": "909041005",
    "mp40tiachop": "909040010",
    "lv100": "909042007",
    "chimgokien": "909042008",
    "noel": "909051002",
    "cungten": "909051012",
    "xe": "909051010",
    "canhhong": "909051001",
    "cuoi": "909051015",
    "voisen": "909051004",
    "choigame": "909051017",
    "sikibidi": "909042017",
    "rasengan": "909047015",
    "sungcuoi": "909050020"
}

# ================== DISCORD BOT ==================
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ================== MODAL ==================
class InfoModal(discord.ui.Modal, title="Nhập thông tin Free Fire"):
    tc = discord.ui.TextInput(label="Team Code", placeholder="VD: ABC123", required=True)
    uid = discord.ui.TextInput(label="UID", placeholder="VD: 1234567890", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "🎯 Chọn emote bên dưới",
            view=EmoteView(self.tc.value, self.uid.value)
        )

# ================== SELECT ==================
class EmoteSelect(discord.ui.Select):
    def __init__(self, tc, uid):
        self.tc = tc
        self.uid = uid
        options = [
            discord.SelectOption(label=name, value=name)
            for name in list(EMOTES.keys())[:25]
        ]
        super().__init__(placeholder="🎭 Chọn emote", options=options)

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        name = self.values[0]
        emote_id = EMOTES[name]

        params = {
            "tc": self.tc,
            "uid1": self.uid,
            "emote_id": emote_id
        }

        try:
            r = requests.get(API_URL, params=params, timeout=15)
            status = "✅ Thành công" if r.status_code == 200 else "❌ Thất bại"
        except Exception as e:
            status = f"⚠️ Lỗi API"

        embed = discord.Embed(title="🎭 FREE FIRE EMOTE", color=0x00ff66)
        embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
        embed.add_field(name="👤 UID", value=self.uid, inline=False)
        embed.add_field(name="🔑 Team Code", value=self.tc, inline=False)
        embed.add_field(name="🎬 Emote", value=name, inline=True)
        embed.add_field(name="📡 Status", value=status, inline=True)
        embed.set_footer(text="Powered by Sikibidi API")
        embed.timestamp = discord.utils.utcnow()

        await interaction.response.send_message(embed=embed)

class EmoteView(discord.ui.View):
    def __init__(self, tc, uid):
        super().__init__(timeout=120)
        self.add_item(EmoteSelect(tc, uid))

# ================== BUTTON ==================
class StartView(discord.ui.View):
    @discord.ui.button(label="🚀 GỬI EMOTE", style=discord.ButtonStyle.success)
    async def start(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.guild is None:
            await interaction.response.send_message(
                "❌ Không dùng bot trong tin nhắn riêng!",
                ephemeral=True
            )
            return
        await interaction.response.send_modal(InfoModal())

# ================== SLASH COMMAND ==================
@bot.tree.command(name="emote", description="Gửi emote Free Fire bằng nút bấm")
async def emote(interaction: discord.Interaction):
    if interaction.guild is None:
        await interaction.response.send_message(
            "❌ Không dùng bot trong tin nhắn riêng!",
            ephemeral=True
        )
        return

    user = interaction.user
    embed = discord.Embed(
        title="🔥 FREE FIRE EMOTE",
        description="Bấm nút bên dưới để gửi emote",
        color=0x00ff66
    )
    embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)

    await interaction.response.send_message(embed=embed, view=StartView())

# ================== READY ==================
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Bot online: {bot.user}")

bot.run(TOKEN)