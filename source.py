import pyaudio
import numpy as np
import math
import tkinter as tk
from time import sleep

# Define your loudness threshold
LOUDNESS_THRESHOLD = 35  # Adjust this threshold as needed
# converting threshold level to dB
# LOUDNESS_THRESHOLD = np.sqrt(np.mean(LOUDNESS_THRESHOLD**2))

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Create a Tkinter window
root = tk.Tk()
root.title("Audio Blackout")

# Function to blackout the screen
def blackout_screen():
    root.attributes('-fullscreen', True)
    root.after(10000, restore_screen)  # Restore the screen after 10 seconds

# Function to restore the screen
def restore_screen():
    root.attributes('-fullscreen', False)

# Create a button to manually blackout the screen for testing
blackout_button = tk.Button(root, text="Blackout Screen", command=blackout_screen)
blackout_button.pack()

# Open a stream to capture audio from the microphone
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 2048

stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

# Main loop to monitor audio levels
while True:
    try:
        # Read audio data from the stream
        data = stream.read(CHUNK)

        # Convert audio data to a NumPy array
        audio_data = np.frombuffer(data, dtype=np.int16)

        # Calculate the root mean square (RMS) of the audio data to estimate loudness
        rms = np.sqrt(np.mean(np.square(audio_data**2)))
        print(rms)

        # Check if loudness exceeds the threshold
        if rms > LOUDNESS_THRESHOLD:
            blackout_screen()  # Blackout the screen when it's loud

        root.update()  # Update the Tkinter window to handle button clicks

    except KeyboardInterrupt:
        break

# Close the audio stream and exit
stream.stop_stream()
stream.close()
audio.terminate()
root.destroy()
