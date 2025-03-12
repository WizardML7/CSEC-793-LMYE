import sounddevice as sd
import numpy as np
import wave
import time
import datetime
import os

# Configuration
NUM_RUNS = 100  # Must match victim script
DURATION = 10  # Each recording duration in seconds
SAMPLERATE = 48000  # Common sample rate
DEVICE = 17  # Ensure this is correct (VB-Audio Virtual Cable)
RECORDING_DIR = "recordings/voip_alternating/"

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
    time.sleep(15)  # Running to the victim to start that script

    print(f"Starting {NUM_RUNS} recording runs.")

    for i in range(NUM_RUNS):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(RECORDING_DIR, f"voip_capture_{timestamp}.wav")
        
        print(f"Run {i+1}/{NUM_RUNS}")
        record_audio(DURATION, filename)
        
        time.sleep(2)  # Short pause before next run

    print("All recordings complete.")
