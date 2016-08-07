import re
from random import choice
import sys

# Would be set to True when used to run the testing module to avoid unnecessarily verbose output on terminal
testing = False

# Game variables
possible_words = []
game_word = ''
curr_state = ''
correct = []
missed = []

def getWords(filename, length=None):
    """
        Returns all the words of a given length from the given global dictionary file
    """

    with open(filename) as f:
        l = []
        for words in f:
            word = words.strip().lower()
            if (length is None) or (length is not None and len(word) == length):
                l.append(word)
    return l


def guess():
    """
        The function which returns the next letter to guess, based on frequency heuristics
        and regex matching.
    """

    global possible_words, missed, correct

    table = {}
    tried = missed + correct

    regex = re.compile('^' + curr_state + '$')
    possible_words = [m.group(0) for l in possible_words for m in [regex.match(l)] if m]

    for word in possible_words:
        for letter in set(word):
            if letter in tried:
                continue
            elif letter not in table:
                table[letter] = 1
            else:
                table[letter] += 1

    return max(table, key=lambda k: table[k]) if table else None


def move(guessed_letter):
    """
        Tests the result of the guessed letter and changes the game
        state accordingly.
        Prints out the guessed letter, game state and wrongly guessed letters.
    """

    global game_word, correct, missed, curr_state, testing

    if not testing: print "guess: %c" % (guessed_letter)

    s = ''

    if guessed_letter in game_word:
        correct.append(guessed_letter)
    else:
        missed.append(guessed_letter)

    for letter in game_word:
        if letter in correct or letter == guessed_letter:
            s += letter
        else:
            s += '_'

    if not testing: print s, ' missed:', ','.join(missed), '\n'

    curr_state = s.replace('_', '.')

    return s


def intialize(word):
    """
        Function to initialize the game variables
    """

    global possible_words, missed, correct, game_word, curr_state, testing

    game_word = word
    possible_words = getWords('words.txt', len(game_word))
    missed = []
    correct = []

    l = len(game_word)

    curr_state = '.' * l

    if not testing: print '\n', '_' * l, ' missed:', '\n'


def play(word, TEST=False):
    """
        The central function that encapsulates the functioning of all the above implemented
        functions and simulates game play.
    """

    global missed, correct, testing

    testing = TEST

    intialize(word)
    letters = set([chr(i + 97) for i in range(0, 26)])

    while len(missed) < 6:
        s = guess()
        if s is None:
            s = choice(list(letters.difference(set(missed + correct))))

        state = move(s)
        if '_' not in state:
            if not testing: print "Game won!\n"
            return 1

    if not testing: print "Game lost!\n"
    return 0


def main():
    """
        The main function.Handles the input of the word as a command-line argument.
    """

    if len(sys.argv) < 2:
        print("Word is missing! To be given as command-line argument.")
    else:
        play(sys.argv[1])


if __name__ == "__main__":
    main()
