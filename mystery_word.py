import random
import os

# function to start game
def start_game():
    """Starts the game by asking user for the desired mode and returns
    an int for which mode they select"""
    os.system("clear")
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
def get_word_list(difficulty_int, file="words.txt"):
    """Reads from words.txt locally and returns a word list based on 
    difficulty where 1 is 4-6 letters long, 2 is 6-8 letters long,
    and 3 or more is 8 or more letters long"""
    if difficulty_int == 1:
        difficulty_range = range(4,7)
    elif difficulty_int == 2:
        difficulty_range = range(6,9)
    else:
        # evil mode prompt
        print("Feeling brave I see...")
        chosen_character_length = 0
        try:
            chosen_character_length = int(input(
                "What's the maximum letter length you want to try? "))
        except:
            chosen_character_length = 100
        difficulty_range = range(1,chosen_character_length+1)
    
    with open(file, "r") as word_file:
        # add only stripped, lowercase versions of words of legal
        # lengths to the list
        game_word_list = [
            word.strip().lower()
            for word in word_file.readlines()
            if len(word.strip()) in difficulty_range
        ]
    return game_word_list

# cool sounding function that both displays the word in partially
# guessed form (if display=True) and checks if the game has been won
def the_chimera(guess_list, mystery_list, display=True):
    """takes two lists of single letters, the first of guesses,
    the second is of the target mystery word, where letters not
    guessed yet are lower case and guessed letters are upper case,
    printing the line if display=True, and returning the updated
    mystery_list a boolean of game_won"""

    new_mystery_list = []
    for letter in mystery_list:
        if letter in guess_list:
            new_mystery_list.append(letter.upper())
        else:
            new_mystery_list.append(letter)

    display_list = []
    game_won = False

    for letter in new_mystery_list:
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

    return new_mystery_list, game_won

# checks an evil template for win condition
def evil_win(evil_template):
    """accepts an evil template and checks if it is complete, returning True
    if it is"""
    if "_" in evil_template:
        return False
    else:
        return True

# "cut off one head, and two more take its place"
# this is the equivalent of the_chimera for evil mode
def the_hydra(guess_list, mystery_template, mystery_words_list):
    """accepts a guess_list, mystery_template, and mystery_words_list,
    returning a new mystery_template, new mystery_words_list, and the
    number of words eliminated on that step. Logic is to maximize remaining 
    words, given a guess."""
    number_of_words_eliminated = 0

    return mystery_template, mystery_words_list, number_of_words_eliminated

# main game function
def play_game(mystery_word):
    """plays a game of mystery word, accepting a string of the mystery word,
     returns bool play_again"""
    
    mystery_word_list = []
    for char in mystery_word:
        mystery_word_list.append(char.lower())
    
    # print("DEBUG", mystery_word_list)

    end_of_game = False
    wrong_answers_remaining = 8
    already_guessed_list = []
    while not end_of_game:
        os.system("clear")
        print("")
        the_chimera(already_guessed_list, mystery_word_list, display=True)
        print("")
        print("wrong answers left:", wrong_answers_remaining)
        print("letters you've guessed already", already_guessed_list)
        print("")
        guess = input("Guess a single letter (a-z): ")
        
        while (not guess.isalpha()) or (len(guess) != 1) or (guess in already_guessed_list):
            guess = input("Please guess a single letter (a-z) not already guessed: ")
        guess = guess.lower()
        already_guessed_list.append(guess)
        if guess in mystery_word_list:
            mystery_word_list, end_of_game = the_chimera(already_guessed_list, mystery_word_list, display=False)
            # print(mystery_word_list, "in main")
            if end_of_game:
                the_chimera(already_guessed_list, mystery_word_list, display=True)
                print("YOU WIN!")
        else:
            print("\a")
            wrong_answers_remaining -= 1
            if wrong_answers_remaining == 0:
                print("Sorry, you lose. The word was", mystery_word.upper(), "!")
                end_of_game = True
    return play_again_query()

# display funcion for the evil mode
def evil_display(mystery_word_template):
    """takes the mystery word template as an argument and displays it"""
    display_str = ""
    for char in mystery_word_template:
        display_str += char + " "
    print(display_str)
    return None

