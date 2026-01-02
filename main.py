import discord
from discord.ext import commands
import asyncio
import threading
import os

# ================== TOKENS ==================
TOKENS = [
    os.getenv("TOKEN1"),
    os.getenv("TOKEN2"),
    os.getenv("TOKEN3"),
    os.getenv("TOKEN4"),
    os.getenv("TOKEN5"),
]

# ================== VOICE CHANNELS ==================
VOICE_CHANNEL_IDS = [
    1454765414637637849,
    1387502642724474950,
    1452087596648759459,
    1382464909631029400,
    1329182037432733778
]

# ================== COMMAND CHANNEL ==================
COMMAND_CHANNEL_ID = 1227007968868831273

# ================== ALLOWED USERS ==================
BASE_ALLOWED_USERS = [
    731124230795690074,
    325803798566010881
]

# ================== BOT START ==================
def start_bot(token, voice_channel_id):
    if not token:
        return

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True

    bot = commands.Bot(command_prefix="!", intents=intents)
    allowed_users = BASE_ALLOWED_USERS.copy()

    def allowed(ctx):
        return (
            ctx.author.id in allowed_users
            and ctx.channel.id == COMMAND_CHANNEL_ID
        )

    @bot.event
    async def on_ready():
        print(f"🤖 {bot.user} جاهز ✅")

    # ================== دخول ==================
    @bot.command()
    async def دخول(ctx):
        if not allowed(ctx):
            return

        if ctx.guild.voice_client:
            await ctx.send("❌ البوت داخل الروم بالفعل")
            return

        channel = bot.get_channel(voice_channel_id)
        if not channel:
            await ctx.send("❌ الروم الصوتي غير موجود")
            return

        vc = await channel.connect()
        await vc.guild.change_voice_state(
            channel=channel,
            self_deaf=True
        )
        await ctx.send("✅ دخل الروم الصوتي (Deaf)")

    # ================== خروج ==================
    @bot.command()
    async def خروج(ctx):
        if not allowed(ctx):
            return

        vc = ctx.guild.voice_client
        if vc:
            await vc.disconnect()
            await ctx.send("✅ خرج من الروم الصوتي")
        else:
            await ctx.send("❌ البوت مو داخل روم")

    # ================== تصريح ==================
    @bot.command()
    async def تصريح(ctx):
        if not allowed(ctx):
            return

        msg = "✅ المصرح لهم:\n" + "\n".join(f"<@{u}>" for u in allowed_users)
        await ctx.send(msg)

    # ================== إضافة ==================
    @bot.command()
    async def أضف(ctx, user: discord.Member):
        if not allowed(ctx):
            return

        if user.id in allowed_users:
            await ctx.send("⚠️ الشخص مصرح له مسبقًا")
        else:
            allowed_users.append(user.id)
            await ctx.send(f"✅ تم إضافة {user.mention}")

    # ================== حذف ==================
    @bot.command()
    async def حذف(ctx, user: discord.Member):
        if not allowed(ctx):
            return

        if user.id not in allowed_users:
            await ctx.send("⚠️ الشخص غير موجود")
        else:
            allowed_users.remove(user.id)
            await ctx.send(f"✅ تم حذف {user.mention}")

    # ================== ساعد ==================
    @bot.command()
    async def ساعد(ctx):
        if not allowed(ctx):
            return

        await ctx.send(
            "**📜 الأوامر:**\n"
            "!دخول\n"
            "!خروج\n"
            "!تصريح\n"
            "!أضف @شخص\n"
            "!حذف @شخص\n"
            "!ساعد"
        )

    loop.run_until_complete(bot.start(token))


# ================== RUN ALL BOTS ==================
threads = []

for token, channel_id in zip(TOKENS, VOICE_CHANNEL_IDS):
    t = threading.Thread(
        target=start_bot,
        args=(token, channel_id),
        daemon=True
    )
    t.start()
    threads.append(t)

# يمنع السكربت من الإغلاق
for t in threads:
    t.join()
