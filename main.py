import discord
from discord.ext import commands
from config import settings
import youtube_dl
import os
import ffmpeg

bot = commands.Bot(command_prefix=settings['prefix'])  # создание "тела" бота

players = {}
play_queue = []
connection = False


@bot.command()
async def hello(ctx):
    author = ctx.message.author  # Объявляем переменную author и записываем туда информацию об авторе.
    await ctx.send(f'Hello, {author.mention}!')


@bot.command()
async def play(ctx, url):
    global connection
    voice = ctx.message.author.voice
    if not connection:
        await voice.channel.connect()
        connection = True
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.play(url)






@bot.command()
async def leave(ctx):
    global connection
    if connection:
        voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
        await voice.disconnect()
    else:
        await ctx.send("да алё, я и так офнут")


@bot.command()
async def pause(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
        await ctx.send('ну поставил и чо')
    else:
        await ctx.send('ты шо дебик, я не в голосовом')


@bot.command()
async def stop(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    voice.stop()

bot.run(settings['token'])
