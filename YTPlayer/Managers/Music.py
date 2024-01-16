import pandas as pd
import os
from PyInquirer import prompt
from zhconv import convert

from dotenv import load_dotenv
from googleapiclient.discovery import build

class constants:
    queueMusicListFile = "YTPlayer/youtubeQueueMusicList.xlsx"
    musicListFile = "YTPlayer/youtubeMusicList.xlsx"
    controllerCommandFile = 'YTPlayer/youtubeMusicControllerCommand.txt'
    musicListColumnTitle = "name"
    musicListColumnLink = "value"
    queueMusicListColumns = [musicListColumnTitle, musicListColumnLink]
    musicListColumns = [musicListColumnTitle, musicListColumnLink]
    volumeFile = "YTPlayer/volume.txt"


class MusicManager:
    playingMusic = ""

    # Redo the showMusicList, saveMusic, removeMusic

    def showMusicList(self, music):
        musicList = self.getMusicList()
        filteredMusicList = []
        if (len(filteredMusicList) > 0):
            if (music is not None and music != ""):
                for m in musicList:
                    if self.hantToHans(str(music).lower().replace(" ", "")) in self.hantToHans(str(m['name']).lower().replace(" ", "")):
                        filteredMusicList.append(music)
            else:
                filteredMusicList = musicList
            
            selectedMusic = self.selectMusic(filteredMusicList)
            self.queueMusic(selectedMusic)
        else:
            print("-- No Music --")

    
    def saveMusic(self, music):
        resultList = self.searchYTMusic(music)
        selectedMusic = self.selectMusic(resultList)
        if selectedMusic is not None:
            if os.path.exists(constants.musicListFile) == False:
                return constants.musicListFile + " does not exists."
            
            df = pd.read_excel(constants.musicListFile, header=0)
            
            isLinkExists = False
            for index, row in df.iterrows():
                if row['value'] == selectedMusic['value']:
                    isLinkExists == True
                    break
            
            if isLinkExists == False:
                musicList = df.values.tolist()
                musicList.append([selectedMusic[constants.musicListColumnTitle], selectedMusic[constants.musicListColumnLink]])
                pd.DataFrame(musicList, columns=[constants.musicListColumnTitle, constants.musicListColumnLink]).to_excel(constants.musicListFile, index=False)
                self.alert("saved")

            else:
                print("This Music Already Exist in Music List")

    
    def removeMusic(self, music=None):
        musicList = self.getMusicList(music)
        print(musicList)
        selectedMusic = self.selectMusic(musicList)
        if selectedMusic is not None:
            i = 0
            for m in musicList:
                if selectedMusic['value'] == m[constants.musicListColumnLink]:
                    musicList.pop(i)
                i += 1
            pd.DataFrame(musicList, columns=constants.musicListColumns).to_excel(constants.musicListFile, index=False) 


    def getVolume(self):
        volume = 0
        with open(constants.volumeFile) as f:
            volume = int(f.readline())
            if volume < 0:
                volume = 0
            elif volume > 100:
                volume = 50
        return volume


    def setVolume(self, volume):
        volume = str(volume)
        with open(constants.volumeFile, 'w') as f:
            f.write(volume)


    def getMusicList(self, music=None):
        musicDF = pd.read_excel(constants.musicListFile, header=0, index_col=None)
        filteredMusicList = []
        if (music is not None and music != ""):
            for index, row in musicDF.iterrows():
                if self.hantToHans(str(music).lower().replace(" ", "")) in self.hantToHans(str(row['name']).lower().replace(" ", "")):
                    filteredMusicList.append({'name': row['name'], 'value': row['value']})
        else:
            for index, row in musicDF.iterrows():
                filteredMusicList.append({'name': row['name'], 'value': row['value']})
            filteredMusicList = musicDF.values.tolist()
        return filteredMusicList
    

    def selectMusic(self, searchList: list):
        questions = [
            {
                'type': 'list',
                'name': 'value',
                'message': 'Search Results:',
                'choices': searchList
            }
        ]
        answer = prompt(questions)
        print()

        try:
            for x in searchList:
                if answer['value'] == x['value']:
                    answer = {constants.musicListColumnTitle: x['name'], constants.musicListColumnLink: x['value']}
        except:
            return None

        return answer       


    def getPlayingMusic(self):
        pass


    def getNextMusic(self):
        pass


    def queueMusic(self):
        pass
    

    def dequeueMusic(self):
        pass


    def getQueueList(self):
        return pd.read_excel(constants.queueMusicListFile, header=0, index_col=None)[constants.musicListColumnLink].values.tolist()
    

    def searchYTMusic(self, keywords):
        youtube = build('youtube', 'v3', developerKey='AIzaSyDdBvbYp4KaKXMK24Cq5ceRqLxMFvRUnuw')
        youtubeRequest = youtube.search().list(
            part = 'id,snippet',
            q = keywords,
            maxResults = 20,
            type = 'video'
        )

        youtubeResponse = youtubeRequest.execute()
        searchResults = []

        for video in youtubeResponse["items"]:
            searchResults.append({'name': video["snippet"]["title"], 'value': f'https://www.youtube.com/watch?v={video["id"]["videoId"]}'})
        
        return searchResults
    

    def hantToHans(self, hantStr: str):
        return convert(hantStr, 'zh-hans')

    
    def alert(self, message):
        print("[YTPlayer] - " + message)
        print()