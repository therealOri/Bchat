import os
import beaupy
import discord
from discord import app_commands
import tomllib
import asyncio
import logging



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
        main_menu_options = ['Dm a User?', 'Send Messages?', 'Exit?'] # updating the menu to get ready for future updates.
        banner()
        print(f'What would you like to do?\n{"-"*dash}\n')
        menu_option = beaupy.select(main_menu_options, cursor_style="#ffa533")
        
        if not menu_option:
            clear()
            print("Keyboard Interuption Detected!\nGoodbye <3")
            await manual.close() # This isn't the best way or probably the right way to close out and exit..but it's what I've got for now.


        # Send DMs
        if main_menu_options[0] in menu_option:
            clear()
            flag=True
            while flag:
                user_id = beaupy.prompt("User ID")
                if not user_id:
                    clear()
                    break
                try:
                    user_id = int(user_id)
                    flag=False
                except Exception as e:
                    clear()
                    input(f'Oops, an error has occured...\nError: {e}\n\nPress "enter" to try again...')
                    clear()
                    continue

            if flag == True:
                clear()
                continue

            msg = beaupy.prompt("Message to send")
            member = await manual.fetch_user(int(user_id))
            await member.send(msg)
            input(f'@{member.name} has been DMed!\n\nPress "enter" to continue...')
            clear()
            continue



        # Send Messages
        if main_menu_options[1] in menu_option:
            clear()
            while True:
                bot_guilds = manual.guilds
                guild_list = []
                for _ in bot_guilds:
                    guild_list.append(_.name)

                guild_list += ["Back?"]
                banner()
                print(f'What server would you like to talk in?\n{"-"*dash}\n')
                guild_option = beaupy.select(guild_list, cursor_style="#ffa533")

                if not guild_option:
                    clear()
                    break

                if guild_list[-1] in guild_option:
                    clear()
                    break

                guild = discord.utils.get(manual.guilds, name=guild_option)
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
                    print(f'What channel would you like to talk in?\n(Currently in name="{guild.name}" id="{guild.id}")\n{"-"*dash}\n')
                    channel_option = beaupy.select(channel_list, cursor_style="#ffa533")

                    if not channel_option:
                        clear()
                        break

                    if channel_list[-1] == channel_option:
                        clear()
                        break

                    if " " in channel_option:
                        clear()
                        continue

                    channel = discord.utils.get(guild.channels, name=channel_option)
                    while True:
                        clear()
                        banner()
                        print(f'Currently in channel: ("{channel.name}")')
                        msg = beaupy.prompt("What would you like to say? - (type 'q' to go back)")
                        if msg.lower() == 'q':
                            break

                        if msg.lower() == 'f+':
                            #upload file from file path
                            attachment = beaupy.prompt("File path - (drag & drop)")
                            if not attachment or attachment.lower() == 'q':
                                break
                            else:
                                attachment = attachment.replace('\\', '').strip()
                                d_file = discord.File(attachment)
                                try:
                                    await channel.send(file=d_file)
                                except Exception as e:
                                    clear()
                                    input(f'Oops..and error has occured. (need permission to attach files in this channel.)\nError: {e}\n\nPress "enter" to continue...')
                                continue

                        else:
                            await channel.send(msg)
                            continue




manual.run(TOKEN, reconnect=True, log_level=logging.INFO)
