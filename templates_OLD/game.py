#-----------------------------Startup----------------------------#
from random import choice
from random import randint
words = [line.rstrip().upper() for line in open("wordsLong.txt")]

def startup():
    global name
    name = input("Greetings traveller!\nWhat is your name?\n--> ")
    print(name + "... Ahh, yes. The prophecies have spoken of such a name." + "\n" + "You have been chosen to face the mightiest Mechs of the land in a battle of wits and determination. Only one shall rise victorious, will it be you?\n\n")
    tutorial_state = input("Would you like to recieve a tutorial? (Yes/No)\n--> ").lower()
    while tutorial_state != "yes" and tutorial_state != "no": tutorial_state = input("Please do not toy with me traveller, a simple yes or no should suffice.\n--> ").lower()
    if tutorial_state == "yes": print("\nAlright traveller, welcome to 'Words with Enemies'! The game consists of five rounds, with each round presenting the player with a set of letters (the amount of which will vary according to your chosen level of difficulty). From these letters, the player is to form a valid word that will be assigned a score based on how many unique characters are in it when compared to the opponent's word. Both the player and the opponent form their word from the same letter set.\nFor example, in the letter set'T C M U L E P O A K', the player forms the word 'TOP' while the opponent forms the word 'POTLUCK. POT has 0 unique characters when compared to POTLUCK, while POTLUCK has 4 unique letters. Thus, the opponent would win the round.\n The winner of the game is determined by the total score, calculated by finding the sum of each round's points.\n New players should first play against the Robo Cub to experience the game mechanics.\n\nGood luck, traveller.\n")


def main():
    global AI
    AI = {"1": "Robo Cub", "2": "Iron Sensei", "3": "V-07-TR-0N"}
    global difficulty
    difficulty = input("\n\nWho shall you face?\n1) Robo Cub\n2) Iron Sensei\n3) V-07-TR-0N\n--> ")
    while difficulty != "1" and difficulty != "2" and difficulty != "3" : difficulty = input("My apologies, I have never heard of such a warrior, please select one of the above.\n--> ")
    if difficulty == "1": print("The Robo Cub has been plaguing the nearby forests with his mild personality and quiet groans... Do take care of him, won't you?\n\n")
    if difficulty == "2": print("Beware traveller, the Iron Sensei is not as easy to defeat as the simple Robo Cub. This Sensei of Steel has spent years studying an ancient text. This text, spoken of in legend, is referred to only as \'The Dictionary\'... Sounds ominous, does it not?\n\n") 
    if difficulty == "3": print("V-07-TR-0N? Traveller, you must truly be the chosen one if you can liberate us from V-07-TR-0N's rein. His intellect is god-like and has known no defeat.\nGood luck, traveller...\n\n")

#----------------------------Mechanics---------------------------#
    
def letterArray():
    global array
    array = "".join([choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for x in range(0, int(difficulty) * 2 + 8)])
    while (int(array.count("A")) + int(array.count("E")) + int(array.count("I")) + int(array.count("O")) + int(array.count("U"))) < int(difficulty) + 1:
        array = list(array)
        array[randint(0, (len("".join(array)) - 1))] = choice("AEIOU")
    return list(array)


def allWords():
    global valid_words
    valid_words = {}
    for word in words:
        buffer_word = word
        buffer_letters = "".join(letters)
        for y in range(0, len(letters)):
            for x in range(0, len(word)):
                if buffer_word[x] == buffer_letters[y]:
                    buffer_word = buffer_word.replace(str(buffer_word[x]), "*", 1)
                    buffer_letters = buffer_letters.replace(str(buffer_letters[y]), "*", 1)
        if buffer_word == "*"*len(word):
            valid_words[word] = len(word)
    return valid_words


def aiWord():
    global ai_word
    value_list = []
    for value in valid_words.values():
        if value not in value_list:
            value_list.append(value)
    value_list.sort(key=int)
    if difficulty == "1": ai_list = [word for word, length in valid_words.items() if length == value_list[0]]
    if difficulty == "2": ai_list = [word for word, length in valid_words.items() if length != value_list[0] or value_list[-1]]
    if difficulty == "3": ai_list = [word for word, length in valid_words.items() if length == value_list[-1]]
    if ai_list != []: ai_word = choice(ai_list).upper()
    else: ai_word = ""
    return ai_word

def isValid():
    if player_word in valid_words.keys():
        return True
    else:
        return False
    

