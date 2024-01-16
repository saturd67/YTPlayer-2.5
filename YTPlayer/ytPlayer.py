import pafy
import vlc
import YTPlayer.constant as constant
import time
import pandas as pd

import os
os.add_dll_directory(os.getcwd())

def getVolume():
    volume = 0
    with open(constant.volumeFile) as f:
            volume = int(f.readline())
            if volume < 0:
                volume = 0
            elif volume > 100:
                volume = 50


    return volume

def setVolume(volume):
    with open(constant.volumeFile, 'w') as f:
        f.write(volume)

def play_song(userInput, url):
    print("play_song: " + str(userInput))
    is_opening = False
    is_playing = False

    global previousCommandTime
    previousCommandTime = ""
    video = pafy.new(url)
    best = video.getbestaudio()
    play_url = best.url

    instance = vlc.Instance()
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
    
    while str(player.get_state()) in good_states:

        if userInput == "skip":
            player.set_pause(1)

        elif userInput == "pause":
            player.set_pause(1)

            while userInput != "unpause":
                time.sleep(1)

            player.set_pause(0)      
            time.sleep(0.5)

        elif "setVolume" in userInput:
            userInput = userInput.split()

            try:
                volume = int(userInput[1])
                if volume >= 0 and volume <= 100:
                    player.audio_set_volume(volume)
                    setVolume(str(volume))

            except:
                pass


        if str(player.get_state()) == "State.Opening" and is_opening is False:
            is_opening = True        

        if str(player.get_state()) == "State.Playing" and is_playing is False:
            is_playing = True

        time.sleep(1)

    player.stop()

