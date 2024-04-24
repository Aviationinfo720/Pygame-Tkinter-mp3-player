from tkinter import filedialog
from tkinter import *
import pygame
import os
 
root = Tk()
root.title('Music Player')
root.geometry("500x300")
 
pygame.mixer.init()
 
menubar = Menu(root)
root.config(menu=menubar)
 
songs = []
current_song = ""
paused = True
full_path = ""
selected_index = ""
 
def letter_replacer(sentence, old_word, new_word):
    words = sentence.split()
    new_sentence = ' '.join([new_word if word == old_word else word for word in words])
    return new_sentence
 
def load_music():
    global current_song, selected_index
    global full_path
    root.directory = filedialog.askdirectory()
 
    for song in os.listdir(root.directory):
        name, ext = os.path.splitext(song)
        if ext == '.mp3':
            songs.append(song)
 
    for song in songs:
        songlist.insert('end', song)
 
    
    songlist.bind('<<ListboxSelect>>', lambda event: select_music())
 
def select_music():
    global selected_item
    global selected_index
    global full_path
    selected_index = songlist.curselection()
    if selected_index:
        selected_item = songlist.get(selected_index[0])
        full_path = os.path.join(root.directory, selected_item)
        full_path = os.path.normpath(full_path)
 
 
def play_music():
    global current_song, paused
    global full_path
 
    cache = read_file(cache_file_path)
 
    if paused == False:
        if current_song == "" and full_path != "" or ".":
            print("Loading music file:", full_path)
            pygame.mixer.music.load(full_path)
            pygame.mixer.music.set_volume(0.7)
            pygame.mixer.music.play()
 
    else:
        pygame.mixer.music.unpause()
        paused = False
 
# Call play_music() when needed to play the music
 
def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True
 
def select_next_song():
    global songlist
    current_index = songlist.curselection()
    
    if current_index:
        next_index = current_index[0] + 1
        if next_index < songlist.size():
            songlist.select_clear(current_index)
            songlist.select_set(next_index)
            songlist.activate(next_index)
            songlist.see(next_index)
        else:
            # Reached the end of the list, wrap around to the first song
            songlist.select_clear(current_index)
            songlist.select_set(0)
            songlist.activate(0)
            songlist.see(0)
    select_music()
 
def select_previous_song():
    current_index = songlist.curselection()
    
    if current_index:
        prev_index = current_index[0] - 1
        if prev_index >= 0:
            songlist.select_clear(current_index)
            songlist.select_set(prev_index)
            songlist.activate(prev_index)
            songlist.see(prev_index)
        else:
            songlist.select_clear(current_index)
            songlist.select_set(songlist.size() - 1)
            songlist.activate(songlist.size() - 1)
            songlist.see(songlist.size() - 1)
    select_music()
 
organise_menu  = Menu(menubar, tearoff=False)
organise_menu.add_command(label='Select Folder', command=load_music)
menubar.add_cascade(label='Organise', menu=organise_menu)
 
songlist = Listbox(root, bg='black', fg='white', width=100, height=15)
songlist.pack()
 
play_btn_image = PhotoImage(file="") # Put the button image path here, this is for the play button
pause_btn_image = PhotoImage(file="") # Put the button image path here, this is for the pause button
next_btn_image = PhotoImage(file="") # Put the button image path here, this is for the next button
previous_btn_image = PhotoImage(file="") # Put the button image path here, this is for the  previous button
 
control_frame = Frame(root)
control_frame.pack()
 
play_btn = Button(control_frame, image=play_btn_image, borderwidth=0, command=play_music)
pause_btn = Button(control_frame, image=pause_btn_image, borderwidth=0, command=pause_music)
next_btn = Button(control_frame, image=next_btn_image, borderwidth=0, command=select_next_song)
previous_btn = Button(control_frame, image=previous_btn_image, borderwidth=0, command=select_previous_song)
 
previous_btn.grid(row=0, column=0, padx=7, pady=10)
pause_btn.grid(row=0, column=1, padx=7, pady=10)
play_btn.grid(row=0, column=2, padx=7, pady=10)
next_btn.grid(row=0, column=3, padx=7, pady=10)
 
 
root.mainloop()
