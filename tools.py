import random

def displayTitle():    
    with open("Titles/Title" + str(random.randint(0,5)) + ".txt", "r", encoding="utf8") as f:
        title = f.readlines()
        print()
        print("".join(title))
        print("=========================================================================================================\n")