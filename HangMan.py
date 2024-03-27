from random import randint
from sys import exit
from os import startfile

def getWord(wordList: str) -> str:
    """Opens a list of words then picks a random word and returns that word"""
    wordlist = open(wordList, 'r')

    words = [line for line in wordlist]

    randomWord = words[randint(0, len(words) - 1)].strip().lower()
    wordlist.close()

    return randomWord

def wordToLines(word: str) -> list:
    """Converts the word to a bunch of lines"""
    wordLines: list = []
    wordArray: list = [letter for letter in word]
    for letter in range(len(wordArray)):
        if wordArray[letter].isspace(): wordLines.append(' ')
        else:                           wordLines.append('_')

    return wordLines

def guess(letter: str) -> None:
    """Takes a guess from the player and adds the guess to an already guessed pool and a wrong guess pool"""
    global guessWord, guessedLetters, hiddenWord, incorrectGuesses, wrongLetters
    if letter in guessedLetters:
        print("You have already guessed that letter")
    elif letter in guessWord:
        for i in range(len(guessWord)):
            if guessWord[i] == letter:
                hiddenWord[i] = letter  # I have no idea how to lose one indent

        guessedLetters.append(letter)
    else:
        guessedLetters.append(letter)
        wrongLetters.append(letter)
        incorrectGuesses += 1

def strArrayToText(array: list) -> str:
    """Converts the array of strings into one single string"""
    strWord = ''
    for i in range(len(array)):
        strWord += array[i]
    return strWord

def wrongLetterToStr(array: list) -> str:
    """Turns the wrong letter array into a str"""
    strWord = ''
    for i in range(len(array)):
        strWord = strWord + ' ' + array[i]
    return strWord

def again() -> None:
    """If the player wants to play again, it re-opens the file"""
    while True:
        try:
            answer = True if input("Do you want to play again? Yes or No?").lower()[0] == 'y' else False
        except IndexError:
            continue

        if not answer:
            exit(0)

        startfile(__file__)
        exit(0)

def win() -> None:
    """If the player wins, increase the number in their account by one"""
    winAmount = registeredIndex[username][1] + 1
    registeredIndex[username][1] = winAmount
    loseAmount = registeredIndex[username][2]
    try:
        winrate = winAmount / loseAmount
    except ZeroDivisionError:
        winrate = winAmount
    print(f"\nYou Win! You have won {winAmount} times! You have lost {loseAmount} times\nYou have a win to lose rate of {winrate:.2f}\n")
    with open('./HangManRegisteredUsers.txt', 'w') as file:
        file.write(str(registeredIndex))
    again()

def lose() -> None:
    """If the player loses, increase the number in their account by one"""
    global guessWord
    file = open('./HangManRegisteredUsers.txt', 'r')
    winAmount = registeredIndex[username][1]
    loseAmount = registeredIndex[username][2] + 1
    registeredIndex[username][2] = loseAmount
    winrate = winAmount / loseAmount
    print(f"\nYou Lose the word was {guessWord}! You have won {winAmount} times! You have lost {loseAmount} times\nYou have a win to lose rate of {winrate:.2f}\n")
    file = open('./HangManRegisteredUsers.txt', 'w')
    file.write(str(registeredIndex))
    again()

def loginSystem() -> None:
    """A massive thing that lets the player create an account or login to an existing account. Then writes the result to a file
       registeredIndex: [password -> str, win -> int, lose -> int, logged_in -> bool]"""

    global username, password, registeredIndex
    registeredIndex = {}
    try:
        file = open('./HangManRegisteredUsers.txt', 'r')
    except FileNotFoundError:
        file = open('./HangManRegisteredUsers.txt', 'w')
        file.write('{}')
        file.close()
        file = open('./HangManRegisteredUsers.txt', 'r')

    registeredIndex = eval(file.readline())

    # testing to see if someone is logged in and then leaving the function
    for keys in registeredIndex:
        if registeredIndex[keys][3] is not True:
            continue
        username = keys
        try:
            signOut = True if input('Do you want to sign out? ').lower()[0] == 'y' else False
        except IndexError:
            signOut = False
        if signOut:
            registeredIndex[keys][3] = False
            username = ''
            file = open('./HangManRegisteredUsers.txt', 'w')
            file.write(str(registeredIndex))
            exit(0)
        return

    login = True if input("Do you want to login or create an account? ").lower()[0] == 'l' else False
    while login:
        username = input("Username: ").lower()
        if username not in registeredIndex:
            print("We could not find you. Please create an account.")
            username = ''
            login = False
            break
        password = input("Password: ")
        while password != registeredIndex[username][0]:
            password = input("Incorrect Password. Please try again: ")
        print("You have successfully logged in")
        registeredIndex[username][3] = True
        return

    while not login:
        username = input("Create a username: ").lower()
        while username in registeredIndex:
            username = input("Username already taken. Pick a new username: ")
        password = input("Create a password: ")

        registeredIndex[username] = [password, 0, 0, False]

        file = open('./HangManRegisteredUsers.txt', 'w')
        file.write(str(registeredIndex))

        input("Account successfully made. Press enter to close window")
        exit(0)


