import discord
from discord.ext import commands
from config import settings
from youtube_dl import YoutubeDL
import asyncio
import time



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


@client.command()
async def play(ctx, url):
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

    with YoutubeDL(ydl_options) as ydl:
        info = ydl.extract_info(url, download=False)
    url = info['url']
    song = info['title']
    duration = info['duration']

    durations.append(duration)
    songs.append(song)
    play_queue.append(url)

    while play_queue:
        if not voice_client.is_playing():
            voice_client.play(discord.FFmpegPCMAudio(play_queue[0], **ffmpeg_options))
            play_queue.pop(0)
            songs.pop(0)
        await asyncio.sleep(durations[0])
        durations.pop(0)




@client.command()
async def queue(ctx):
    text_channel = ctx.message.author
    await ctx.send(embed=discord.Embed(title=songs))



@client.command()
async def playE(ctx, url):
    play_queue.append(url)

    voice = ctx.message.author.voice
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    try:
        voice_client.is_connected()
    except:
        await voice.channel.connect()



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


client.run(settings['token'])
