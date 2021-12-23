# Time Converter Bot
import config
import discord
from discord.ext.commands import Bot

from datetime import datetime, timedelta

bot = Bot(command_prefix='$')

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')

@bot.event
async def on_message(message):
    if not message.author == bot.user:
        msg = message.content.lower()
        if msg.startswith("test"):
            await message.channel.send('Hey there!')
        elif msg.startswith("now"):
            pst = datetime.today()
            ppst = pst.strftime("%H:%M:%S")
            hst = (pst - timedelta(hours=2)).strftime("%H:%M:%S")
            await message.channel.send(f"Current time (PST): {ppst}\nCurrent time (HST): {hst}")
        else:
            try:
                t = containsTime(msg)
                if t:
                    hour = t[0]
                    ampm = "AM"
                    if hour > 12:
                        ampm = "PM"
                    minute = "{:02d}".format(t[1])
                    # Fix author for time conversion
                    if message.author.name == config.HST_username:
                        nHour = (hour + 2)
                        n_am = "AM"
                        if nHour > 12:
                            n_am = "PM"
                        res = f"{hour%12}:{minute} {ampm} HST is equivalent to {nHour%12}:{minute} {n_am} PST"
                    else:
                        # TODO: handle hourly edge cases, refactor into method
                        nHour = (hour - 2)
                        n_am = "AM"
                        if nHour < 0:
                            nHour += 12
                            n_am = "PM"
                        elif nHour > 12:
                            n_am = "PM"
                        res = f"{hour%12}:{minute} {ampm} PST is equivalent to {nHour%12}:{minute} {n_am} HST"
                    await message.channel.send(res)
            except:
                await message.channel.send("Are you trying to break me? Don't do that")

            
def containsTime(msg):
    global targets
    msg = msg.split()

    hour = -1

    for word in msg:
        if word == "am":
            hour = 0
            break
        elif word == "pm":
            hour = 12
            break
        elif word == "at":
            hour = -2

    if hour == -1:
        return False
    elif hour == -2:
        hour = 12

    minute = 0

    for i in range(len(msg)):
        if i>0 and (msg[i] == "am" or msg[i] == "pm"):
            if ":" in msg[i-1]:
                t = msg[i-1].split(":")
                if len(t) == 2:
                    if t[0].isnumeric():
                        hour += int(t[0])
                    if t[1].isnumeric():
                        minute += int(t[1])
                    break
                else:
                    return False
            if msg[i-1].isnumeric():
                hour += int(msg[i-1])
                break
        elif i < len(msg) - 1 and msg[i] == "at":
            if ":" in msg[i+1]:
                t = msg[i+1].split(":")
                if len(t) == 2:
                    if t[0].isnumeric():
                        hour += int(t[0])
                    if t[1].isnumeric():
                        minute += int(t[1])
                    break
                else:
                    return False
            if msg[i+1].isnumeric():
                hour += int(msg[i+1])
                break
            else:
                return False
    add = minute//60
    hour += add
    hour %= 24
    minute %= 60

    return hour, minute


# Token for TimeConverter
bot.run(config.time_converter_bot)