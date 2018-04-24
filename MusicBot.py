# Bot libraries
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform

# Custom libraries
import sys
sys.path.append("lib")
import SearchEngines as eng
from ctypes.util import find_library
import youtube_dl

# Profanity filter
import profanity.profanity

# Bot specifics
client = Bot(description="Music Bot by itzSnoopy",
             command_prefix="", pm_help=False)


# On Run command
@client.event
async def on_ready():
    print("Logged in as " + client.user.name + " (ID:" + client.user.id + ") | Connected to " +
          str(len(client.servers)) + " servers | Connected to " + str(len(set(client.get_all_members()))) + " users")
    print("---------")
    print("Current Discord.py Version: {} | Current Python Version: {}".format(
        discord.__version__, platform.python_version()))
    print("---------")
    print("Use this link to invite {}:".format(client.user.name))
    print("https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8".format(client.user.id))
    print("--------")
    print("Github Link: https://github.com/itzSnoopy/DiscordCustomBot")
    print("--------")

    print("List of Channels: ")
    for item in client.get_all_channels():
        print(item.id + ": " + item.name)
    print("--------")

    return await client.change_presence(game=discord.Game(name="Ready to roll"))


# Commands
@client.command()
async def helpme():
    await client.say("Bot in alpha version")


# Search command
@client.command()
async def search(*args):
    query = []
    engine = ""

    # Check for profanity
    for item in args:
        if profanity.profanity.contains_profanity(item):
            print(item)
            await client.say("plz dont get me in trouble. -itzSnoopy")
            return

    # Check if command is formatted
    if args[0]:
        engine = eng.select(args[0])

        if engine == "google" and args[0] != "google":
            query = args
        else:
            for index in range(len(args)):
                query.append(args[(index + 1)])

                if (index + 2) >= len(args):
                    break

    # If command isnt formatted
    else:
        await client.say("Please use the format: search [ENGINE] [QUERY TO SEARCH]")
        return

    # Do the Search
    await client.say("searching " + engine + "...")
    output = eng.search(engine, *query)

    # Check if output isnt empty
    if output:
        for item in output:
            await client.say(item)


# Play command
@commands.command(pass_context=True, no_pm=True)
async def play(self, ctx):
    channel = ctx.message.author.voice_channel

    state = self.get_voice_state(ctx.message.server)

    state.voice.move_to(channel)

    return True


@client.command()
async def join():
    discord.opus.load_opus("opus")
    #HARDCODED UNTIL I DECIDE HOW TO HANDLE SEARCH CACHE
    url = "https://www.youtube.com/watch?v=9W44NWYwa1g"

    voice_channel = None

    for channel in client.get_all_channels():
        if channel.name == "stream":
            voice_channel = channel

    print(voice_channel.id)

    vc = await client.join_voice_channel(channel)

    player = await vc.create_ytdl_player(url)
    player.start()


# Bot token
client.run('DISCORD BOT TOKEN GOES HERE')
