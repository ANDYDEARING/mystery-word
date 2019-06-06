import random

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
    mode_choice = None
    # return the choice as long as the input is valid
    while True:
        try:
            mode_choice = int(input("Choose (1-4) "))
        except:
            pass
        if mode_choice in range(1,5):
            return mode_choice
        elif mode_choice == 5:
            exit()
        else:
            print("Invalid Entry, try again")

def get_word_list(difficulty_int):
    """Reads from words.txt locally and returns a word list based on 
    difficulty where 1 is 4-6 letters long, 2 is 6-8 letters long,
    and 3 or more is 8 or more letters long"""
    if difficulty_int == 1:
        difficulty_range = range(4,7)
    elif difficulty_int == 2:
        difficulty_range = range(6,9)
    else:
        # 100 is more than enough for the longest word in english 
        # (45 at the moment)
        difficulty_range = range(8,100)
    with open("words.txt", "r") as word_file:
        game_word_list = [
            word
            for word in word_file.readlines()
            if len(word) in difficulty_range
        ]
    return game_word_list

# initialize the game
mode_select = (start_game())
game_list = get_word_list(mode_select)
print(game_list[random.randrange(len(game_list))])

# play the game

# choose the word