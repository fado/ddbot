import random
import sys

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("No argument supplied.")
        sys.exit(1)

    numberOfDice = sys.argv[1].split('d')[0]
    numberOfSides = sys.argv[1].split('d')[1]
    difficulty = sys.argv[-1]

    print("Number of dice: " + numberOfDice)
    print("Number of sides: " + numberOfSides)
    print("Difficulty: " + difficulty)
    print("")

    results = []
    successes = 0

    for i in range(0, int(numberOfDice)):
        roll = random.randint(1, int(numberOfSides))
        results.append(roll)
        print("Rolling a dice: " + str(roll))

    for roll in results:
        if roll >= int(difficulty):
            successes += 1
        if roll == 1:
            successes -= 1

    if successes < 0:
        print("\nBotch!")
    else:
        print("\n" + str(successes) + " successes.")
