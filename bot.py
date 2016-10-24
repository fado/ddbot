import os
import random
from discord.ext import commands

description = '''Fado's Discord Dice Bot'''

bot = commands.Bot(command_prefix='.', description='')

@bot.command()
async def roll(result : str, *args, **kwargs):
    numberOfDice, numberOfSides = parse_dice(result)
    output = ""

    output += "[Rolling " + str(numberOfDice) + "d" + str(numberOfSides) + "] You rolled "

    try:
        results, output = do_roll(output, numberOfDice, numberOfSides)
    except ValueError as e:
        bot.say(e.args[0])

    if args:
        if args[0] == "vs":
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

        elif args[0] == "and" or args[2] == "and":
            if args[1] == "total" or args[3] == "total":
                total = 0
                for result in results:
                    total += result
                output += "\n\nTotal is " + str(total) + "."

    await bot.say(output)


def parse_dice(dice : str):
    return dice.split('d')[0], dice.split('d')[1]


def do_roll(output, numberOfDice, numberOfSides):
    results = []
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