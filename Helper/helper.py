import os
import difflib
import tools

def commandList(userInput):

    match str(userInput[0]).lower():
        case "cls":
            os.system('cls')
            tools.displayTitle()
        case "help":
            showCommandList()
        
def showCommandList():
    with open("Helper/commandList.txt") as f:
        commandList = f.readlines()
        print()
        print("".join(commandList))

def correctTypo(keyword: str):   
    f = open("Helper/commands.txt")
    commands = f.readline()
    commands = commands.lower().split()
    exactWords = difflib.get_close_matches(keyword.lower(), commands, n=1, cutoff=0.7)

    if len(exactWords)>0:
        if keyword.lower() != exactWords[0].lower():
            print("[Helper] - Corrected " + keyword + " -> " + exactWords[0])
        return exactWords[0]
    else: 
        return keyword

    
