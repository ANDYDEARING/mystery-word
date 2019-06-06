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

# get a word list for the selected difficulty
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
            word.strip()
            for word in word_file.readlines()
            if len(word) in difficulty_range
        ]
    return game_word_list

def the_chimera(guess_list, mystery_list, display=True):
    """takes two lists of single letters, the first of guesses,
    the second is of the target mystery word, where letters not
    guessed yet are lower case and guessed letters are upper case,
    printing the line if display=True, and returning a boolean of game_won"""

    for letter in mystery_list:
        if letter in guess_list:
            letter = letter.upper()
    
    display_list = []
    game_won = False

    for letter in mystery_list:
        if letter == letter.upper():
            display_list.append(letter)
        else:
            display_list.append("_")
    if "_" not in display_list:
        game_won = True
    if display == True:
        display_str = ""
        for letter in display_list:
            display_str += letter + " "
        print(display_str)

    return game_won


# main game function
def play_game(mystery_word):
    """plays a game of mystery word, accepting a string of the mystery word,
     returns bool play_again"""
    
    mystery_word_list = []
    for char in mystery_word:
        mystery_word_list.append(char.lower())
    
    print("DEBUG", mystery_word_list)

    end_of_game = False
    wrong_answers_remaining = 8
    already_guessed_list = []
    while not end_of_game:
        print("")
        print(the_chimera(already_guessed_list, mystery_word_list, display=True))
        print("")
        print("wrong answers left:", wrong_answers_remaining)
        print("letters you've guessed already", already_guessed_list)
        print("")
        guess = input("Take a guess: ")
        
        while (not guess.isalpha()) or (len(guess) != 1) or (guess in already_guessed_list):
            guess = input("Please guess a single letter (a-z) not already guessed: ")
        already_guessed_list.append(guess.lower())
        if guess in mystery_word_list:
            end_of_game = the_chimera(already_guessed_list, mystery_word_list, display=False)
            if end_of_game:
                print("YOU WIN!")
        else:
            print("It's not there...")
            wrong_answers_remaining -= 1
            if wrong_answers_remaining == 0:
                print("Sorry, you lose.")
                end_of_game = False
    
    return play_again_query()

# evil mode function
def play_evil_mode(evil_word_list):
    """plays the evil mode of mystery word, returns bool play_again"""
    print("Coming soon!")
    return play_again_query()

# play again function
def play_again_query():
    """asks the user if they want to play again and returns a bool"""
    play_again_str = input("Play Again?(y/n) ")
    try:
        if play_again_str[0].lower() == "y":
            play_again = True
        else:
            play_again = False
    except:
        play_again = False
    return play_again

# initialize and run the game till exit
while True:
    mode_select = (start_game())
    game_list = get_word_list(mode_select)
    if mode_select < 4:
        play_again = play_game(game_list[random.randrange(len(game_list))])
        if not play_again:
            exit()
    elif mode_select == 4:
        play_again = play_evil_mode(game_list)
        if not play_again:
            exit()
