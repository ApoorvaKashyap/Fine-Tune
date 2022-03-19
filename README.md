# Web Based MP3 Player

***Language: Python***

---

- [Web Based MP3 Player](#web-based-mp3-player)
  - [Web Based MP3 Player](#web-based-mp3-player-1)
    - [Functionalities](#functionalities)
    - [Libraries Used](#libraries-used)
  - [How to Use](#how-to-use)
    - [Prerequisites](#prerequisites)
    - [The Controls](#the-controls)
  - [Cantribution](#cantribution)
  - [License](#license)

---
## Web Based MP3 Player

The Music Player will be developed from scratch using Python. It will be web-based, i.e., it will have a  web server fropm where music will be downloaded and adde to the app's playlist. The player will search for a music track on demand and then play the music track if found. Otherwise, it downloads the track from the server.

Server: [Youtube](www.youtube.com)

### Functionalities

1. Play a track already downloaded through the app.
2. If the demanded track is unavailable, then download it from the server.
3. Have the Play/Pause, Forward Seek and Backward Seek Buttons.

### Libraries Used

1. OS - To work with directories and filesystems.
2. PyTube - To access songs from Youtube.
3. URLLib - To access the html codes of webpages.
4. Re - To find the matching expressions in the search results.
5. MoviePy - To convert the downloaded file into .mp3 format.
6. PyGame - To control the Music Playback.
7. PIL - To insert image into Tkinter Labels

---

## How to Use

To run the program, open the root folder of this bundle in the terminal and type the following command:
`python main.py`

### Prerequisites

1. Python 3 should be preinstalled and added to the path.

### The Controls

1. The Input Bar at the top takes the name of the track. The Search Button beside it launches the search function. If the track is already present, it says so, else tries to download the track.
2. The List at the right side contains a list of the already present tracks. Selecting the track and pressing the Play/Pause Button plays the track.
3. The Volume Slider is at the bottom of the screen. It needs to be set to a certain value when the first song is run.
4. The Forward Seek and Backward Seek button jump to the nearest multiple of 15th second in their respective directions. If the forward or the backward button is pressed twice in the starting or the ending 15 s of the song, then the song stops.

---
