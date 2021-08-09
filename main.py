import discord
from discord.ext import commands
from config import settings
from youtube_dl import YoutubeDL
import asyncio
import time
from requests import get




client = commands.Bot(command_prefix=settings['prefix'])  # создание "тела" бота

players = {}
play_queue = []
connection = False
count_songs = 0
songs = []


@client.command()
async def hello(ctx):
    author = ctx.message.author  # Объявляем переменную author и записываем туда информацию об авторе.
    await ctx.send(f'Hello, {author.mention}!')


def que(voice_client):

    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    songs.pop(0)
    if songs:
        try:
            if voice_client.is_connected():
                return discord.FFmpegPCMAudio(song, **ffmpeg_options)
        except:
            return


@client.command()
async def play(ctx, *arg):
    global count_songs
    voice = ctx.message.author.voice
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    try:
        voice_client.is_connected()
    except:
        await voice.channel.connect()
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    ydl_options = {'format': 'bestaudio', 'noplaylist': 'True'}
    ffmpeg_options = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    arg = " ".join(arg)
    with YoutubeDL(ydl_options) as ydl:
        try:
            get(arg)
        except:
            video = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
            await ctx.send('видосик: ' + video['webpage_url'])
        else:
            video = ydl.extract_info(arg, download=False)
    url = video['url']
    song = video['title']
    duration = video['duration']

    durations.append(duration)
    songs.append(song)
    play_queue.append(url)

    while play_queue:
        if not voice_client.is_playing():
            voice_client.play(discord.FFmpegPCMAudio(play_queue[0], **ffmpeg_options), after=que(voice_client))
        # await asyncio.sleep(durations[0])
        # durations.pop(0)



@client.command()
async def q(ctx):
    text_channel = ctx.message.author
    await ctx.send(embed=discord.Embed(title=songs))


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
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()


@client.command()
async def colorize(ctx):
    r, g, b = 255, 255, 255
    roles = ctx.message.author.roles
    role_name = roles[-1]
    role = discord.utils.get(ctx.guild.roles, name=str(role_name))
    while True:
        print(g, b)
        print(discord.Colour.from_rgb(r, g, b))
        await role.edit(color=(discord.Colour.from_rgb(r, g, b)))
        g -= 5
        b -= 5




client.run(settings['token'])
