# Bot libraries
import discord
import asyncio
from discord.ext.commands import Bot
from discord.ext import commands
import platform

# Custom libraries
import sys
sys.path.append("lib")
import UserManagement as uMng

# Custom Solutions
import packCibertec as ciber

# Profanity filter
from profanity.profanity import contains_profanity

# Bot specifics
client = Bot(description="Bot by itzSnoopy", command_prefix="", pm_help=True)

# Global variables

gState = True  # Can the bot process commands right now?
gUserID = 0  # ID of user requesting data
gUsername = ""  # Username of user
gUser = ""  # user need for testing

# Main Loop


def main():
    # Events
    #
    #
    @client.event
    async def on_ready():  # Loading bot into server
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
        print("List of Servers:")
        for item in client.servers:
            print(item.id + ": " + item.name)
            print("\n\n")

        return await client.change_presence(game=discord.Game(name="Ready to roll"))

    @client.event
    async def on_message(message):  # Pre-process message
        global gUserID
        global gUsername
        global gUser
        global gState

        if message.author.name == "TestBot":
            return

        # aceptar minusculas/mayusculas en la primera letra
        message.content = message.content[:1].lower() + message.content[1:]

        # print(gUserID)
        # print(gUsername)

        if gState:
            gState = False  # Declare bot is busy

            gUserID = message.author.id
            gUsername = message.author.name
            gUser = message.author

            if not checkProfanity(str(message.content)):  # Check for profanity
                # Do the command
                await client.process_commands(message)
            else:
                # await client.say("Comando censurado")
                print("comando censurado")
            gState = True  # Declare bot is free
            print("Finishing command")

            return
        else:
            print("busy")

            return

    # Commands
    #
    #

    # Registro
    @client.command()
    async def registrar(*args):
        global gUserID
        global gUsername

        # 0: validation result(T/F), 1: Names or login error message
        result = ["ERROR", "ERROR"]

        # Check format of ID and PASS
        if not args or not len(args) == 2 or not args[0][0] == "i":
            await client.say("Usa el formato correcto: <registrar i201812345 P4$$W0RD>")
            return

        # TODO check if already registered

        await client.say("Probando usuario y contraseña")

        result = ciber.testUser(args)

        if result[0] == "Validated":
            await client.say("Usuario validado correctamente")
            await client.say("Bienvenid@ " + result[1])
        else:
            await client.say("Error en la validacion: " + result[1])
            return

        uMng.insertUser([gUserID, gUsername, args[0], args[1], result[1]])

        return

    # Horario
    @client.command()
    async def horario(*args):
        global gUserID

        if not args:  # When registered use this
            args = [gUserID]
            print("buscando con id: " + gUserID)
        elif len(args) == 2:  # Sin registrarse
            print("buscando con iCode y Pass")
        else:
            await client.say("Porfavor registrate <registrar [USUARIO] [CONTRASEÑA]> o usa usuario y contraseña <horario i201812345 P4$$W0RD>")
            return

        data = uMng.getUserData(args)

        if data[0] == "error":
            await client.say("Error en el login:\n" + data[1])
            return

        ciber.checkHorario(data)

        await client.send_file(gUser, "output.html")

        await client.say("Horario enviado!")

        return

    # Notas
    @client.command()
    async def promedio(*args):
        global gUserID

        data = uMng.getUserData([gUserID])

        if data[0] == "error":
            # print(str(data))
            await client.say("No te encuentras registrad@, usa: registrar i201812345 P4$$W0RD")

            return

        await client.say("Revisando promedio")

        if len(args) == 1:
            data.append(args[0])

        print(data)

        results = ciber.checkPromedio(data)

        if len(results) > 1:
            for i in range(len(results)):
                if results[i][3] == "":
                    results[i][3] = "   "

                await client.say(" || ".join(results[i]))

            await client.say("Puedes revisar tus notas detalladas de cada curso usando promedio + codigo")
        else:
            await client.say("No se encontraron cursos")

        return

    # Help

    @client.command()
    async def helpme():
        await client.say("Bot in beta version")
        return

    # Test module
    @client.command()
    async def test(*args):
        global gUser

        print("\n\nRunning test module<\n\n")
        print("*args:" + str(*args))
        print("args:" + str(args))
        print("----------------------------------------------")

        await client.send_message(gUser, "hi")

        print("----------------------------------------------")
        print("\n\n>End of test module\n\n")
        return

# Methods
#
#

# Check for profanity


def checkProfanity(args):
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
