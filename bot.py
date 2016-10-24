import os
import random
from discord.ext import commands

description = '''Fado's Discord Dice Bot'''

bot = commands.Bot(command_prefix='.', description='')

@bot.command()
async def roll(result : str, *args, **kwargs):
    numberOfDice, numberOfSides = parse_dice(result)
    output = ""

    try:
        output += "[Rolling " + str(numberOfDice) + "d" + str(numberOfSides) + "] You rolled "
        results, output = do_roll(output, numberOfDice, numberOfSides)
    except ValueError as e:
        await bot.say("Error: " + str(e))
        return

    for i in range(0, len(args)):
        if args[i] == "vs":
            successes = 0

            for result in results:
                if result >= int(args[1]):
                    successes += 1
                if result == 1:
                    successes -= 1

            output += "\nDifficulty was " + str(args[1]) + " and you scored "
            if successes < 0:
                output += "a Botch!"
            else:
                output += str(successes) + " successes."
        try:
            if args[i] == "and" and args[i + 1] == "total":
                    total = 0
                    for result in results:
                        total += result
                    output += "\n\nTotal is " + str(total) + "."
        except IndexError:
            await bot.say("Error: Invalid input, but I can roll your dice anyway.")

    await bot.say(output)


def parse_dice(dice : str):
    return dice.split('d')[0], dice.split('d')[1]


def do_roll(output, numberOfDice, numberOfSides):
    results = []

    if int(numberOfDice) > 100:
        raise ValueError("Too many dice. I will only roll up to 100 at a time.")

    try:
        for i in range(0, int(numberOfDice)):
            roll = random.randint(1, int(numberOfSides))
            results.append(roll)
            output += str(roll)
            if i < int(numberOfDice) - 1:
                output += ", "
        output += "."

    except ValueError:
        raise ValueError("Invalid input.")

    return results, output

try:
    bot.run(os.environ['DISCORD_TOKEN'])
except KeyError:
    print("Environment variable not found.")