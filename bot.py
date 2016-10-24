import os
import discord
import random
from discord.ext import commands

client = discord.Client()
bot = commands.Bot(command_prefix='.', description='')

@bot.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await bot.say(left + right)


@client.event
async def on_read():
    print("Logged in as ")
    print(client.user.name)
    print(client.user.id)
    print("-------------")


@client.event
async def on_message(message):

    if message.content.startswith('.roll'):
        output = ""

        try:
            if len(message.content.split(' ')) == 2:
                dice, numberOfDice, numberOfSides = parse_roll(message.content)

                output += "[Rolling " + str(numberOfDice) + "d" + str(numberOfSides) + "] "
                results, output = do_roll(output, numberOfDice, numberOfSides)

            elif len(message.content.split(' ')) == 4:
                successes = 0

                dice, numberOfDice, numberOfSides = parse_roll(message.content)
                difficulty = str(message.content).split(' ')[-1]

                output += "[Rolling " + str(numberOfDice) + "d" + str(numberOfSides) + " vs " + difficulty + "] "
                results, output = do_roll(output, numberOfDice, numberOfSides)

                for roll in results:
                    if roll >= int(difficulty):
                        successes += 1
                    if roll == 1:
                        successes -= 1

                if successes < 0:
                    output += "Botch!"
                else:
                    output += "\n" + str(successes) + " successes."

            await client.send_message(message.channel, output)

        except ValueError as error:
            await client.send_message(message.channel, error.args[0])


def parse_roll(message):
    dice = str(message).split(' ')[1]
    try:
        numberOfDice = int(dice.lower().split('d')[0])
        numberOfSides = int(dice.lower().split('d')[1])
    except ValueError:
        raise ValueError("Error. Some dice parameters might not have been numbers.")

    if numberOfDice > 100:
        raise ValueError("Error. Someone tried to roll too many dice.")

    return dice, numberOfDice, numberOfSides


def do_roll(output, numberOfDice, numberOfSides):
    results = []
    for i in range(0, numberOfDice):
        roll = random.randint(1, numberOfSides)
        results.append(roll)
        output += str(roll) + " "

    return results, output


try:
    client.run(os.environ['DISCORD_TOKEN'])
except KeyError:
    print("Environment variable not found.")




