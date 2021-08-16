import discord
from discord.ext import commands
from config import settings
from youtube_dl import YoutubeDL
import asyncio
from requests import get


intents = discord.Intents.default()
intents.presences = True
intents.members = True
client = commands.Bot(command_prefix=settings['prefix'], intents=intents)  # создание "тела" бота


loop_check = 0
urls = []
durations = []
titles = []
web_urls = []


@client.command()
async def hello(ctx):
    author = ctx.message.author  # Объявляем переменную author и записываем туда информацию об авторе.
    await ctx.send(f'Hello, {author.mention}!')


async def join(ctx):
    voice = ctx.message.author.voice
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    try:
        voice_client.is_connected()
    except AttributeError:
        await voice.channel.connect()


async def loop_checking():
    global urls, durations, titles
    if loop_check == 0:
        urls.pop(0)
        durations.pop(0)
        titles.pop(0)

    if loop_check == 2:
        urls.append(str(urls[0]))
        urls.pop(0)

        timing = durations[0]
        durations.append(int(timing))
        durations.pop(0)

        titles.append(titles[0])
        titles.pop(0)


async def player(ctx):
    global urls, durations, titles

    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    if not voice_client.is_playing():
        while urls:
            if not voice_client.is_playing():
                voice_client.play(discord.FFmpegPCMAudio(urls[0], **ffmpeg_options))

                embed = discord.Embed(colour=discord.Colour.from_rgb(255, 0, 0))
                embed.description = f'сейчас играет [{titles[0]}]({web_urls[0]})'
                await ctx.send(embed=embed)

                await asyncio.sleep(durations[0])
                await loop_checking()



@client.command()
async def play(ctx, *arg):
    await join(ctx)
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    ydl_options = {'format': 'bestaudio', 'noplaylist': 'True'}

    arg = " ".join(arg)
    with YoutubeDL(ydl_options) as ydl:
        try:
            get(arg)
        except:
            video = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]  # ищем на ютабе
        else:
            video = ydl.extract_info(arg, download=False)

    url = video['url']
    song = video['title']
    duration = video['duration']
    web_url = video['webpage_url']

    embed = discord.Embed()
    embed.description = f"добавляю очередняру [{song}]({web_url})"
    embed.colour = 65535
    await ctx.send(embed=embed)

    web_urls.append(web_url)
    durations.append(duration)
    titles.append(song)
    urls.append(url)

    await player(ctx)


@client.command()
async def loop(ctx):
    global loop_check
    text_channel = ctx.message.author

    if loop_check == 0:
        await ctx.send(embed=discord.Embed(title='активирую лупу песни', colour=65535))
        loop_check = 1

    elif loop_check == 1:
        await ctx.send(embed=discord.Embed(title='активирую лупу плейлиста', colour=65535))
        loop_check = 2

    elif loop_check == 2:
        loop_check = 0
        await ctx.send(embed=discord.Embed(title='деактивирую лупу', colour=65535))


@client.command()
async def remove(ctx, index):
    index = int(index)
    try:
        urls.pop(index - 1)
        durations.pop(index - 1)
        titles.pop(index - 1)
        await ctx.send('удалил микротрецк')
    except:
        await ctx.send('неверный индекс')


@client.command()
async def skip(ctx):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if urls:
        ctx.send('скипаю очередняру')
        voice_client.stop()
        await loop_checking()
        await player(ctx)
    else:
        ctx.send('а шо скипать то?')


@client.command()
async def q(ctx):
    await ctx.send('список очередняры:')
    print(titles)
    description = ''
    for index in range(len(titles)):
        description += f'{index + 1}. {titles[index]} \n'
    await ctx.send(f'```h\n{description}```')


@client.command()
async def leave(ctx):
    global connection
    if connection:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        await voice.disconnect()
    else:
        await ctx.send("да алё, я и так офнут")

@client.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send('ну поставил и чо')
    else:
        await ctx.send('ты шо дебик, я не в голосовом')


@client.command()
async def stop(ctx):
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    try:
        voice_client.stop()
        await ctx.send(embed=discord.Embed(title='эээ куда', colour=65535))
    except:
        await ctx.send(embed=discord.Embed(title='кто', colour=65535))


# Плэйлисты:

@client.command()
async def cpl(name):
    pl = open('playlists.py', 'w')
    pl.write(f'{name} = []')
    pl.close()


@client.command()
async def apl(name, song):
    with open('playlists.py', 'r') as pl:
        for line in pl.readlines():
            line = line.strip()
            line = line.split()




# по запуску бота:

r, g, b = 250, 80, 250
check = 0


@client.event
async def on_ready():
    member_id = 212902032867196929
    guild = client.guilds[0]
    member = discord.utils.get(guild.members, id=member_id)
    channel = discord.utils.get(guild.voice_channels, id=688193890078949385)

    while True:
        await asyncio.sleep(0.8)
        await member.edit(nick='🌌 | kEzy')
        await asyncio.sleep(0.8)
        await member.edit(nick='🌌 | keZy')
        await asyncio.sleep(0.8)
        await member.edit(nick='🌌 | kezY')
        await asyncio.sleep(0.8)
        await member.edit(nick='🌌 | keZy')
        await asyncio.sleep(0.8)
        await member.edit(nick='🌌 | kEzy')
        await asyncio.sleep(0.8)
        await member.edit(nick='🌌 | Kezy')


async def colorize():
    global r, g, b, check

    guild = client.guilds[0]
    role = discord.utils.get(guild.roles, name='ᅠᅠᅠᅠᅠᅠ🌸𝚂𝚊𝚔𝚞𝚛𝚊🌸')

    await role.edit(color=(discord.Colour.from_rgb(r, g, b)))

    if check == 0:
        g += 5
    elif check == 1:
        g -= 5

    if r == 250 and g == 180 and b == 250:
        check = 1
    elif r == 250 and g == 90 and b == 250:
        check = 0


client.run(settings['token'])