def winDetect():
    global player_score
    global ai_score
    left, right = player_word, ai_word
    for x in range(0, len(left)):
        for y in range(0, len(right)):
            if left[x] == right[y]:
                left = left.replace(left[x], "*", 1)
                right = right.replace(right[y], "*", 1)
    left = left.replace("*", "")
    right = right.replace("*", "")
    player_score, ai_score = player_score + len(left), ai_score + len(right)
    
    output = []
    res1 = str(name + ": " + left + "      " + AI[difficulty] + ": " + right + " ")
    res2 = str(name + ": +" + str(len(left)) + "|" + AI[difficulty] + ": +" + str(len(right)) + " ")

    output.append("O" + "-"*len(res1) + "O")

    if len(res1) % 2 == 0:
        padding1 = str(" "*(int(len(res1) / 2) - 6))
        padding2 = str(" "*(int(len(res1) / 2) - 5))
        output.append("|" + padding1 + "<-Results->" + padding2 + "|")
    else:
        padding = str(" "*(int(len(res1) / 2) - 5))
        output.append("|" + padding + "<-Results->" + padding + "|")

    output.append("|" + res1 + "|")
    output.append("| " + " "*(len(res1) - 2) + " |")

    if len(left) > len(right):
        if (len(res1) - len(name + " Wins!")) % 2 == 0:
            padding = str(" "*int(int(len(res1) - len(name + " Wins!")) / 2))
            output.append("|" + padding + name + " Wins!" + padding + "|")
        else:
            padding1 = str(" "*(int(int(len(res1) - len(name + " Wins!")) / 2) + 1))
            padding2 = str(" "*int(int(len(res1) - len(name + " Wins!")) / 2))
            output.append("|" + padding1 + name + " Wins!" + padding2 + "|")
    elif len(left) < len(right):
        if (len(res1) - len(AI[difficulty] + " Wins!")) % 2 == 0:
            padding = str(" "*int(int(len(res1) - len(AI[difficulty] + " Wins!")) / 2))
            output.append("|" + padding + AI[difficulty] + " Wins!" + padding + "|")
        else:
            padding1 = str(" "*(int(int(len(res1) - len(AI[difficulty] + " Wins!")) / 2) + 1))
            padding2 = str(" "*int(int(len(res1) - len(AI[difficulty] + " Wins!")) / 2))
            output.append("|" + padding1 + AI[difficulty] + " Wins!" + padding2 + "|")
    else:
        padding = str(" "*(int(len(res1) / 2) - 2))
        output.append("|" + padding + "Draw!" + padding + "|")

    output.append("| " + " "*(len(res1) - 2) + " |")
    
    if len(res1) % 2 == 0:
        padding = str(" "*(int(len(res1) / 2) - 5))
        output.append("|" + padding + "<-Scores->" + padding + "|")
    else:
        padding1 = str(" "*(int(len(res1) / 2) - 4))
        padding2 = str(" "*(int(len(res1) / 2) - 5))
        output.append("|" + padding1 + "<-Scores->" + padding2 + "|")
        
    if (len(res1) - len(res2)) % 2 == 0:
        padding = str(" "*int(int(len(res1) - len(res2)) / 2))
        output.append("|" + padding + res2 + padding + "|")
    else:
        padding1 = str(" "*(int(int(len(res1) - len(res2)) / 2) + 1))
        padding2 = str(" "*int(int(len(res1) - len(res2)) / 2))
        output.append("|" + padding1 + res2 + padding2 + "|")
        
    output.append("O" + "-"*len(res1) + "O")
    return "\n".join(output)


def turn():
    global letters
    global player_word
    letters = letterArray()
    allWords()
    print("\nRound: " + str(rnum) + " - " + name + " vs. " + AI[difficulty] + " (" + str(player_score) + "-" + str(ai_score) + ")\n" +  "-"*((int(difficulty) * 2 + 8) * 2 + 14) + "\nYour Letters: " + str(" ".join(list(letters))) + "\n" + "-"*((int(difficulty) * 2 + 8) * 2 + 14) + "\n")
    player_word = input("Your Word: (Leave empty to Pass)\n--> ").upper()
    while isValid() == False:
        if player_word == "": print("\n" + name + " has passed Round " + str(rnum)); break
        player_word = input("\nI'm sorry traveller, " + player_word + " is an invalid word. Try again.\nYour Word: (Leave empty to Pass)\n--> ").upper()
    if isValid() == True: print("\n" + name + " selects " + player_word)
    aiWord()
    if ai_word != "": print(AI[difficulty] + " selects " + ai_word + "\n")
    else: print(AI[difficulty] + " has passed round " + str(rnum) + "\n")
    print(winDetect())


def finalResults():
    print("\n\nFINAL RESULTS\n-------------\n\nFinal Score: (" + str(player_score) + "-" + str(ai_score) + ")")
    if player_score > ai_score: print(name + " has defeated " + AI[difficulty] + "!")
    if player_score < ai_score: print(AI[difficulty] + " has defeated " + name + "!")
    if player_score == ai_score: print(name + " has tied with " + AI[difficulty] + "!")
    
#------------------------------Game------------------------------#

startup()

cont = 0
while cont != "no":
    main()
    player_score, ai_score = 0, 0
    
    for x in range(1, 6):
        rnum = x
        turn()
    finalResults()

    cont = input("\nWould you like to continue? (Yes/No)\n--> ").lower()
    while cont != "yes" and cont != "no": cont = input("Please do not toy with me traveller, a simple yes or no should suffice.\n--> ").lower()
    if cont == "yes": print("\nThat's the spirit. Another round, traveller!")
    if cont == "no": print("\nThankyou for visiting, traveller!")
