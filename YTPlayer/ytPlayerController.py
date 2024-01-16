
import os
from YTPlayer.search import search
from PyInquirer import prompt
import pandas as pd
import YTPlayer.constants as constants
import random
import zhconv
from colorama import Fore, Style

def commandList(userInput):
    match str(userInput[0]).lower():
        case "start":
            if len(getMusicQueueList()) == 0:
                displayYTPlayerAlert("No Music in Queue List")
            else:
                displayYTPlayerAlert("Started")

        case "exit":
            displayYTPlayerAlert("Exited")
            commandExit()

        case "play" | "p":
            if len(userInput) > 1:
                musicName = " ".join(userInput[1:len(userInput)])
                searchAndPlayMusic(musicName)
        
        case "showqueuelist" | "sql":
            showQueueList()

        case "showmusiclist" | "sml":
            showMusicList(userInput)
        
        case "purge":
            clearQueueList()
            displayYTPlayerAlert("QueueList Cleared")

        case "v" | "volume":
            if (len(userInput) > 1):
                displayYTPlayerAlert("Volume: " + userInput[1] if str(userInput[1]).isdigit() else getVolume())
            else:
                displayYTPlayerAlert("Volume: " + getVolume())

        case "music" | "m":
            displayYTPlayerAlert("Current Music: " + getPlayingMusic() if getPlayingMusic() != "" else "No music")
        
        case "randomqueuemusic" | "random" | "rdm":
            randomQueueMusic(userInput)

        case "randomplay" | "rp":
            randomPlayMusic(userInput)

        case "save" | "sv":
            if len(userInput) > 1:
                saveYoutubeMusic(userInput)

        case "remove" | "rm":
            removeYoutubeMusic(userInput)

        case "repeat":
            if (len(userInput) >= 3 and str(userInput[len(userInput)-1]).isdigit()):
                repeatNum = userInput[len(userInput)-1]
                musicName = ' '.join(userInput[1:len(userInput)-1])
                searchAndPlayMusic(musicName, int(repeatNum))
            else:
                displayYTPlayerAlert("Invalid input")

def searchAndPlayMusic(musicName, repeatNum=1):
    search_results = search(musicName)
    choice = list_search_results(search_results)
    for i in range(repeatNum):
        queueMusic(choice)
        i += 1
        if (i >= repeatNum):
            break

def startYTMusicPlayer():
    displayYTPlayerAlert("Started")

def showQueueList():
    displayTitle("YT Queue List")
    displayMusicList(getMusicQueueList(), 20)

def showMusicList(userInput):
    displayTitle("YT Music List")

    music_list = getMusicList()

    filtered_music_list = []

    if len(userInput) > 1:
        for music in music_list:
            musicName = " ".join(userInput[1:len(userInput)])
            if hantToHans(str(musicName).lower().replace(" ", "")) in hantToHans(str(music['name']).lower().replace(" ", "")):
                filtered_music_list.append(music)

    else:
        filtered_music_list = music_list

    if len(filtered_music_list)>0:
        questions = [
            {
                'type': 'list',
                'name': 'search',
                'message': 'Selected :',
                'choices': filtered_music_list,
            },
        ]

        answer = prompt(questions)
        print()
        fullAnswer={}
        
        try:
            for m in music_list:
                if answer['search'] == m['value']:
                    fullAnswer = {constants.musicList_column_title: m['name'], constants.musicList_column_link:m['value']}
        except:
            pass

        queueMusic(fullAnswer)
    
    else:
        print("-- No Music --")

def getPlayingMusic():
    musicList = pd.read_excel(constants.queueMusicListFile, header=0, index_col=None)[constants.musicList_column_title]
    playingMusic = musicList[0] if len(musicList) > 0 else ""

    if len(playingMusic) > 40:
        playingMusic = playingMusic[0:40] + "..."

    return playingMusic

def clearQueueList():
    df = pd.read_excel(constants.queueMusicListFile, header=0, index_col=None).values.tolist()
    if (len(df) > 0):
        pd.DataFrame([[df[0][1],df[0][2]]], columns=constants.queueMusicListColumns).to_excel(constants.queueMusicListFile)

def randomQueueMusic(userInput):
    df = pd.read_excel(constants.musicListFile)[constants.musicListColumns]
    musicList = df.values.tolist()

    if (len(userInput) > 1):
        musicNum = int(userInput[1] if str(userInput[1]).isdigit() else len(musicList))
        if musicNum > len(musicList):
            musicNum = len(musicList)

    else:
        musicNum = len(musicList)
    
    randomMusicList = random.sample(musicList, musicNum)
    pd.DataFrame(randomMusicList, columns=constants.queueMusicListColumns).to_excel(constants.queueMusicListFile)
    displayYTPlayerAlert("Random queue music Done")