# makes a blank word template for evil mode
def make_evil_template(evil_words_list):
    """returns an evil word template of random length, accepting an evil_words_list
    and choosing the word length that maximizes potential words, which it then uses
    to return a template of that length"""

    # default value
    max_words_in_length_of = 1
    word_length_freq = {}

    # iterate through the words list and sort by frequency of length, 
    # discovering the highest and storing it in max_words_in_length_of
    for word in evil_words_list:
        try:
            word_length_freq[len(word)] += 1
        except:
            word_length_freq[len(word)] = 1
    
    def get_frequency_value(word_tup):
        """Given a tuple, returns the second value"""
        return word_tup[1]
    
    max_words_in_length_of = sorted(
        word_length_freq.items(), key=get_frequency_value, reverse = True)[0][0]
    
    # make a template of length max_words_in_length_of
    evil_word_template = []
    for _ in range(max_words_in_length_of):
        evil_word_template.append("_")
    return evil_word_template

# evil mode function
def play_evil_mode(evil_words_list):
    """plays the evil mode of mystery word, returns bool play_again"""
    # mystery_word_list = []
    # for char in mystery_word:
    #     mystery_word_list.append(char.lower())
    mystery_word_template = make_evil_template(evil_words_list)
    end_of_game = False
    wrong_answers_remaining = 8
    already_guessed_list = []
    words_eliminated = 0
    remaining_mystery_words = evil_words_list
    while not end_of_game:
        os.system("clear")
        print("")
        evil_display(mystery_word_template)
        print("")
        print("wrong answers left:", wrong_answers_remaining)
        print("letters you've guessed already", already_guessed_list)
        print("")
        print("Evil mode console:", len(evil_words_list), "words remaining.")
        print(words_eliminated, "words eliminated on previous step.")
        print("")
        guess = input("Guess a single letter (a-z): ")
        
        while (not guess.isalpha()) or (len(guess) != 1) or (guess in already_guessed_list):
            guess = input("Please guess a single letter (a-z) not already guessed: ")
        guess = guess.lower()
        already_guessed_list.append(guess)

        mystery_word_template, remaining_mystery_words, words_eliminated = the_hydra(
            already_guessed_list, mystery_word_template, remaining_mystery_words)
        
        if evil_win(mystery_word_template):
            end_of_game = True
            evil_display(mystery_word_template)
            print("YOU BEAT ME!!!")
            print("THAT'S IMPOSSIBLE!!!")
            print("NOOOOOOOOO!!!!!")
        else:
            print("\a")
            wrong_answers_remaining -= 1
            if wrong_answers_remaining == 0:
                print("You never had a chance. The word was", evil_words_list[0], "!")
                end_of_game = True

        # logic breakpoint
        # if guess in mystery_word_list:
        #     mystery_word_list, end_of_game = the_chimera(already_guessed_list, mystery_word_list, display=False)
        #     if end_of_game:
        #         the_chimera(already_guessed_list, mystery_word_list, display=True)
        #         print("YOU WIN!")
        # else:
        #     print("\a")
        #     wrong_answers_remaining -= 1
        #     if wrong_answers_remaining == 0:
        #         print("Sorry, you lose. The word was", mystery_word.upper(), "!")
        #         end_of_game = True

    return play_again_query()

# play again function
def play_again_query():
    """asks the user if they want to play again and returns a bool"""
    play_again_str = input("Play Again?(y/n) ")
    # any answer that starts with a "y" or "Y" is "yes", otherwise "no"
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

    # anything that starts with an f or F uses fun_words.txt, otherwise words.txt
    word_list_str = input("Which word list would you like to use, Fun or School? ")
    word_file = "words.txt"
    try:
        if word_list_str[0].lower() == "f":
            word_file = "fun_words.txt"
    except:
        pass
    game_list = get_word_list(mode_select, file=word_file)

    # if the user is playing on regular, select a random word
    if mode_select < 4:
        play_again = play_game(game_list[random.randrange(len(game_list))])
        if not play_again:
            exit()
    # if the user is playing on evil mode, pass the list of potential words
    elif mode_select == 4:
        play_again = play_evil_mode(game_list)
        if not play_again:
            exit()