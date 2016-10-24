import asyncio
import os

import discord
import random
import sys

client = discord.Client()

@client.event
async def on_read():
    print("Logged in as ")
    print(client.user.name)
    print(client.user.id)
    print("-------------")

@client.event
async def on_message(message):
    if message.content.startswith('!dice') or message.content.startswith("!test"):

        output = ""

        try:
            dice = str(message.content).split(' ')[1]

            numberOfDice = dice.lower().split('d')[0]
            numberOfSides = dice.lower().split('d')[1]
            difficulty = str(message.content).split(' ')[-1]

            if len(message.content.split(' ')) != 4:
                raise ValueError

            if int(numberOfSides) != 20 and message.content.startswith("!test"):
                await client.send_message(message.channel, "Can only test on a d20.")
                return

            results = []
            successes = 0

            output += "Rolling " + numberOfDice + "d" + numberOfSides + ": "
            for i in range(0, int(numberOfDice)):
                roll = random.randint(1, int(numberOfSides))
                results.append(roll)
                output += str(roll) + " "

            for roll in results:
                if message.content.startswith("!dice"):
                    if roll >= int(difficulty):
                        successes += 1
                    if roll == 1:
                        successes -= 1
                if message.content.startswith("!test"):
                    if roll <= int(difficulty):
                        successes += 1

            if successes < 0:
                output += "Botch!"
            else:
                output += "\n" + str(successes) + " successes."
        except ValueError:
            await client.send_message(message.channel, "Invalid input. Friel detected.")

        await client.send_message(message.channel, output)

try:
    client.run(os.environ['DISCORD_TOKEN'])
except KeyError:
    print("Environment variable not found.")




