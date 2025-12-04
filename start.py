import discord
from discord.ext import commands
import requests
import os
from flask import Flask
from threading import Thread

# ===== KEEP-ALIVE WEB SERVER =====
app = Flask("")

@app.route("/")
def home():
    return "Bot is running!"

def run():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# ===== BOT SETUP =====
BOT_TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== FULL EMOTE LIST =====
EMOTE_LIST = {
    "m60":"909051003","soka":"909000068","mangxa":"909000075","longtoc":"909000081",
    "phomat":"909000090","m4a1":"909033001","camco":"909000034","xm8":"909000085",
    "ump":"909000098","mp5":"909033002","m1887":"909035007","m1014lv8":"909039011",
    "thomson":"909038010","g18":"909038012","an94":"909035012","goda":"909041005",
    "mp40tiachop":"909040010","lv100":"909042007","chimgokien":"909042008","noel":"909051002",
    "cungten":"909051012","xe":"909051010","canhhong":"909051001","cuoi":"909051015",
    "voisen":"909051004","choigame":"909051017","cuoi2":"909000002","chongday":"909000012",
    "chicken":"909000006","ngaivang":"909000014","aicap":"909000011","tanghoa":"909000010",
    "buocdicuaquy":"909000020","dakungfu":"909000028","thatim":"909000045","ak":"909000063",
    "nhayvoicho":"909000052","saitama1":"909000064","siu":"909000066","mangxa4nguoi":"909000071",
    "xemangxa":"909000074","cudam":"909000067","namdam":"909037011","chayraimoney":"909035001",
    "ctsinhton":"909034011","tamnang":"909036006","xevang4banh":"909040001","baytrenkiem":"909041004",
    "xichdu":"909040013","sikibidi":"909042017","xemoto":"909043009","lambo":"909042012",
    "traitim2nguoi":"909043010","cauhon":"909043013","zombie":"909044012","parafal":"909045001",
    "maico":"909045009","ngoithien":"909045015","cuoingua":"909045003","phao":"909045005",
    "bapbenh":"909045012","6nong":"909046010","camco2":"909046013","sutbong":"909046015",
    "nhaybong":"909046016","lacdich":"909046017","ngoighe":"909047001","ghetinhyeu":"909047003",
    "canh1":"909047004","ngaivang2":"909047005","khoecup":"909047006","rasengan":"909047015",
    "bithuatlangla":"909047016","ketannaruto":"909047017","chayninja":"909047018","ketannaruto2":"909047019",
    "guitar":"909048003","piano":"909048004","nhaydanhtrong":"909048005","chacchac":"909048006",
    "ngu":"909048007","lacda":"909048009","camco3":"909048011","nhaydengiau":"909048012",
    "nailoong":"909049001","songaychoi":"909049006","p90":"909049010","oi":"909049013",
    "uethochuyensinh":"909050002","hoadon":"909050005","minato":"909050006","therings":"909050009",
    "sungcuoi":"909050020"
}

# ===== BOT FIX UID + PASSWORD FOR FRIEND API =====
FRIEND_UID = "4280450142"
FRIEND_PASSWORD = "0597DEB46F6A975DD6BD4A0C3313023D6F51A381CDBFDE6C085D408B21F4766B"

# ===== EMBED FUNCTION =====
def make_embed(title):
    return discord.Embed(
        title=title,
        description="🎮 **Xử lý thành công — vô game check lẹ đi ní 😭🔥**",
        color=discord.Color.green()
    )

# ===== COMMANDS =====
@bot.command()
async def emote(ctx, teamcode: str, uid: str, gun_name: str):
    gun = gun_name.lower()
    if gun not in EMOTE_LIST:
        available = ", ".join(EMOTE_LIST.keys())
        return await ctx.send(f"❌ Không tìm thấy emote `{gun}`!\n👉 Danh sách: `{available}`")
    emote_id = EMOTE_LIST[gun]
    api = f"https://ff-community-apiemoteessss.onrender.com/emote?teamcode={teamcode}&uid1={uid}&emote_id={emote_id}"
    try:
        requests.get(api, timeout=10)
    except:
        pass
    await ctx.send(embed=make_embed(f"🔥 EMOTE • {gun}"))

@bot.command(name="5")
async def five(ctx, uid: str):
    api = f"https://ff-community-apiemoteessss.onrender.com/5?uid={uid}&region=VN"
    try:
        requests.get(api, timeout=10)
    except:
        pass
    await ctx.send(embed=make_embed("⚡ API 5 EXECUTED"))

@bot.command()
async def ghost(ctx, teamcode: str):
    api = f"https://ghost-code-amph.onrender.com/execute_command_all?command=/bngx={teamcode}"
    try:
        requests.get(api, timeout=10)
    except:
        pass
    await ctx.send(embed=make_embed("👻 GHOST EXECUTED"))

@bot.command()
async def checkteam(ctx, teamcode: str):
    api = f"https://ff-community-apiemoteessss.onrender.com/?teamcode={teamcode}"
    try:
        req = requests.get(api, timeout=10)
        if req.status_code == 200:
            await ctx.send(embed=make_embed(f"✅ Teamcode `{teamcode}` OK!"))
        else:
            await ctx.send(f"❌ API lỗi: {req.status_code}")
    except Exception as e:
        await ctx.send(f"❌ Lỗi kết nối API: {e}")

@bot.command()
async def lag(ctx, teamcode: str):
    api = f"https://ff-community-apiemoteessss.onrender.com/lag?teamcode={teamcode}"
    try:
        req = requests.get(api, timeout=10)
        if req.status_code == 200:
            await ctx.send(embed=make_embed(f"🔧 Đã chạy lag cho `{teamcode}`"))
        else:
            await ctx.send(f"❌ API lỗi: {req.status_code}")
    except Exception as e:
        await ctx.send(f"❌ Không thể kết nối API: {e}")

# ===== FRIEND COMMANDS (CHỐNG DM RIÊNG, DÙNG UID + PASSWORD CỐ ĐỊNH) =====
@bot.command()
async def ketban(ctx, target_uid: str):
    if ctx.guild is None:
        return await ctx.send("❌ Lệnh này không được dùng trong DM!")
    api = f"https://danger-add-friend.vercel.app/adding_friend?uid={FRIEND_UID}&password={FRIEND_PASSWORD}&friend_uid={target_uid}"
    try:
        requests.get(api, timeout=10)
        await ctx.send(embed=make_embed(f"🤝 Đã gửi lời mời kết bạn tới `{target_uid}`!"))
    except:
        await ctx.send("❌ Lỗi API kết bạn!")

@bot.command()
async def xoa(ctx, target_uid: str):
    if ctx.guild is None:
        return await ctx.send("❌ Lệnh này không được dùng trong DM!")
    api = f"https://danger-add-friend.vercel.app/remove_friend?uid={FRIEND_UID}&password={FRIEND_PASSWORD}&friend_uid={target_uid}"
    try:
        requests.get(api, timeout=10)
        await ctx.send(embed=make_embed(f"❌ Đã xóa bạn với `{target_uid}`!"))
    except:
        await ctx.send("❌ Lỗi API xoá bạn!")

# ===== RUN BOT =====
bot.run(BOT_TOKEN)