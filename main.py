#Importing Required Libraries and Modules
import tkinter as tk
from tkinter.ttk import *
from PIL import Image, ImageTk
from modules.handleTracks import *
from tkinter import messagebox
import os
import pygame
from modules.songList import *

#Making a Basic Structure - Do NOT Change
root = tk.Tk()
root.title('TuneUp Music Player')
photo = tk.PhotoImage(file="imgs/icons/logo.png")
root.iconphoto(True, photo)

#Making the Main Window - Do NOT Change
win_width = 850
win_height = 480
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
start_x = int((screen_width/2) - (win_width/2))
start_y = int((screen_height/2) - (win_height/2))
root.geometry('{}x{}+{}+{}'.format(win_width, win_height, start_x, start_y))

#Intializing Song Attributes
songName='Name'
publisher='Publisher'
pubDate='Release Date'
yurl='Youtube ID'
duration='Duration'

#Initializing the Mixer
pygame.init()
pygame.mixer.init()
pygame.mixer.music.set_volume(float(25))
updateLst()


#Making the List of Available Songs
songlist = tk.Listbox(root, bg='#87847e', fg='#ffffff', width=40, height=25, selectbackground='red', selectforeground='yellow')
songlist.place(x=585, y=50)

path = "./music/.music-cache"
song = os.listdir(path)
for i in song:
  songlist.insert(tk.END, i)

track_duration = 0

'''Defining the functions of the music player'''
#Stop the Music
def stop():
  pygame.mixer.music.stop()
  songlist.selection_clear(tk.ACTIVE)

#Displays the Info of the Cureently Playing Song
def infoShow(trackName):
  global track_duration
  try:
    trackName=inputSearch(trackName)
    video_ids=urlProvider(trackName)
    url = video_ids[0]
    with open('./music/db/{}.dat'.format(url),'r') as yfile:
      line = str(yfile.read())
  except Exception as e:
    print(e)
  else:
    line = line.split('|')
    name_label.config(text='{}: {}'.format(songName, line[0]))
    pub_label.config(text='{}: {}'.format(publisher, line[1]))
    date_label.config(text='{}: {}'.format(pubDate, line[2]))
    yurl_label.config(text = '{}: {}'.format(yurl, line[3]))
    duration_label.config(text = '{}: {} s'.format(duration, line[4]))
    track_duration = int(line[4])

#Controls the Play/Pause Button
global paused
paused = False

song = None

#Tracks the current playing song and plays the new
#if the new is not equal to the old
def change_song(s):
  global song
  if song != s:
    path = f'./music/.music-cache/{s}'
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(loops = 0)
    infoShow(s.replace(".mp3", ""))
    song = s

def pause(is_paused):
  global started
  global paused
  paused = is_paused
  if paused:
    songName = songlist.get(tk.ACTIVE)
    change_song(songName)
    pygame.mixer.music.pause()
    pause_button.config(image = play_button_img)
    paused = False
  else:
    pygame.mixer.music.unpause()
    pause_button.config(image = pause_button_img)
    paused = True

#Changes the Volume of the Playing Track
def vol_change(var):
  x = int(var)
  lvar.set(x)
  if x>=70:
    v_img.config(image=vol_high)
  if 1<=x<70:
    v_img.config(image=vol_low)
  if x == 0:
    v_img.config(image = vol_mute)
  pygame.mixer.music.set_volume(float(x/100))

i = 1

def fseek():
  global track_duration, i
  if 15 * i < track_duration :
    pygame.mixer.music.set_pos(i * 15)
    i+=1
  else:
    stop()


def bseek():
  global track_duration, i
  if 15 * (i-1) >= 0 :
    i-=1
    pygame.mixer.music.set_pos(i * 15)
  else:
    stop()

def onSearch():
  result=onSearchSubmit(search_term.get())
  if result == 0:
    msg = "Please enter a valid search term."
    messagebox.showerror("Error",msg)
  elif result == 1:
    msg="The track is already present. Please select it from the Track List"
    messagebox.showinfo("Information",msg)
  elif result == 2:
    msg = "The track is too long to be downloaded."
    messagebox.showerror("Error",msg)
  elif result == 3:
    msg = "Couldn't download the track. Please try again later."
    messagebox.showerror("Error",msg)
  elif result == 4:
    msg = "The track has been downloaded successfully."
    messagebox.showinfo("Information",msg)
    refresh()

#Styles for the Labels
lbl_Styles=Style()
lbl_Styles.configure('W.TLabel', font = ('Times', 14, 'bold'), foreground = '#ffffff', background='#50544f')

