import os
import beaupy
import discord
from discord import app_commands
import tomllib
import asyncio



def load_config(file_name):
    with open('config.toml', 'rb') as fileObj:
        config = tomllib.load(fileObj)
    return config




# Definitions
config = load_config('config.')
TOKEN = config["bot_token"]







def banner():
    print("""

                ██████╗  ██████╗██╗  ██╗ █████╗ ████████╗
                ██╔══██╗██╔════╝██║  ██║██╔══██╗╚══██╔══╝
                ██████╔╝██║     ███████║███████║   ██║   
                ██╔══██╗██║     ██╔══██║██╔══██║   ██║   
                ██████╔╝╚██████╗██║  ██║██║  ██║   ██║   
                ╚═════╝  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝                       
                                                    
           Made by @therealOri_ | https://github.com/therealOri

""")


def clear():
    os.system("clear||cls")


################### Client Setup ###################
class ManualBot(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)



intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
manual = ManualBot(intents=intents)
################### Client Setup ###################




@manual.event
async def on_ready():
    clear()
    dash=60
    while True:
        bot_guilds = manual.guilds
        guild_list = []
        for _ in bot_guilds:
            guild_list.append(_.name)

        guild_list += ["Quit?"]
        banner()
        print(f'What server would you like to talk in?\n{"-"*dash}\n')
        main_option = beaupy.select(guild_list, cursor_style="#ffa533")

        if not main_option:
            await manual.close()
            clear()
            print("Keyboard Interuption Detected!\nGoodbye <3")


        if guild_list[-1] in main_option:
            await manual.close()
            clear()
            print("Goodbye! <3")




        guild = discord.utils.get(manual.guilds, name=main_option)
        channel_list = []
        for channel in await guild.fetch_channels():
            if isinstance(channel, discord.TextChannel) and channel.permissions_for(guild.me).send_messages:
                channel_list.append(channel.name)
            else:
                pass
        channel_list += [" "]
        channel_list += [" "]
        channel_list += ["[+] -=-=-=- Back to server selector? -=-=-=- [+]"]

        while True:
            clear()
            banner()
            print(f'What channel would you like to talk in?\n(Currently in "{guild.name}")\n{"-"*dash}\n')
            second_option = beaupy.select(channel_list, cursor_style="#ffa533")


            if not second_option:
                clear()
                break

            if channel_list[-1] == second_option:
                clear()
                break

            if " " in second_option:
                clear()
                continue

            channel = discord.utils.get(guild.channels, name=second_option)
            while True:
                clear()
                banner()
                print(f'Currently in channel: ("{channel.name}")')
                msg = beaupy.prompt("What would you like to say? - (type 'q' to go back)")
                if msg.lower() == 'q':
                    break
                else:
                    await channel.send(msg)
                    continue




manual.run(TOKEN, reconnect=True, log_handler=None)
