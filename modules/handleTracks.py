from modules.songList import download, inputSearch, musicSearch

#Handles the Music Track Search and Download
def onSearchSubmit(track):
    term = inputSearch(track)
    if term == '0':
        return 0
    else:
        if musicSearch(term) == 0:
            return download(term)
        else:
            return 1