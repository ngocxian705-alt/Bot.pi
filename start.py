import os
import discord
from discord.ext import commands
import requests

# ========= CONFIG =========
TOKEN = os.getenv("DISCORD_TOKEN")  # Lấy token từ ENV
API_URL = "https://sikibidiapiemote.onrender.com/join"

# ========= FULL EMOTE =========
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
    "cuoi2": "909000002",
    "chongday": "909000012",
    "chicken": "909000006",
    "ngaivang": "909000014",
    "aicap": "909000011",
    "tanghoa": "909000010",
    "buocdicuaquy": "909000020",
    "dakungfu": "909000028",
    "thatim": "909000045",
    "AK": "909000063",
    "nhayvoicho": "909000052",
    "saitama1": "909000064",
    "siu": "909000066",
    "mangxa4nguoi": "909000071",
    "xemangxa": "909000074",
    "cudam": "909000067",
    "namdam": "909037011",
    "chayraimoney": "909035001",
    "Ctsinhton": "909034011",
    "tamnang": "909036006",
    "xevang4banh": "909040001",
    "baytrenkiem": "909041004",
    "xichdu": "909040013",
    "sikibidi": "909042017",
    "xemoto": "909043009",
    "xe_lambo": "909042012",
    "traitim2nguoi": "909043010",
    "cauhon": "909043013",
    "zombie": "909044012",
    "parafal": "909045001",
    "maico": "909045009",
    "ngoithien": "909045015",
    "cuoingua": "909045003",
    "phao": "909045005",
    "bapbenh": "909045012",
    "6nong": "909046010",
    "camco2": "909046013",
    "sutbong": "909046015",
    "nhaybong": "909046016",
    "lacdich": "909046017",
    "ngoighe": "909047001",
    "ghetinhyeu": "909047003",
    "canh1": "909047004",
    "ngaivang2": "909047005",
    "khoecup": "909047006",
    "rasengan": "909047015",
    "bithuatlangla": "909047016",
    "ketannaruto": "909047017",
    "chayninja": "909047018",
    "ketannaruto2": "909047019",
    "guitar": "909048003",
    "piano": "909048004",
    "nhaydanhtrong": "909048005",
    "chacchac": "909048006",
    "ngu": "909048007",
    "lacda": "909048009",
    "camco3": "909048011",
    "nhaydengiau": "909048012",
    "nailoong": "909049001",
    "songaychoi": "909049006",
    "p90": "909049010",
    "oi": "909049013",
    "uethochuyensinh": "909050002",
    "hoadon": "909050005",
    "minato": "909050006",
    "The_Rings": "909050009",
    "sungcuoi": "909050020"
}

# ========= BOT =========
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# ========= MODAL =========
class InfoModal(discord.ui.Modal, title="Nhập thông tin Free Fire"):
    tc = discord.ui.TextInput(label="Team Code", placeholder="VD: ABC123", required=True)
    uid = discord.ui.TextInput(label="UID", placeholder="VD: 1234567890", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            content="🎯 Chọn emote bên dưới",
            view=EmoteView(self.tc.value, self.uid.value)
        )

# ========= SELECT =========
class EmoteSelect(discord.ui.Select):
    def __init__(self, tc, uid):
        self.tc = tc
        self.uid = uid
        options = [discord.SelectOption(label=name, value=name) for name in list(EMOTES.keys())[:25]]
        super().__init__(placeholder="🎭 Chọn emote", options=options)

    async def callback(self, interaction: discord.Interaction):
        user = interaction.user
        name = self.values[0]
        emote_id = EMOTES[name]

        params = {"tc": self.tc, "uid1": self.uid, "emote_id": emote_id}
        try:
            r = requests.get(API_URL, params=params, timeout=15)
            status = "✅ Thành công" if r.status_code == 200 else "❌ Thất bại"
        except Exception as e:
            status = f"⚠️ Lỗi: {e}"

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

# ========= BUTTON =========
class StartView(discord.ui.View):
    @discord.ui.button(label="🚀 GỬI EMOTE", style=discord.ButtonStyle.success)
    async def start(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Chặn DM
        if interaction.guild is None:
            await interaction.response.send_message(
                "❌ Bạn không thể dùng bot qua tin nhắn riêng! Vui lòng dùng trong server.",
                ephemeral=True
            )
            return
        await interaction.response.send_modal(InfoModal())

# ========= SLASH COMMAND =========
@bot.tree.command(name="emote", description="Gửi emote Free Fire bằng nút bấm")
async def emote(interaction: discord.Interaction):
    # Chặn DM
    if interaction.guild is None:
        await interaction.response.send_message(
            "❌ Bạn không thể dùng bot qua tin nhắn riêng! Vui lòng dùng trong server.",
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

# ========= READY =========
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Bot online: {bot.user}")

bot.run(TOKEN)