from tkinter import * #libery to create gui elements
from tkinter import ttk as ttk
from tkinter import filedialog #opens file explorer
from tkinter import messagebox
from pygame import mixer #allows media elements
from mutagen.mp3 import MP3 #tracks length of media element
import os #access to storage
import time
import pygame

""" Setting up Window Size"""
root = Tk()
root.title('Roberts MP3 Player')
root.geometry('400x400') 

"""Intiaize mixer"""
pygame.mixer.init() 


def play_time(): 

    """ 
    Function to get the length of the currently playing song
    Grabbing the elapsed time increasing it by seconds
    resetting the time when song is changed.
    """

    if stopped: 
        return

    current_time = mixer.music.get_pos() / 1000 
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time)) 
    song = playlist.get(ACTIVE) 
    song_mut = MP3(song) 
    global song_length 
    song_length = song_mut.info.length
   
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    current_time +=1 
    if int(music_slider.get()) == int(song_length):
        status_bar.config(text=f' {converted_song_length} : {converted_song_length} ')
    elif paused:
        pass
    elif int(music_slider.get()) == int(current_time):
    
        slider_position = int (song_length)
        music_slider.config(to=slider_position, value = int(music_slider.get())) 

    else: 
        slider_position = int(song_length)
        music_slider.config(to=slider_position, value=int(music_slider.get()))

        
        converted_current_time = time.strftime('%M:%S', time.gmtime(int(music_slider.get())))

		
        status_bar.config(text=f' {converted_current_time}  :  {converted_song_length}  ')
        next_time = int(music_slider.get()) + 1 
        music_slider.config(value=next_time)

    status_bar.after(1000, play_time)

""" Media Controls  """

def play(): 

    """
    Play the selected song from the list box.
    """
    try:
        music_slider.config(value=0)
        song = playlist.curselection()
        song = playlist.get(ACTIVE)
        global stopped
        stopped = False

        mixer.music.load(song) 
        mixer.music.play(loops=0) 
        play_time() 

    except:
        messagebox.showinfo("Error", "Add Songs to playlist")
        

def stop(): 
    """
    Stop function
    """
    global stopped
    stopped = True
    mixer.music.stop()
    playlist.selection_clear(ACTIVE)


def next_song():
    """
    Plays the next song by changing selecting the song next in line 
    to the current playing
    """
    try:
        music_slider.config(value=0)
        next_song = playlist.curselection()
        next_song = next_song[0]+1 
        song = playlist.get(next_song) 
        mixer.music.load(song)
        mixer.music.play(loops=0)

        playlist.selection_clear(0, END) 
        playlist.activate(next_song)
        playlist.selection_set(next_song, last=None)
    except:
        messagebox.showinfo("Selection Error", "No Next song")
    

def previous_song():
    """
    Plays the previous song by changing selecting the song previous in line 
    to the current playing
    """
    try:
        music_slider.config(value=0)
         
        next_song = playlist.curselection()
        
        next_song = next_song[0]-1  
   
        song = playlist.get(next_song)  
   
        mixer.music.load(song)
        mixer.music.play(loops=0)
   
        playlist.selection_clear(0, END)
  
        playlist.activate(next_song)
    
    
        playlist.selection_set(next_song, last=None)
    except:
        messagebox.showinfo("Selection Error", "No Previous song")
    
 
""" global paused varaible """
global paused
paused = False

def pause(is_paused):
    """ Pause function"""
    global paused
    paused = is_paused
    if paused:
        mixer.music.unpause()
        paused = False
    else:
        mixer.music.pause()
        paused = True

def slide(x):
	
	song = playlist.get(ACTIVE)


def add_song():
    """
    Adding one song to the playlist
    """
    song = filedialog.askopenfilename(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))
    playlist.insert(END, song)


def add_several_songs():
    """
    add several songs to playlist 
    """
    songs = filedialog.askopenfilenames(initialdir='audio/', title="Choose A Song", filetypes=(("mp3 Files", "*.mp3"), ))	

    for song in songs:
        if song.endswith(".mp3"):
       
            playlist.insert(END, song)


def delete_song():
    """
    Deletes a song from the playlist
    """
    playlist.delete(ANCHOR)
    mixer.stop()

def delete_all_songs():
    """
    Deletes all songs from the playlist
    """
    playlist.delete(0, END)
    mixer.stop()

"""    Setting up visual elements       """

"""icons"""
backbtn_image = PhotoImage(file='back.png')
playbtn_image = PhotoImage(file='play.png')
pausebtn_image = PhotoImage(file='pause.png')
stopbtn_image = PhotoImage(file='stop.png')
nextbtn_image = PhotoImage(file='next.png')

"""creating master frame"""
master_frame = Frame(root)
master_frame.pack(pady=20)

"""create controls frame"""
controls_frame = Frame(master_frame)
controls_frame.grid(row=1, column=0, pady=20)

"""creating playlist as listbox"""
playlist = Listbox(master_frame,bg ="black", fg="white",font=('arial',11),width=40)
playlist.grid(row=0, column=0)

""" Creating the buttons  """
playbtn=Button(controls_frame,image=playbtn_image,borderwidth=0,command=play)
playbtn.config(font=('arial',20),bg="grey",fg="white",padx=7,pady=7)
playbtn.grid(row=0,column=1)

pausebtn=Button(controls_frame,image=pausebtn_image,borderwidth=0,command=lambda: pause(paused))
pausebtn.config(font=('arial',20),bg="grey",fg="white",padx=7,pady=7)
pausebtn.grid(row=0,column=2)

stopbtn=Button(controls_frame,image=stopbtn_image,borderwidth=0,command=stop)
stopbtn.config(font=('arial',20),bg="grey",fg="white",padx=7,pady=7)
stopbtn.grid(row=0,column=4)

nextbtn=Button(controls_frame,image=nextbtn_image,borderwidth=0,command=next_song)
nextbtn.config(font=('arial',20),bg="grey",fg="white",padx=7,pady=7)
nextbtn.grid(row=0,column=3)

backbtn=Button(controls_frame,image=backbtn_image,borderwidth=0,command=previous_song)
backbtn.config(font=('arial',20),bg="grey",fg="grey",padx=7,pady=7)
backbtn.grid(row=0,column=0)

""" Creating menus and menu buttons  """

music_menu = Menu(root)
root.config(menu=music_menu)

""" button"""
add_song_menu = Menu(music_menu)
music_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song To Playlist", command=add_song)

"""Add Many Songs to playlist button"""
add_song_menu.add_command(label="Add Several Songs To Playlist", command=add_several_songs)

"""Create Delete Song Menu button"""
remove_song_menu = Menu(music_menu)
music_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Delete A Song From Playlist", command=delete_song)
remove_song_menu.add_command(label="Delete All Songs From Playlist", command=delete_all_songs)

"""Create Status Bar"""
status_bar = Label(root, text='', bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

music_slider = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
music_slider.grid(row=2, column=0, pady=10)

root.mainloop()










    








