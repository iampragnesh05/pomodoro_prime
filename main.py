import threading
import time
import tkinter as tk
import winsound
from idlelib.configdialog import font_sample_text

from PIL import Image, ImageTk
from PIL.ImageOps import expand
from PIL.ImagePalette import random
from pandas.plotting import andrews_curves
from quotes import bhagavad_gita_quotes
import  random
import pygame

pygame.mixer.init()

# ---------------------------- COLOR PALETTES ------------------------------- #
LIGHT_THEME = {
    "background": "#f7f5dd",
    "text": "#000000",
    "button_bg": "#9bdeac",
    "button_fg": "#ffffff",
    "quote_fg": "#e7305b"
}

DARK_THEME = {
    "background": "#2e2e2e",
    "text": "#ffffff",
    "button_bg": "#4e4e4e",
    "button_fg": "#ffffff",
    "quote_fg": "#e2979c"
}

MUSIC_FILES = {
    "Rain": "rain.mp3",
    "Peaceful": "Peaceful.mp3",
    "Nature": "nature.mp3"
}
current_music = None

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
CYCLES = 4  # Number of cycles

# Convert minutes to seconds
WORK_SEC = WORK_MIN * 60
SHORT_BREAK_SEC = SHORT_BREAK_MIN * 60

# ---------------------------- TIMER RESET ------------------------------- # 

# ---------------------------- TIMER MECHANISM ------------------------------- # 
cycle_count = 0

def beep():
    winsound.Beep(1000, 500)

def update_quotes():
    quote = random.choice(list(bhagavad_gita_quotes.values()))
    quote_label.config(text = quote)

def quote_timer():
    while cycle_count < CYCLES:
        time.sleep(300)
        update_quotes()
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count, next_phase, next_count):
    minutes = count // 60
    seconds = count % 60
    canvas.itemconfig(text_id, text=f"{minutes:02d}:{seconds:02d}")

    if count > 0:
        window.after(1000, count_down, count - 1, next_phase, next_count)
    else:
        beep()
        if next_phase =="Break":
            start_work()
        elif next_phase == "Work":
            start_work()

def start_work():
    global cycle_count
    cycle_count += 1
    if cycle_count <= CYCLES:
        timer_label.config(text="WORK", fg=GREEN)
        update_quotes()
        threading.Thread(target=quote_timer, daemon=True).start()
        count_down(WORK_SEC, "Break", SHORT_BREAK_SEC)

def start_break():
    timer_label.config(text="BREAK", fg=PINK)
    count_down(SHORT_BREAK_SEC, "Work", WORK_SEC)





# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Pomodoro")
# Set the initial window size and minimum size
window.geometry("700x700")  # Initial size
window.minsize(400, 200)    # Minimum size

timer_label = tk.Label(window, text="TIMER", fg= GREEN, bg=YELLOW , font=(FONT_NAME, 36, "bold"))
timer_label.place(relx= 0.5, rely= 0.2, anchor= tk.CENTER)




window.config(bg=YELLOW)

image_path = "tomato.png"
image = Image.open(image_path)
photo = ImageTk.PhotoImage(image)

# Create a canvas to display the image and text
canvas = tk.Canvas(window, width=photo.width(), height=photo.height(), bg=YELLOW, highlightthickness=0)
canvas.pack(expand = True)
canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
canvas.create_image(0, 0, anchor = tk.NW, image = photo)
text_id = canvas.create_text(photo.width() // 2, photo.height() // 2 , text = "00:00" , fill="white", font = ({FONT_NAME}, 24, "bold"))

canvas.image = photo



quote_label = tk.Label(window, text="", fg=GREEN, bg=YELLOW, wraplength=400, font=(FONT_NAME, 12, "bold"))
quote_label.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

def start_cycle():
    global cycle_count
    cycle_count = 0  # Reset cycle count on new start
    start_work()

def reset_timer():
    window.after_cancel(start_cycle)  # Cancel any running countdown
    canvas.itemconfig(text_id, text="25:00")
    timer_label.config(text="TIMER", fg=GREEN)



def create_rounded_button(text, command, x, y):
    button_canvas = tk.Canvas(window, width=80, height=40, bg=current_theme["button_bg"], highlightthickness=0)
    button_canvas.place(x=x, y=y)
    text_id = button_canvas.create_text(40, 20, text=text, fill=current_theme["button_fg"], font=(FONT_NAME, 10, "bold"))
    button_canvas.bind("<Button-1>", lambda event: command())
    return button_canvas



def switch_theme(theme):
    window.config(bg=theme["background"])
    timer_label.config(bg=theme["background"], fg=theme["text"])
    quote_label.config(bg=theme["background"], fg=theme["quote_fg"])
    canvas.config(bg=theme["background"])


def toggle_theme():
    global current_theme
    if current_theme == LIGHT_THEME:
        current_theme = DARK_THEME
    else:
        current_theme = LIGHT_THEME
    switch_theme(current_theme)

def play_music():
    selected_music = music_var.get()
    pygame.mixer.music.stop()  # Stop any currently playing music
    pygame.mixer.music.load(MUSIC_FILES[selected_music])  # Load new music file
    pygame.mixer.music.play(-1)  # Play selected music in a loop

# Initialize current theme
current_theme = LIGHT_THEME


reset_button = create_rounded_button("Reset", reset_timer, x=450, y=200)
start_button = create_rounded_button("Start", start_cycle, x=200, y=200)


theme_button = tk.Button(window, text="Toggle Theme", command=toggle_theme, bg=current_theme["button_bg"], fg=current_theme["button_fg"])
theme_button.place(x=10, y=20)  # Adjust the position as needed

# Frame for music selection with title
music_frame = tk.LabelFrame(window, text="Please choose preferred music", bg=YELLOW, fg="black", font=(FONT_NAME, 12, "bold"))
music_frame.place(relx=0.50, rely=0.80, anchor=tk.CENTER)

# Music selection radio buttons
music_var = tk.StringVar(value="Rain")
tk.Radiobutton(music_frame, text="Rain", variable=music_var, value="Rain", command=play_music, bg=YELLOW, fg="black").pack(anchor="w", padx=10, pady=5)
tk.Radiobutton(music_frame, text="Peaceful", variable=music_var, value="Peaceful", command=play_music, bg=YELLOW, fg="black").pack(anchor="w", padx=10, pady=5)
tk.Radiobutton(music_frame, text="Nature", variable=music_var, value="Nature", command=play_music, bg=YELLOW, fg="black").pack(anchor="w", padx=10, pady=5)
# Start the default music (Rain) on launch
play_music()

window.mainloop()