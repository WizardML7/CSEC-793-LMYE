import sounddevice as sd
import numpy as np
import wave
import time
import datetime
import os

# Configuration
NUM_RUNS = 100  # Must match victim script
DURATION = 40  # Match victim's browsing duration
SAMPLERATE = 48000  # Common sample rate
DEVICE = 17  # Ensure this is correct (VB-Audio Virtual Cable)
RECORDING_DIR = "recordings/voip_web/"
WEBSITES = [
    "reuters", "economictimes", "indianexpress", "news_au",
    "chinadaily", "latimes", "nytimes", "forbes",
    "newsweek", "bloomberg_middleeast", "foxnews",
    "abcnews", "euronews", "nationalgeographic"
]

# Ensure recording directory exists
os.makedirs(RECORDING_DIR, exist_ok=True)

def record_audio(duration, filename):
    """Records audio for the specified duration and saves it to a file."""
    print(f"[{datetime.datetime.now()}] Recording started: {filename}")

    recording = sd.rec(
        int(duration * SAMPLERATE),
        samplerate=SAMPLERATE,
        channels=2,
        dtype='float32',
        device=DEVICE,
        blocking=True
    )
    
    # Convert to 16-bit PCM format
    recording = np.int16(recording * 32767)

    # Save as WAV file
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(SAMPLERATE)
        wf.writeframes(recording.tobytes())

    print(f"[{datetime.datetime.now()}] Recording saved as {filename}")

if __name__ == "__main__":
    print("Waiting 15 seconds before starting to align with victim...")
    time.sleep(15)  # Sync start time with victim

    print(f"Starting {NUM_RUNS} recording runs.")

    for i in range(NUM_RUNS):
        website_index = i % len(WEBSITES)  # Loop through websites
        website_name = WEBSITES[website_index]
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(RECORDING_DIR, f"{website_name}_{timestamp}.wav")
        
        print(f"Run {i+1}/{NUM_RUNS} - Recording for {website_name}")
        record_audio(DURATION, filename)
        
        time.sleep(5)  # Match pause duration from victim script

    print("All recordings complete.")