# setting up the basic variables
guessedLetters:   list = []
wrongLetters:     list = []
incorrectGuesses: int  = 0

guessWord:  str  = getWord('hangManWords.txt')
hiddenWord: list = wordToLines(guessWord)

username: str = ''
password: str = ''
registeredIndex: dict = {str(username): [password, 0, 0, False]}

loops: int = 0

# logging in
loginSystem()
while True:

    hangmanUI = [f" HANGMAN \n"
                 f"  ____   Wrong Letters:\n"
                 f"      |  {wrongLetterToStr(wrongLetters)}\n"
                 f"      |  \n"
                 f"      |  \n"
                 f"  ^^^^^^^^^ \n"
                 f"{strArrayToText(hiddenWord)}",
                 f" HANGMAN \n"
                 f"  ____   Wrong Letters:\n"
                 f"  O   |  {wrongLetterToStr(wrongLetters)}\n"
                 f"      |  \n"
                 f"      |  \n"
                 f"  ^^^^^^^^^ \n"
                 f"{strArrayToText(hiddenWord)}",
                 f" HANGMAN \n"
                 f"  ____   Wrong Letters:\n"
                 f"  O   |  {wrongLetterToStr(wrongLetters)}\n"
                 f"  I   |  \n"
                 f"      |  \n"
                 f"  ^^^^^^^^^ \n"
                 f"{strArrayToText(hiddenWord)}",
                 f" HANGMAN \n"
                 f"  ____   Wrong Letters:\n"
                 f"  O   |  {wrongLetterToStr(wrongLetters)}\n"
                 f"  I   |  \n"
                 f" /    |  \n"
                 f"  ^^^^^^^^^ \n"
                 f"{strArrayToText(hiddenWord)}",
                 f" HANGMAN \n"
                 f"  ____   Wrong Letters:\n"
                 f"  O   |  {wrongLetterToStr(wrongLetters)}\n"
                 f"  I   |  \n"
                 f" / \\  |  \n"
                 f"  ^^^^^^^^^ \n"
                 f"{strArrayToText(hiddenWord)}",
                 f" HANGMAN \n"
                 f"  ____   Wrong Letters:\n"
                 f"  O   |  {wrongLetterToStr(wrongLetters)}\n"
                 f"--I   |  \n"
                 f" / \\  |  \n"
                 f"  ^^^^^^^^^ \n"
                 f"{strArrayToText(hiddenWord)}",
                 f" HANGMAN \n"
                 f"  ____   Wrong Letters:\n"
                 f"  O   |  {wrongLetterToStr(wrongLetters)}\n"
                 f"--I-- |  \n"
                 f" / \\  |  \n"
                 f"  ^^^^^^^^^ \n"
                 f"{strArrayToText(hiddenWord)}"]

    print(hangmanUI[incorrectGuesses])

    if incorrectGuesses >= 6:
        lose()
    if strArrayToText(hiddenWord) == guessWord:
        win()

    if loops == 0:
        loops += 1

    guessLetter = input("\nGuess a letter: ").lower()

    while len(guessLetter) != 1:
        if len(guessLetter) > 1:
            guessLetter = input("\nYou provided two letters instead of one. Guess a letter: ").lower()
        elif len(guessLetter) == 0:
            guessLetter = input("\nYou didn't provide a letter. Guess a letter: ").lower()

    guess(guessLetter)
