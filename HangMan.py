import random
from sys import exit
from os import startfile

def getWord() -> str:
    wordlist = open('hangManWords.txt', 'r')

    words = [line for line in wordlist]

    randomWord = words[random.randint(0, len(words) - 1)].strip().lower()
    wordlist.close()

    return randomWord

def wordToLines(word: str) -> list:
    wordLines: list = []
    wordArray: list = [letter for letter in word]
    for letter in range(len(wordArray)):
        if wordArray[letter].isspace(): wordLines.append(' ')
        else:                           wordLines.append('_')

    return wordLines

def guess(letter: str):
    global guessWord, guessedLetters, hiddenWord, incorrectGuesses, wrongLetters

    if letter in guessedLetters:
        print("You have already guessed that letter")
    elif letter in guessWord:
        for i in range(len(guessWord)):
            if guessWord[i] == letter:
                hiddenWord[i] = letter

        guessedLetters.append(letter)
    else:
        guessedLetters.append(letter)
        wrongLetters.append(letter)
        incorrectGuesses += 1

def strArrayToText(array: list) -> str:
    strWord = ''
    for i in range(len(array)):
        strWord += array[i]
    return strWord

def wrongLetterToStr(array: list) -> str:
    strWord = ''
    for i in range(len(array)):
        strWord = strWord + ' ' + array[i]
    return strWord

def again() -> None:
    while True:
        try:
            answer = input("Do you want to play again? ").lower()[0]
            break
        except IndexError:
            continue
    while True:
        if answer == 'y':
            startfile(__file__)
            exit()
        elif answer == 'n':
            exit(0)
        else:
            while True:
                try:
                    answer = input("You didn't provide a proper answer. Yes or No?").lower()[0]
                    break
                except IndexError:
                    continue

def win() -> None:
    file = open('./HangManRegisteredUsers.txt', 'r')
    winAmount = registeredIndex[username][1] + 1
    registeredIndex[username][1] = winAmount
    loseAmount = registeredIndex[username][2]
    try:
        winrate = winAmount / loseAmount
    except ZeroDivisionError:
        winrate = winAmount
    print(f"\nYou Win! You have won {winAmount} times! You have lost {loseAmount} times\nYou have a win to lose rate of {winrate:.2f}\n")
    file = open('./HangManRegisteredUsers.txt', 'w')
    file.write(str(registeredIndex))
    again()

def lose() -> None:
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
    # keep list of usernames in a dictionary and have an array assigned to the key.
    # [password -> str, win -> int, lose -> int, logged_in -> bool]
    # need to do some file handling
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
        if registeredIndex[keys][3] is True:
            username = keys
            signOut = True if input('Do you want to sign out? ').lower()[0] == 'y' else False
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
        if username in registeredIndex:
            password = input("Password: ")
            while True:
                if password == registeredIndex[username][0]:
                    print("You have successfully logged in")
                    registeredIndex[username][3] = True
                    return
                else:
                    password = input("Incorrect Password. Please try again: ")
        else:
            print("We could not find you. Please create an account.")
            username = ''
            login = False

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


guessedLetters:   list = []
wrongLetters:     list = []
incorrectGuesses: int  = 0

guessWord:  str  = getWord()
hiddenWord: list = wordToLines(guessWord)

username: str = ''
password: str = ''
registeredIndex: dict = {str(username): [password, 0, 0, False]}

loops: int = 0

loginSystem()
while True:
    if incorrectGuesses >= 6:
        lose()
    if strArrayToText(hiddenWord) == guessWord:
        win()

    if loops == 0:
        print(strArrayToText(hiddenWord))
        loops += 1

    guessLetter = input("\nGuess a letter: ").lower()

    while len(guessLetter) != 1:
        if len(guessLetter) > 1:
            guessLetter = input("\nYou provided two letters instead of one. Guess a letter: ").lower()
        elif len(guessLetter) == 0:
            guessLetter = input("\nYou didn't provide a letter. Guess a letter: ").lower()

    guess(guessLetter)

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
    # print(f"Wrong Guesses: {wrongLetterToStr(wrongLetters)}")
    # print(strArrayToText(hiddenWord))
