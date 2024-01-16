from YTPlayer.Managers.Music import MusicManager

musicManager = MusicManager()

musicManager.removeMusic('JayChou')
# musicManager.removeMusic('JayChou')
print(musicManager.getMusicList())
