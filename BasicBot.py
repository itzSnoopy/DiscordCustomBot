# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform

# Library
import profanity.profanity
import sys
sys.path.append("lib")

import youtube as yt

# Here you can modify the bot's prefix and description and wether it sends help in direct messages or not.
client = Bot(description="Basic Bot by Habchy#1665",
             command_prefix="!", pm_help=False)

# This is what happens everytime the bot launches. In this case, it prints information like server count, user count the bot is connected to, and the bot id in the console.
# Do not mess with it because the bot can break, if you wish to do so, please consult me or someone trusted.


@client.event
async def on_ready():
    print('Logged in as ' + client.user.name + ' (ID:' + client.user.id + ') | Connected to ' +
          str(len(client.servers)) + ' servers | Connected to ' + str(len(set(client.get_all_members()))) + ' users')
    print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(
        discord.__version__, platform.python_version()))
    print('--------')
    print('Use this link to invite {}:'.format(client.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
    print('--------')
    print('Support Discord Server: https://discord.gg/FNNNgqb')
    print('Github Link: https://github.com/Habchy/BasicBot')
    print('--------')
    # Do not change this. This will really help us support you, if you need support.
    print('You are running BasicBot v2.1')
    print('Created by Habchy#1665')
    # This is buggy, let us know if it doesn't work.
    return await client.change_presence(game=discord.Game(name='PLAYING STATUS HERE'))

# Lists of comands


@client.command()
async def helpme(*args):
    await client.say("Hola pablo")


@client.command()
async def search(*args):
    for item in args:
        if profanity.profanity.contains_profanity(item):
            await client.say("Search has been censored")
        else:
            await client.say("Searching...")

            output = yt.search(*args)

            for item in output:
                await client.say(item)

    """
    await client.say(output[0])
    await client.say(output[1])
    """

"""
TODO: DEVVEDIN CLASS NEEDS TESTING
"""
@client.command()
async def list():
    list = yt.getList()
    if list:
        for item in list:
            await client.say(item)
            await client.say("Use command with option !command -[number]")

"""
TODO:FUTURE COMMANDS THEORETICAL
BASE ON LEN(*STR)
GET ITEM IN ARRAY
SHOULD CONFORT TO -COMMANDEXTRA
SWITCH IT TO ADDED COMMANDS
"""
@client.command()
async def query(*args):
    await client.say("add link to playlist")

    # Show then place in queue
    # Command option for place in certain position -> ARRRAY STARTS AT 0
    # Echo final position until test success

@client.command()
async def list(*args):
    await client.say("list all entries in playlist")

    # Show first X amount of entires then total amount as total row
    # Command to upload whole file
    # Command to show next song(s)
    # Command to show all -> should only work by admin

@client.command()
async def play(*args):
    await client.say("play link then continue queue")

    # Add commands extra for play then clear que, play then do something else

"""
ADD SLEEP BREAK BETWEEN COMMANDS
ADD ADMIN RECOGNITION
ADD WHITELIST FOR USERS
APPLY CURRENT PROFANITY FILTER TO EVERYTHING!!
COMMAND TO KILL BOT
COMMAND TO SLEEP BOT
COMMAND TO RUN SCRIPT ONLY BY ADMIN
COMMAND TO SHOW CURRENT TIME
COMMAND TO SHOW CURRENT RESOURCES BEING USED
COMMAND TO RESTART BOT
COMMAND FOR FLAVOUR
COMMAND FOR EXTRA STUFF INCLUDING IMAGES
CREATE MEDIA FOLDER
CREATE SCRIPT LIBRARY ELSEWHERE
"""


# Basic Bot was created by Habchy#1665
# Please join this Discord server if you need help: https://discord.gg/FNNNgqb
# Please modify the parts of the code where it asks you to. Example: The Prefix or The Bot Token
# This is by no means a full bot, it's more of a starter to show you what the python language can do in Discord.
# Thank you for using this and don't forget to star my repo on GitHub! [Repo Link: https://github.com/Habchy/BasicBot]

# The help command is currently set to be not be Direct Messaged.
# If you would like to change that, change "pm_help = False" to "pm_help = True" on line 9.
