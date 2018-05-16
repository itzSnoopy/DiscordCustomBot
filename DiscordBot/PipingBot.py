# Bot libraries
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform

# Custom libraries
import sys
sys.path.append("lib")
import SearchEngines as engine
import youtube_dl as YoutubeDL

# Custom Solutions
import packCibertec as cb

# Profanity filter
from profanity.profanity import contains_profanity

# Bot specifics
client = Bot(description="Bot by itzSnoopy", command_prefix="", pm_help=False)
discord.opus.load_opus("opus")

# Global variables
gQuery = []
gEngine = ""
gURL = "https://www.youtube.com/watch?v=pAgnJDJN4VA"
gChannel = None
gVoiceClient = None
gOutput = []
gPlaylist = []
gPlayer = None
gState = False

# Main Loop


def main():
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

    # Help
    @client.command()
    async def helpme():
        await client.say("Bot in alpha version")
        return

    # Search
    @client.command()
    async def search(*args):
        # Checking for profanity
        if checkProfanity(*args):
            await client.say("Plz dont get me in trouble. -itzSnoopy")
            return

        # Open variables
        global gQuery
        global gEngine
        global gOutput

        # Assisgn value to gQuery and gEngine
        # Check formatting
        if len(args) > 1:
            gEngine = engine.select(args[0])
            gQuery = []

            # Create the query
            for index in range(len(args)):
                if index != 0:
                    gQuery.append(args[index])

            await client.say("Searching [" + gEngine + "] for [" + " ".join(gQuery) + "]")
        # If its not formatted correctly
        else:
            await client.say("Please use the correct format: search [ENGINE] [QUERY]")

        # Do the search
        gOutput = engine.search(gEngine, *gQuery)

        # Check if output isnt NULL
        if gOutput:
            # Echo results
            for item in gOutput:
                await client.say(item)

        return

    # Join Channel
    @client.command()
    async def join(*args):
        # Open variables
        global gChannel
        global gVoiceClient
        global gPlayer

        # Check formatting/lenght for now only
        if len(args) > 1:
            await client.say("Please enter a valid VOICE CHANNEL NAME")
            return

        # Check if already in channel
        if gChannel:
            if gChannel.name == args[0]:
                await client.say("Bot already in channel: " + gChannel.name)
                return
            else:
                print(gChannel.name)
                # print(gVoiceClient.Channel.name) need to find if already in voice channel

        # Search channels for desired channel
        for channel in client.get_all_channels():
            if channel.name == args[0]:
                gChannel = channel
                await client.say("Joining Channel: " + gChannel.name)

                # Join voice channel if possible
                if str(gChannel.type) == "voice":
                    gVoiceClient = await client.join_voice_channel(gChannel)
                else:
                    print(gChannel.type)
                    print("not joining")

                return

        # If no channel gets matched
        await client.say("No channel with name [" + args[0] + "] found")

        return

    # Play
    @client.command()
    async def play(*args):
        # Open variables
        global gChannel
        global gVoiceClient
        global gPlaylist
        global gPlayer

        global gURL  # for testing

        # Check channel connectivity status
        if not gChannel or not gVoiceClient:
            await client.say("Join a channel first: join [CHANNEL NAME]")
            return

        # Check search method
        if args[0].isdigit() and len(args) == 1:
            print("Searching by index")
            print(args[0])
        else:
            print("Searching by TAG")

        # Manage player
        if gPlayer:
            if gPlayer.is_playing():
                print("Already playing something...")
                gPlayer.stop()

        if str(gChannel.type) != "voice":
            await client.say("Current channel does not support audio features")
            return

        # Start player
        gPlayer = await gVoiceClient.create_ytdl_player(gURL)
        gPlayer.start()

        return

    # Revisar horario
    @client.command()
    async def horario(*args):
    #async def horario():
        await client.say("Revisando horario...")

        #cb.checkHorario()
        cb.checkHorario(*args)

        await client.send_file(client.get_channel("445728179504676864"), "output.html")

        return

    @client.command()
    async def notas():
        await client.say("Revisandro notas...")

        cb.checkNotas()

        await client.send_file(client.get_channel("445728179504676864"), "output.html")

        return

#
#   METHODS
#

# Check for profanity


def checkProfanity(*args):
    for word in args:
        if contains_profanity(word):
            print(word)
            return True

    return False


# Startup
if __name__ == "__main__":
    main()

    # Bot token
    client.run('')
    print("program ended")
    input("Enter to exit")