def randomPlayMusic(userInput):
    clearQueueList()
    displayYTPlayerAlert("QueueList Cleared")
    randomQueueMusic(userInput)

def saveYoutubeMusic(music):
    music = " ".join(music[1:len(music)])

    search_result = search(music)
    choice = list_search_results(search_result)

    if choice:
        data = pd.read_excel(constants.musicListFile, header=0, index_col=None)[constants.queueMusicListColumns].values.tolist()

        linkExist = False

        for m in data:
            if m[1] == choice['value']:
                linkExist = True

        if linkExist == False:
            data.append([choice[constants.musicList_column_title], choice[constants.musicList_column_link]])
            pd.DataFrame(data, columns=constants.queueMusicListColumns).to_excel(constants.musicListFile)
            displayYTPlayerAlert(choice['name'] + " saved")
        else:
            print("This Music Already Exist in YT Music List.")

def removeYoutubeMusic(userInput):
    music_list = getMusicList()

    filtered_music_list = []

    if len(userInput) > 1:
        for music in music_list:
            musicName = userInput[1]
            if hantToHans(str(musicName).lower().replace(" ", "")) in hantToHans(str(music['name']).lower().replace(" ", "")):
                filtered_music_list.append(music)

    else:
        filtered_music_list = music_list

    displayTitle("YT Music List")
    if len(filtered_music_list) > 0:
        questions = [
            {
                'type': 'list',
                'name': 'search',
                'message': 'Selected :',
                'choices': filtered_music_list,
            },
        ]

        answer = prompt(questions)
        print()

        # Remove music from list
        new_music_list = music_list
        try:
            i=0
            for m in music_list:

                if answer['search'] == m[constants.musicList_column_link]:
                    new_music_list.pop(i)

                i+=1
        except:
            pass

        pd.DataFrame(new_music_list, columns=constants.musicListColumns).to_excel(constants.musicListFile)
    
    else:
        print("-- No Music --")

#   **************************
#       Tool
#   **************************
#   --------------------------
def getMusicList():
    data = pd.read_excel(constants.musicListFile, header=0, index_col=None)[constants.musicListColumns].values.tolist()

    music_list = []

    for i in data:
        item = {
            constants.musicList_column_title: i[0],
            constants.musicList_column_link: i[1]
        }

        music_list.append(item)

    return music_list

def getMusicQueueList():
    data = pd.read_excel(constants.queueMusicListFile, header=0, index_col=None)[constants.musicList_column_title].values.tolist()

    return data

def getVolume():
    volume = 0
    with open(constants.volumeFile) as f:
            volume = int(f.readline())
            if volume < 0:
                volume = 0
            elif volume > 100:
                volume = 100


    return str(volume)

def displayYTPlayerAlert(detail):
    print("[YTPlayer] - " + detail)
    print()

def list_search_results(search_list: list):
    questions = [
        {
            'type': 'list',
            'name': 'search',
            'message': 'Search Results:',
            'choices': search_list,
        },
    ]

    answer = prompt(questions)
    print()

    fullAnswer = {}
    try:
        for m in search_list:
            if answer['search'] == m['value']:
                fullAnswer = {constants.musicList_column_title: m['name'], constants.musicList_column_link:m['value']}
    
    except:
        pass

    return fullAnswer

def queueMusicFileIsEmpty():
    df = pd.read_excel(constants.queueMusicListFile)

    return df.empty

def queueMusic(music):

    if music:
        musics = pd.read_excel(constants.queueMusicListFile,header=0,index_col=None)[constants.queueMusicListColumns].values.tolist()
        musics.append([music[constants.musicList_column_title], music[constants.musicList_column_link]])
        print("[Added] - " + music[constants.musicList_column_title])
        print()
        pd.DataFrame(musics, columns=constants.queueMusicListColumns).to_excel(constants.queueMusicListFile)

def commandExit():
    os.system("taskkill /F /PID %d"%(os.getpid()))

def doublebreakLine():
    print("=====================================")

def singleBreakLine():
    print("-------------------------------------")

def displayMusicList(musicList, max=0):
    i = 0

    if len(musicList) < 1:
        print("No Music")

    for music in musicList:
        i+=1
        sider = Fore.YELLOW + "[Playing] " if i == 1 else "          "

        print(sider + placeHolder(i) + "     " + (music if (len(music) <= 45) else music[0:45] + "..."))
        if (i == 1):
            print(Style.RESET_ALL, end="")

        if i >= max & max != 0:
            print("+" + str(len(musicList)-i) + " More")
            break

    print()
def placeHolder(num):

    max_space = 7
    length = len(str(num))
    space = ""
    
    if length < 8:
        for x in range(max_space-length):
            space += " "

    return str(num) + space

def displayTitle(titleName):
    print()
    doublebreakLine()
    print("     " + titleName)
    doublebreakLine()

def hantToHans(hant_str: str):
    return zhconv.convert(hant_str, 'zh-hans')