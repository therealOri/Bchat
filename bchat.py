import dis_snek
import os
from datetime import datetime
from dotenv import load_dotenv

from dis_snek import listen, Snake, Activity, ActivityType, Intents, GuildText

#token
load_dotenv()
token = os.getenv('TOKEN')


def banner():
    return print("""

                ██████╗  ██████╗██╗  ██╗ █████╗ ████████╗
                ██╔══██╗██╔════╝██║  ██║██╔══██╗╚══██╔══╝
                ██████╔╝██║     ███████║███████║   ██║   
                ██╔══██╗██║     ██╔══██║██╔══██║   ██║   
                ██████╔╝╚██████╗██║  ██║██║  ██║   ██║   
                ╚═════╝  ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝                       
                                                    
      Made by Ori#6338 | @therealOri_ | https://github.com/therealOri


""")


def clear():
    os.system("clear||cls")


#bot config
client = Snake(
    intents=Intents.ALL,
    sync_interactions=True,
    delete_unused_application_cmds=True,
    activity=Activity(type=ActivityType.LISTENING, name="your one stop shop for music."), #This can be changed. It's just what I had for my bot.
    send_command_tracebacks=True
)


@listen()
async def on_ready():
    clear()
    while True:
        try:
            guild_list = [g for g in client.guilds]
            text = "\n".join(f"{idx}) {g.name}" for idx, g in enumerate(guild_list))
            banner()
            choice = int(input(f"{text}\n000) Quit\n\nChoose a guild: "))
            clear()
        except Exception:
            clear()
            print("The input you entered is not an integer. Please try again...")
            input('press enter to continue...')
            clear()
            continue

        if choice == 000:
            exit("Goodbye!")


        if choice >= len(guild_list):
            print("Invalid number/not an option. Please try again...")
            input('press enter to continue...')
            clear()
            continue
            

        while True:
            guild = guild_list[choice]
            channel_list = [channel for channel in guild.channels if isinstance(channel, GuildText)]
            text2 = "\n".join(f"{idx}) {ch.name}" for idx, ch in enumerate(channel_list))
            try:
                banner()
                choice2 = int(input(f"Currently in: {guild}\n\n{text2}\n000) Back\n\nChoose a channel: "))
                clear()
            except Exception:
                clear()
                print("The input you entered is not an integer. Please try again...")
                input('press enter to continue...')
                clear()
                continue

            if choice2 == 000:
                guild = None
                channel_list = None
                text2 = None
                break

            if choice2 >= int(len(channel_list)) or '':
                print("Invalid number/not an option. Please try again...")
                input('press enter to continue...')
                clear()
                continue

            else:
                clear()
                banner()
                channel = channel_list[choice]
                message = input("Message to send: ")
                await channel.send(message)
                clear()





client.start(token)