#Making the Song Info Display
coverart = Image.open("./imgs/coverart/default.jpg")
ca_img = ImageTk.PhotoImage(coverart)
ca_label = tk.Label(image=ca_img)
ca_label.image = ca_img
ca_label.place(x=20, y= 50)
default='N/A'
np_label = tk.Label(root, text="Now Playing .....", font = ('Times', 14, 'italic'), foreground = '#ffffff', background='#50544f')
np_label.place(x=300, y=65)
name_label = tk.Label(root, text="{}: {}".format(songName,default), font = ('Times', 12), foreground = '#ffffff', background='#50544f')
name_label.place(x=300, y=95)
pub_label = tk.Label(root, text="{}: {}".format(publisher,default), font = ('Times', 12), foreground = '#ffffff', background='#50544f')
pub_label.place(x=300, y=125)
date_label = tk.Label(root, text="{}: {}".format(pubDate,default), font = ('Times', 12), foreground = '#ffffff', background='#50544f')
date_label.place(x=300, y=155)
yurl_label = tk.Label(root, text="{}: {}".format(yurl,default), font = ('Times', 12), foreground = '#ffffff', background='#50544f')
yurl_label.place(x=300, y=185)
duration_label = tk.Label(root, text="{}: {}".format(duration,default), font = ('Times', 12), foreground = '#ffffff', background='#50544f')
duration_label.place(x=300, y=215)

#Making the Search Bar
search_term = tk.StringVar()
search_bar = tk.Entry(root, textvariable=search_term, font=('Times', 10, 'normal'), bg='#87847e', fg='#ffffff')
search_bar.place(x=17, y=5, height=30, width=700)
searchButton = tk.Button(root, text='Search..', width=100, command=onSearch)
searchButton.place(x=725, y=5, height=30, width=100)

#Making the controls images
play_button_img = tk.PhotoImage(file='./imgs/icons/play.png')
pause_button_img = tk.PhotoImage(file='./imgs/icons/pause.png')
stop_button_img = tk.PhotoImage(file='./imgs/icons/stop.png')
fskip_button_img = tk.PhotoImage(file='./imgs/icons/skip-forward.png')
bskip_button_img = tk.PhotoImage(file='./imgs/icons/skip-back.png')
fseek_button_img = tk.PhotoImage(file='./imgs/icons/fast-forward.png')
bseek_button_img = tk.PhotoImage(file='./imgs/icons/rewind.png')
vol_high = Image.open("./imgs/icons/high-vol.png")
vol_high = ImageTk.PhotoImage(vol_high)
vol_low = Image.open("./imgs/icons/low-vol.png")
vol_low = ImageTk.PhotoImage(vol_low)
vol_mute = Image.open("./imgs/icons/mute.png")
vol_mute = ImageTk.PhotoImage(vol_mute)

#Making the Buttons
pause_button=tk.Button(root, image=play_button_img, borderwidth=0,bg='#50544f', relief=tk.GROOVE, command =lambda: pause(paused))
pause_button.place(x = 215, y = 315)
bseek=tk.Button(root, image=bseek_button_img, borderwidth=0,bg='#50544f', relief=tk.GROOVE,  command=bseek)
bseek.place(x = 40, y = 325)
fseek=tk.Button(root, image=fseek_button_img, borderwidth=0,bg='#50544f', relief=tk.GROOVE,  command=fseek)
fseek.place(x = 380, y = 325)
v_img = tk.Label(image=vol_mute, bg='#50544f')
v_img.image = v_img
v_img.place(x=17, y=428)
volume_scale = tk.Scale(root,from_=0, to=100, orient = tk.HORIZONTAL, command = vol_change, bg="#50544f")
volume_scale.place(x = 60, y =425, width=500 )
lvar = tk.IntVar()
volume_scale.set(25)

#Adding Quit Button and Refresh Button using right click 
def refresh():
  path = "./music/.music-cache"
  song = os.listdir(path)
  songlist.delete(0, tk.END)
  for i in song:
    songlist.insert(tk.END, i)
  updateLst()
  
rMenu = tk.Menu(root, tearoff = 0)

def showMenu(e):
    rMenu.post(e.x_root, e.y_root)

rMenu.add_command(label = 'Refresh', command = refresh)
rMenu.add_separator() 
rMenu.add_command(label = 'Quit', command = root.quit)
root.bind("<Button-3>", showMenu)

#Configuring the GUI
root.resizable(0, 0)
root.configure(background="#50544f")

#Running the GUI
root.mainloop()
