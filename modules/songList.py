import urllib.request
import re
from pytube import YouTube
import moviepy.editor as mp
import os

#Create a list of downloaded music
trackList = []
def lstIncrement(yurl):
    global trackList
    trackList.append(yurl)
def updateLst():
    tracklist=os.listdir('./music/db/')
    for i in range(len(trackList)):
        trackList[i] = trackList[i].replace(".dat", "")
        print("Updated!!")
        
#A Class to Handle the Music Files Details
class tracks:
    def __init__(self, name, pub, year, yurl, coverart = '.\imgs\coverart.jpg'):
        self.name = name
        self.pub = pub
        self.year = year
        self.yurl = yurl
        self.coverart = coverart
    
    #Saving the Details of the Downloaded Track to a File to be read later.
    def save(self):
        try:
            with open('./music/db/{}.dat'.format(trackList[len(trackList)-1]), 'w') as mT:
                mT.write(str(self.name)+"|")
                mT.write(str(self.pub)+"|")
                mT.write(str(self.year)+"|")
                mT.write(str(self.yurl)+"|")
                mT.write(str(self.coverart))
        except Exception as e:
            print(e)
        else:
            print('Done')
    
    #Displays the Progress of the Downloading Track
    def progress_function(stream, chunk, bytes_remaining):
        if (((1-bytes_remaining/stream.filesize)*100) % 0.1) == 0:
            print(round((1-bytes_remaining/stream.filesize)*100, 3), '% \done...')

#Provides the List of Video IDs of Youtube Search Results
def urlProvider(track):
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query={}".format(track))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return video_ids

#Downloads the Required Music Track
def download(track):
    video_ids = urlProvider(track)
    url = 'www.youtube.com/watch?v={}'.format(video_ids[0])
    try:
        ytVid = YouTube(url, on_progress_callback=tracks.progress_function)
        duration = str(str(int((ytVid.length / 60))) + ' minutes ' + str(int((ytVid.length % 60))) +' seconds')
        print(duration)
        if (ytVid.length/60) < 10 :
            ytVid.prefetch()
            Streams = ytVid.streams.filter(only_audio=True).first()
            Streams.download('./music/.music-cache')
            clip = mp.AudioFileClip('./music/.music-cache/{}.mp4'.format(ytVid.title))
            clip.write_audiofile('./music/.music-cache/{}.mp3'.format(ytVid.title)) 
            os.remove('./music/.music-cache/{}.mp4'.format(ytVid.title))
            track1 = tracks(ytVid.title, ytVid.author, ytVid.publish_date, video_ids[0])
            lstIncrement(video_ids[0])
            track1.save()
        else: 
            return 2
    except Exception as e:
        print(e)
        return 3
    else:
        return 4

#Searches for Required Music Track in the Already Downloaded Tracks
def musicSearch(track):
    video_ids = urlProvider(track)
    url = video_ids[0]
    print(url)
    print(trackList)
    for i in range(len(trackList)):
        if url == trackList:
            return 1
    return 0

#Returns the search term for Youtube Search
def inputSearch(term):
    try:
        term = term.lower().split(' ')
        track = ''
        for i in term:
            if term.index(i) < (len(term) - 1):
                track += str(i)+'+'
            else:
                track += str(i)
    except Exception as e:
        print(e)
        return '0'
    else:
        return track