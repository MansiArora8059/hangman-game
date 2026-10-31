import tkinter as tk
import winsound
from tkinter import messagebox
from tkinter import simpledialog
from database import get_random_word, get_high_score, save_high_score

current_level = "easy"
levels = ["easy", "medium", "difficult"]
word = get_random_word(current_level).upper()
print("Game word:", word)
word_letter = []

for letter in word:
    if letter not in word_letter:
        word_letter.append(letter)

used_letters = []
lives = 5
game_over = False
sound_on = True
score = 0
player_name = "Player"


root = tk.Tk()
root.title("Hangman Game")
player_name = tk.simpledialog.askstring(
    "Player Name",
    "Enter your name:"
)

if not player_name:
    player_name = "Player"
high_score = get_high_score(player_name)
#frame set
# Main window layout
root.geometry("1200x750")
root.minsize(900, 600)

root.configure(bg="#FFE4EF")

# Three columns
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=4)
root.grid_columnconfigure(2, weight=1)

# Left panel - Player statistics
header_frame = tk.Frame(
    root,
    bg="#FFD6E5",
    bd=0,
    highlightthickness=2,
    highlightbackground="#F5A9C5"
)
header_frame.grid(
    row=0, column=0,
    sticky="nsew",
    padx=12, pady=15
)

# Center panel - Hangman game
game_frame = tk.Frame(root, bg="#FFE4EF")
game_frame.grid(
    row=0, column=1,
    sticky="nsew",
    padx=12, pady=15
)

# Right panel - Game controls
control_frame = tk.Frame(root, bg="#FFD6E5")
control_frame.grid(
    row=0, column=2,
    sticky="nsew",
    padx=12, pady=15
)


header_frame.grid_columnconfigure(0, weight=1)
game_frame.grid_columnconfigure(0, weight=1)
control_frame.grid_columnconfigure(0, weight=1)
#canvas setting
canvas = tk.Canvas(
    game_frame,
    bg= "#FFE4EF",
    highlightthickness=0
)
canvas.pack(fill="both", expand=True, padx=20, pady=10)

# Canvas drawing

vertical_pole = canvas.create_line(
    50, 50, 50, 250, width=4
)

horizontal_pole = canvas.create_line(
    50, 50, 200, 50, width=4
)

rope = canvas.create_line(
    200, 50, 200, 90, width=3
)

head = canvas.create_oval(
    180, 90, 220, 130, width=3
)

body = canvas.create_line(
    200, 130, 200, 190, width=4, state="hidden"
)

left_arm = canvas.create_line(
    200, 145, 170, 175, width=4, state="hidden"
)

right_arm = canvas.create_line(
    200, 145, 230, 175, width=4, state="hidden"
)

left_leg = canvas.create_line(
    200, 190, 170, 230, width=4, state="hidden"
)

right_leg = canvas.create_line(
    200, 190, 230, 230, width=4, state="hidden"
)

stats_title = tk.Label(
    header_frame,
    text="PLAYER STATS",
    bg="#FFD6E5",
    fg="#D94F70",
    font=("Arial", 17, "bold")
)
stats_title.pack(pady=(35, 25))
#labels
player_label = tk.Label(
    header_frame,
    text=f"Player: {player_name}",
    bg="#FFE4EF",
    fg="#D94F70",
    font=("Arial", 14, "bold")
    )
player_label.pack(pady=12)
level_label = tk.Label(
    header_frame,
    text=f"LEVEL: {current_level.upper()}",
    bg="#FFE4EF",
    fg="#D94F70",
    font=("Arial", 14, "bold")
)
level_label.pack(pady=12)

lives_label = tk.Label(
    header_frame,
    text=f"Lives: {lives} ♥",
    bg="#FFE4EF",
    fg="#FD6A63",
    font=("Arial", 13, "bold")
)
lives_label.pack(pady=12)

score_label = tk.Label(
    header_frame,
    text=f"Score: {score}",
    bg="#FFE4EF",
    fg="#78C699",
    font=("Arial", 13, "bold")
)
score_label.pack(pady=12)
high_score_label = tk.Label(
    header_frame,
    text=f"High Score: {high_score}",
    font=("Arial", 12, "bold"),
    bg="#FFE4EF"
)
high_score_label.pack(pady=12)
word_label = tk.Label(
    game_frame,
    text="_ " * len(word),
    bg="#FFE4EF",
    fg="#D94F70",
    font=("Arial", 26, "bold"),
    pady=10
)
word_label.pack(pady=10)
used_label = tk.Label(
    game_frame,
    text="Used letters: ",
    bg="#FFE4EF",
    fg="#78C699",
    font=("Arial", 11, "bold")
)
used_label.pack(pady=5)


