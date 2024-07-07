import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import pyttsx3
import os
import threading

root = Tk()
root.title("Text to Speech")
root.geometry("900x550+200+200")
root.resizable(False, False)
root.configure(bg="#305065")

engine = pyttsx3.init()

is_playing = False
paused = False
current_thread = None

def speaknow():
    global is_playing, paused, current_thread
    is_playing = True
    paused = False
    text = test_area.get(1.0, END).strip()
    language = language_combobox.get()
    gender = gender_combobox.get()
    speed = speed_combobox.get()
    voices = engine.getProperty('voices')
    
    def setvoice():
        selected_voice = None
        for voice in voices:
            if language.lower() in voice.name.lower():
                if gender == 'Male' and 'male' in voice.name.lower():
                    selected_voice = voice
                    break
                elif gender == 'Female' and 'female' in voice.name.lower():
                    selected_voice = voice
                    break
        
        if not selected_voice:
            # Fallback to default language's voice if no exact match found
            for voice in voices:
                if language.lower() in voice.name.lower():
                    selected_voice = voice
                    break
        
        if selected_voice:
            engine.setProperty('voice', selected_voice.id)
        
        engine.say(text)
        engine.runAndWait()
    
    if text:
        if speed == "Fast":
            engine.setProperty('rate', 250)
        elif speed == 'Normal':
            engine.setProperty('rate', 150)
        else:
            engine.setProperty('rate', 100)
        
        current_thread = threading.Thread(target=setvoice)
        current_thread.start()

def download():
    text = test_area.get(1.0, END).strip()
    language = language_combobox.get()
    gender = gender_combobox.get()
    speed = speed_combobox.get()
    voices = engine.getProperty('voices')
    
    def setvoice():
        selected_voice = None
        for voice in voices:
            if language.lower() in voice.name.lower():
                if gender == 'Male' and 'male' in voice.name.lower():
                    selected_voice = voice
                    break
                elif gender == 'Female' and 'female' in voice.name.lower():
                    selected_voice = voice
                    break
        
        if not selected_voice:
            # Fallback to default language's voice if no exact match found
            for voice in voices:
                if language.lower() in voice.name.lower():
                    selected_voice = voice
                    break
        
        if selected_voice:
            engine.setProperty('voice', selected_voice.id)
        
        path = filedialog.askdirectory()
        if path:
            os.chdir(path)
            engine.save_to_file(text, 'text.mp3')
            engine.runAndWait()
    
    if text:
        if speed == "Fast":
            engine.setProperty('rate', 250)
        elif speed == 'Normal':
            engine.setProperty('rate', 150)
        else:
            engine.setProperty('rate', 100)
        
        setvoice()

def pause_resume():
    global paused, is_playing
    paused = not paused
    if paused:
        engine.stop()
        pause_button.config(text="Resume")
    else:
        pause_button.config(text="Pause")
        speaknow()

def stop():
    global is_playing
    is_playing = False
    engine.stop()
    pause_button.config(text="Pause")

# icon
image_icon = PhotoImage(file="speak.png")
root.iconphoto(False, image_icon)

# top Frame
Top_frame = Frame(root, bg="white", width=900, height=100)
Top_frame.place(x=0, y=0)

Logo = PhotoImage(file="speaker logo.png")
Label(Top_frame, image=Logo, bg="white").place(x=10, y=5)

Label(Top_frame, text="Text to Speech", font="Times 20 bold", bg="white", fg="black").place(x=100, y=30)

# text area
test_area = Text(root, font="Robote 20", bg="white", relief=GROOVE, wrap=WORD)
test_area.place(x=10, y=150, height=250, width=500)

Label(root, text="VOICE", font="arial 15 bold", bg="#305065", fg="white").place(x=580, y=200)
Label(root, text="SPEED", font="arial 15 bold", bg="#305065", fg="white").place(x=760, y=200)
gender_combobox = Combobox(root, values=['Male', 'Female'], font="arial 14", state='readonly', width=10)
gender_combobox.place(x=550, y=230)
gender_combobox.set('Male')

speed_combobox = Combobox(root, values=['Fast', 'Normal', 'Slow'], font="arial 14", state='readonly', width=10)
speed_combobox.place(x=730, y=230)
speed_combobox.set('Normal')

imageicon = PhotoImage(file="Speak.png")
btn = Button(root, text="Speak", compound=LEFT, image=imageicon, width=130, font="arial 14 bold", command=speaknow)
btn.place(x=550, y=280)

imageicon2 = PhotoImage(file="download.png")
save = Button(root, text="Save", compound=LEFT, image=imageicon2, width=130, bg="#39c790", font="arial 14 bold", command=download)
save.place(x=730, y=280)

Label(root, text="LANGUAGE", font="arial 15 bold", bg="#305065", fg="white").place(x=580, y=120)
language_combobox = Combobox(root, values=['English', 'Spanish', 'French', 'German', 'Italian'], font="arial 14", state='readonly', width=10)
language_combobox.place(x=550, y=150)
language_combobox.set('English')

# Add playback control buttons
play_button = Button(root, text="Play", width=10, font="arial 14 bold", command=speaknow)
play_button.place(x=550, y=370)

pause_button = Button(root, text="Pause", width=10, font="arial 14 bold", command=pause_resume)
pause_button.place(x=680, y=370)

stop_button = Button(root, text="Stop", width=10, font="arial 14 bold", command=stop)
stop_button.place(x=810, y=370)

root.mainloop()
