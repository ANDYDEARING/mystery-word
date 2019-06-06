
# function to start game
def start_game():
    """Starts the game by asking user for the desired mode and returns
    an int for which mode they select"""
    print("")
    print("Welcome to MYSTERY WORD")
    print("Select mode:")
    print("")
    print("1. Easy (4-6 letters)")
    print("2. Normal (6-8 letters")
    print("3. Hard (8+ letters)")
    print("4. Evil Mode")
    print("5. Quit")
    while True:
        try:
            mode_choice = int(input("Choose (1-4) "))
        except:
            pass
        if mode_choice in range(1,6):
            return mode_choice
        else:
            print("Invalid Entry, try again")
print(start_game())

# initialize the game
with open("words.txt", "r") as word_file:
    wordlist = word_file.readlines()

# play the game

# choose the word