def resize_canvas(event):
    width = event.width
    height = event.height

    line_color = "#D94F70"

    canvas.itemconfig(vertical_pole, fill=line_color)
    canvas.itemconfig(horizontal_pole, fill=line_color)
    canvas.itemconfig(rope, fill=line_color)
    canvas.itemconfig(head, outline=line_color)

    canvas.itemconfig(body, fill=line_color)
    canvas.itemconfig(left_arm, fill=line_color)
    canvas.itemconfig(right_arm, fill=line_color)
    canvas.itemconfig(left_leg, fill=line_color)
    canvas.itemconfig(right_leg, fill=line_color)

    # Canvas ke center ki position
    center_x = width / 2

    # Drawing ka size
    scale = min(width / 300, height / 300)

    # Drawing ki starting position
    start_x = center_x - (150 * scale)
    start_y = (height - 250 * scale) / 2

    # Gallows
    canvas.coords(
        vertical_pole,
        start_x, start_y,
        start_x, start_y + 200 * scale
    )

    canvas.coords(
        horizontal_pole,
        start_x, start_y,
        start_x + 150 * scale, start_y
    )

    canvas.coords(
        rope,
        start_x + 150 * scale, start_y,
        start_x + 150 * scale, start_y + 40 * scale
    )

    # Head
    canvas.coords(
        head,
        start_x + 130 * scale, start_y + 40 * scale,
        start_x + 170 * scale, start_y + 80 * scale
    )
    # Body
    canvas.coords(
        body,
        start_x + 150 * scale, start_y + 80 * scale,
        start_x + 150 * scale, start_y + 140 * scale
    )

    # Left arm
    canvas.coords(
        left_arm,
        start_x + 150 * scale, start_y + 95 * scale,
        start_x + 120 * scale, start_y + 125 * scale
    )

    # Right arm
    canvas.coords(
        right_arm,
        start_x + 150 * scale, start_y + 95 * scale,
        start_x + 180 * scale, start_y + 125 * scale
    )

    # Left leg
    canvas.coords(
        left_leg,
        start_x + 150 * scale, start_y + 140 * scale,
        start_x + 120 * scale, start_y + 180 * scale
    )

    # Right leg
    canvas.coords(
        right_leg,
        start_x + 150 * scale, start_y + 140 * scale,
        start_x + 180 * scale, start_y + 180 * scale
    )
    line_width = max(1, 4 * scale)

    canvas.itemconfig(vertical_pole, width=line_width)
    canvas.itemconfig(horizontal_pole, width=line_width)
    canvas.itemconfig(rope, width=line_width)
    canvas.itemconfig(head, width=line_width)

    canvas.itemconfig(body, width=line_width)
    canvas.itemconfig(left_arm, width=line_width)
    canvas.itemconfig(right_arm, width=line_width)
    canvas.itemconfig(left_leg, width=line_width)
    canvas.itemconfig(right_leg, width=line_width)
