import random
import os

# make a string from a template for dicitionaries
def make_string_from_template(template):
    """takes a template list and returns a string of cap letters and underscores"""
    template_str = ""
    for letter in template:
        template_str += letter
    return template_str

# return the second value of a tuple
def get_frequency_value(word_tup):
        """Given a tuple, returns the second value"""
        return word_tup[1]

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

# check to see if a template is compatible with a word
def is_compatible(evil_template, word):
    """accepts a template and a string word, returning a boolean that
    says True if they're compatible and False if they're not"""
    compatible = True
    word_as_list = []
    for char in word:
        word_as_list.append(char)
    if len(evil_template) != len(word_as_list):
        return False
    for index in range(len(evil_template)):
        if (word_as_list[index] != evil_template[index]) and (evil_template[index] != "_"):
            compatible = False
    return compatible

# "cut off one head, and two more take its place"
# this is the equivalent of the_chimera for evil mode
def the_hydra(guess, mystery_template, mystery_words_list):
    """accepts the latest guess, the mystery_template, and mystery_words_list,
    returning a new mystery_template, new mystery_words_list, and the
    number of words eliminated on that step. Logic is to maximize remaining 
    words, given a guess."""
    number_of_words_eliminated = 0
    new_mystery_words_list = []
    new_mystery_template = []

    # count the words that do not contain the guess
    guess_not_in_word_freq = 0
    for word in mystery_words_list:
        if guess not in word:
            guess_not_in_word_freq += 1

    # start a dictionary with frequencies of template compatability
    template_freq = {}
    # add the value of words that do not contain the guess with an index of mystery_template
    template_freq[make_string_from_template(mystery_template)] = guess_not_in_word_freq

    # make a dictionary of templates by frequency
    for word in mystery_words_list:
        temp_template = make_template(mystery_template, guess, word)
        if guess not in word:
            template_freq[make_string_from_template(mystery_template)] += 1
        elif template_freq.get(make_string_from_template(temp_template)) == None:
            template_freq[make_string_from_template(temp_template)] = 1
        else:
            template_freq[make_string_from_template(temp_template)] += 1
    
    # the new mystery template is the template with the highest frequency, which means
    # the highest number of potential words
    new_mystery_template = sorted(
        template_freq.items(), key=get_frequency_value, reverse=True)[0][0]
    
    # new_mystery_words_list is the mystery_words_list members compatible with the new template
    for word in mystery_words_list:
        if is_compatible(new_mystery_template, word):
            new_mystery_words_list.append(word)
    
    number_of_words_eliminated = len(mystery_words_list) - len(new_mystery_words_list)
    return new_mystery_template, new_mystery_words_list, number_of_words_eliminated

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
def make_init_evil_template(evil_words_list):
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
    
    max_words_in_length_of = sorted(
        word_length_freq.items(), key=get_frequency_value, reverse = True)[0][0]
    
    # make a template of length max_words_in_length_of
    evil_word_template = []
    for _ in range(max_words_in_length_of):
        evil_word_template.append("_")
    return evil_word_template

# makes a new template based on an existing template, a letter, and a word
def make_template(old_template, guess_letter, word):
    """accepts a template, a letter, and a potential word sring of the same length
    and returns a new template that updates the old_template with changes, if any"""
    # converts the string word into a list of characters
    word_list = []
    for letter in word:
        word_list.append(letter)
    
    # makes a template using either the existing character or the letter if matched
    new_template = []
    for index in range(len(old_template)):
        if word_list[index].upper() == guess_letter.upper():
            new_template.append(guess_letter.upper())
        else:
            new_template.append(old_template[index])
    return new_template


# eliminate all members of a list that are not the passed length
def trunc_evil_list(evil_words_list, length):
    """accepts a word_list and a length, returning a new list of items
    from the old list with the passed length"""
    new_list = []
    for word in evil_words_list:
        if len(word) == length:
            new_list.append(word)
    return new_list

# evil mode function
def play_evil_mode(evil_words_list):
    """plays the evil mode of mystery word, returns bool play_again"""
    mystery_word_template = make_init_evil_template(evil_words_list)
    end_of_game = False
    wrong_answers_remaining = 8
    already_guessed_list = []
    words_eliminated = 0
    remaining_mystery_words = trunc_evil_list(evil_words_list, len(mystery_word_template))
    while not end_of_game:
        os.system("clear")
        print("")
        evil_display(mystery_word_template)
        print("")
        print("wrong answers left:", wrong_answers_remaining)
        print("letters you've guessed already", already_guessed_list)
        print("")
        print("Evil mode console:", len(remaining_mystery_words), "words remaining.")
        print(words_eliminated, "words eliminated on previous step.")
        print("")
        guess = input("Guess a single letter (a-z): ")
        while (not guess.isalpha()) or (len(guess) != 1) or (guess in already_guessed_list):
            guess = input("Please guess a single letter (a-z) not already guessed: ")
        guess = guess.lower()
        already_guessed_list.append(guess)
        mystery_word_template, remaining_mystery_words, words_eliminated = the_hydra(
            guess, mystery_word_template, remaining_mystery_words)
        
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
                print("You never had a chance. The word was", remaining_mystery_words[0], "!")
                end_of_game = True
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
        elif word_list_str == "test":
            word_file = "test.txt"
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