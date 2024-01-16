#   ========================
#           YTPlayer
#   ========================
# Test
import threading
import time
import pandas as pd
from collections import deque
import YTPlayer.constants as constants
import pafy
import vlc
import random
import tools
import YTPlayer.ytPlayerController as ytPlayerController
import Helper.helper as helper



def getNextMusic():
    data = pd.read_excel(constants.queueMusicListFile, header=0, index_col=None)[constants.musicList_column_link]
    nextMusic = ""
    if data.empty == False:
        musicList = data.values.tolist()
        nextMusic = deque(musicList).popleft()

    return nextMusic

def dequeueMusic():
    try:
        data = pd.read_excel(constants.queueMusicListFile, header=0, index_col=None)
        nextMusic = []
        if data.empty == False:
            queueYouTubeMusicList = data[constants.queueMusicListColumns].values.tolist()
            dequeMusic = deque(queueYouTubeMusicList)
            nextMusic = dequeMusic.popleft()
            data = pd.DataFrame(list(dequeMusic), columns=constants.queueMusicListColumns)
            data.to_excel(constants.queueMusicListFile)
    except:
        pass

    return nextMusic

def getPlayingMusic():
    playingMusic = pd.read_excel(constants.queueMusicListFile, header=0, index_col=None)[constants.musicList_column_title][0]

    if len(playingMusic) > 40:
        playingMusic = playingMusic[0:40] + "..."

    return playingMusic

def getVolume():
    volume = 0
    with open(constants.volumeFile) as f:
            volume = int(f.readline())
            if volume < 0:
                volume = 0
            elif volume > 100:
                volume = 50


    return volume

def setVolume(volume):
    with open(constants.volumeFile, 'w') as f:
        f.write(volume)

def displayYTPlayerAlert(detail):
    print("\n[YTPlayer] - " + detail)

engine1UserInput = ""
isBegin = True
def engine1():
    global engine1UserInput
    global isBegin
    isDisplayedNoMoreMusic = True

    while isBegin:
        if (engine1UserInput == ["start"] or "play" in engine1UserInput or "p" in engine1UserInput):
            isBegin = False
            break
        time.sleep(1)

    while True:
        currentMusic = getNextMusic()       
        if (currentMusic != ""):
            try:
                isDisplayedNoMoreMusic = False
                is_opening = False
                is_playing = False

                video = pafy.new(currentMusic)
                best = video.getbestaudio()
                play_url = best.url

                instance = vlc.Instance("--no-xlib", "--quiet")
                player = instance.media_player_new()
                media = instance.media_new(play_url)
                media.get_mrl()
                player.set_media(media)
                player.play()
                
                player.audio_set_volume(getVolume())

                good_states = [
                    "State.Playing", 
                    "State.NothingSpecial", 
                    "State.Opening"
                ]

                displayYTPlayerAlert("Playing: " + getPlayingMusic())
                while str(player.get_state()) in good_states:
                    if (len(engine1UserInput)) > 0:
                        if engine1UserInput[0] == "skip":
                            displayYTPlayerAlert("Skipped")
                            player.set_pause(1)

                        elif engine1UserInput[0] == "pause":
                            displayYTPlayerAlert("Paused")
                            player.set_pause(1)
                            while engine1UserInput[0] != "unpause" and engine1UserInput[0] != "start":
                                time.sleep(1)
                            displayYTPlayerAlert("Unpaused")
                            player.set_pause(0)      
                            time.sleep(0.5)

                        elif "v" == engine1UserInput[0]:
                            try:
                                volume = int(engine1UserInput[1])
                                if volume >= 0 and volume <= 100:
                                    player.audio_set_volume(volume)
                                    setVolume(str(volume))
                            except:
                                pass
                        engine1UserInput = ""

                    if str(player.get_state()) == "State.Opening" and is_opening is False:
                        is_opening = True

                    if str(player.get_state()) == "State.Playing" and is_playing is False:
                        is_playing = True

                    time.sleep(0.5)
                player.stop()
                dequeueMusic()

            except:
                displayYTPlayerAlert("Unable to play this music")
                time.sleep(1)
                dequeueMusic()

        else:
            if (isDisplayedNoMoreMusic == False):
                displayYTPlayerAlert("No more music")
                isDisplayedNoMoreMusic = True
        time.sleep(0.5)

threading.Thread(target=engine1, daemon=True).start()

tools.displayTitle()
while True:
    userInput = input(":")
    if (userInput != "") :
        userInput = userInput.split()
        userInput[0] = helper.correctTypo(userInput[0]) # Comment this line to turn off typo helper
        
        ytPlayerController.commandList(userInput)
        helper.commandList(userInput)

        engine1UserInput = userInput
        