canvas.bind("<Configure>", resize_canvas)
def resize_text(event):
    if event.widget != root:
        return
    if not all(widget.winfo_exists() for widget in (entry, button, new_game_button)):
        return

    # Dynamic font sizes
    header_size = max(9, min(16, event.height // 45))
    word_size = max(20, min(42, event.width // 18))
    button_size = max(9, min(14, event.width // 45))

    # Header labels
    level_label.config(
        font=("Arial", header_size, "bold")
    )

    lives_label.config(
        font=("Arial", header_size, "bold")
    )

    # Word display
    word_label.config(
        font=("Arial", word_size, "bold")
    )

    # Guess input
    entry.config(
        font=("Arial", button_size + 2)
    )

    # Guess button
    button.config(
        font=("Arial", button_size),
        width=10,
        height=1
    )

    # New Game button
    new_game_button.config(
        font=("Arial", button_size),
        width=10,
        height=1
    )
    sound_button.config(
        font=("Arial", button_size),
        width=10,
        height=1
    )


control_title = tk.Label(
    control_frame,
    text="GAME CONTROLS",
    bg="#FFD6E5",
    fg="#D94F70",
    font=("Arial", 16, "bold")
)
control_title.pack(pady=(40, 30))

entry = tk.Entry(
    control_frame,
    font=("Arial", 16, "bold"),
    bg="#FFC1DA",
    fg="#D94F70",
    insertbackground="#D94F70",
    justify="center",
    relief="flat",
    width=12
)
entry.pack(pady=8, ipady=5)
entry.bind("<Return>", lambda event: Guess())
entry.focus_set()
wrong_guesses= 0

def play_sound(frequency, duration):
    if sound_on:
        winsound.Beep(frequency, duration)

def toggle_sound():
    global sound_on

    sound_on = not sound_on

    sound_button.config(
        text="Sound: ON" if sound_on else "Sound: OFF"
    )

def Guess():
    global lives, game_over, wrong_guesses, current_level, score, high_score
    if game_over:
        return

    guess = entry.get().upper()

    if len(guess) != 1 or not guess.isalpha():
        messagebox.showerror("Invalid Input", "Please enter a single alphabet")
        entry.delete(0, tk.END)
        return

    if guess in used_letters:
        messagebox.showwarning("Letter Already Used", f"{guess} already used")
        entry.delete(0, tk.END)
        return

    used_letters.append(guess)
    used_label.config(text="Used letters: " + ", ".join(sorted(used_letters)))

    if guess not in word:
        lives -= 1
        wrong_guesses+=1
        play_sound(400, 300)


        lives_label.config(text=f"Lives: {lives} left, try again")
    else:
        lives_label.config(text=f"Lives: {lives}")
        play_sound(800, 200)
        score += 1
        score_label.config(text=f"Score: {score}")
    if wrong_guesses == 1:
        canvas.itemconfig(body, state="normal")
    if wrong_guesses == 2:
        canvas.itemconfig(left_arm, state="normal")
    if wrong_guesses == 3:
        canvas.itemconfig(right_arm, state="normal")
    if wrong_guesses == 4:
        canvas.itemconfig(left_leg, state="normal")
    if wrong_guesses == 5:
        canvas.itemconfig(right_leg, state="normal")

    display = ""

    for letter in word:
        if letter in used_letters:
            display += letter + " "
        else:
            display += "_ "

    word_label.config(text=display)

    if all(letter in used_letters for letter in word_letter):
        play_sound(1000, 200)
        play_sound(1200, 300)
        print("WIN CONDITION REACHED!")

        level_index = levels.index(current_level)
        next_index = (level_index + 1) % len(levels)
        current_level = levels[next_index]
        game_over = True


        root.update_idletasks()
        word_label.config(text=" ".join(word), fg="#78C699")
        button.config(state="disabled")
        save_high_score(score, player_name)
        high_score = get_high_score(player_name)
        high_score_label.config(text=f"High Score: {high_score}")
        messagebox.showinfo("Congratulations!", "You Won! 🎉")
        New_Game()
        return


    if lives == 0:
        game_over = True
        word_label.config(text=" ".join(word), fg="#FD6A63")
        entry.config(state="disabled")
        play_sound(300, 600)
        button.config(state="disabled")
        save_high_score(score, player_name)
        high_score = get_high_score(player_name)
        high_score_label.config(text=f"High Score: {high_score}")
        messagebox.showinfo("Game Over", f"The word was {word}")
        new_game_button.focus_set()
        return

    entry.delete(0, tk.END)
def New_Game():
    global word, word_letter, lives, wrong_guesses, game_over, current_level

    word = get_random_word(current_level).upper()
    print("New Game word:", word)
    word_letter = []

    for letter in word:
        if letter not in word_letter:
            word_letter.append(letter)

    used_letters.clear()
    used_label.config(text="Used letters: ")
    lives = 5
    wrong_guesses = 0
    game_over = False
    play_sound(600, 150)

    word_label.config(text="_ " * len(word), fg="#D94F70")

    lives_label.config(text=f"Lives: {lives}")
    level_label.config(text=f"Level: {current_level.upper()}")
    score_label.config(text=f"Score: {score}")
    high_score_label.config(text=f"High Score: {high_score}")
    entry.config(state="normal")
    entry.delete(0, tk.END)
    entry.focus_set()
    canvas.itemconfig(body, state="hidden")
    canvas.itemconfig(left_arm, state="hidden")
    canvas.itemconfig(right_arm, state="hidden")
    canvas.itemconfig(left_leg, state="hidden")
    canvas.itemconfig(right_leg, state="hidden")
    button.config(state="normal")

button = tk.Button(
    control_frame,
    text="Guess",
    command=Guess,
    bg="#D94F70",
    fg="white",
    activebackground="#FF8FB1",
    activeforeground="white",
    font=("Arial", 12, "bold"),
    relief="flat",
    cursor="hand2",
    width=10,
    pady=5
)
button.pack(pady=5)
new_game_button = tk.Button(
    control_frame,
    text="New Game",
    command=New_Game,
    bg="#78C699",
    fg="white",
    activebackground="#B7E3B1",
    activeforeground="#D94F70",
    font=("Arial", 12, "bold"),
    relief="flat",
    cursor="hand2",
    width=10,
    pady=5
)
new_game_button.pack(pady=5)
sound_button = tk.Button(
    control_frame,
    text="Sound: ON",
    command=toggle_sound,
    bg="#FFC1DA",
    fg="#D94F70",
    activebackground="#FF8FB1",
    font=("Arial", 10, "bold"),
    relief="flat",
    cursor="hand2",
    width=10
)
sound_button.pack(pady=5)
# Place all controls in the right panel
entry.pack_forget()
button.pack_forget()
new_game_button.pack_forget()
sound_button.pack_forget()

entry.pack(pady=(150, 15), ipadx=15, ipady=8)
button.pack(pady=10)
new_game_button.pack(pady=10)
sound_button.pack(pady=10)
root.bind("<Configure>", resize_text)
root.mainloop()