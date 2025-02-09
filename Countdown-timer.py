import time
import os
import platform
import tkinter as tk
import threading

# Global variables
running = False  # Controls the countdown process
remaining_time = 0  # Stores the countdown time

def play_alarm():
    """Plays the alarm sound once when the countdown finishes."""
    if platform.system() == "Windows":
        import winsound
        winsound.Beep(1500, 2000)  # Frequency: 1500 Hz, Duration: 2000 ms
    elif platform.system() == "Darwin":  # macOS
        os.system('say "Time is up"')  
    else:  # Linux
        os.system('notify-send "Time is up!" && aplay /usr/share/sounds/alsa/Front_Center.wav')

def update_timer():
    """Updates the countdown timer display in real-time."""
    global remaining_time, running
    
    while running and remaining_time > 0:
        mins, secs = divmod(remaining_time, 60)
        timer_label.config(text=f"{mins:02d}:{secs:02d}")
        time.sleep(1)
        remaining_time -= 1
        # Ensure the UI updates immediately
        root.update_idletasks()

    if remaining_time == 0 and running:
        timer_label.config(text="⏰ Time's Up!")
        play_alarm()  

def start_countdown():
    """Starts the countdown timer."""
    global running, remaining_time
    if running:
        return  # Prevent multiple starts
    
    try:
        remaining_time = int(entry.get())  # Get user input in seconds
        if remaining_time <= 0:
            raise ValueError

        running = True
        threading.Thread(target=update_timer, daemon=True).start()  # Run countdown in background

    except ValueError:
        timer_label.config(text="Invalid input. Enter a number.")

def stop_countdown():
    """Stops the countdown."""
    global running
    running = False
    timer_label.config(text="00:00")  # Reset display

# Create the GUI window
root = tk.Tk()
root.title("Countdown Timer Script")
root.geometry("700x600")

# UI Elements
entry_label = tk.Label(root, text="Enter time (seconds):", font=("Arial", 16))
entry_label.pack()

entry = tk.Entry(root, font=("Arial", 14))
entry.pack()

start_button = tk.Button(root, text="Start", font=("Arial", 16), command=start_countdown)
start_button.pack(pady=10)

stop_button = tk.Button(root, text="Stop", font=("Arial", 16), command=stop_countdown)
stop_button.pack(pady=10)

timer_label = tk.Label(root, text="00:00", font=("Arial", 40))
timer_label.pack()

# Run the GUI event loop
root.mainloop()
