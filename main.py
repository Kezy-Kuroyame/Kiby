import discord
from discord.ext import commands
from config import settings
import youtube_dl
import os
import ffmpeg
import lavalink

client = commands.Bot(command_prefix=settings['prefix'])  # создание "тела" бота

players = {}
play_queue = []
connection = False
count_songs = 0


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
        print('2')
    except:
        await voice.channel.connect()
    print('3')
    voice_client = discord.utils.get(client.voice_clients, guild=ctx.guild)
    server = ctx.message.guild

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        return

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")

    voice_client.play(discord.FFmpegPCMAudio("song.mp3"))


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
