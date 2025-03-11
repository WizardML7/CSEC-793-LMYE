#record_audio.py
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import time
import datetime
import sys

def record_audio(duration, filename="voip_capture.wav", samplerate=44100, device=None):
    """Records audio for the specified duration and saves it to a file."""
    print(f"[{datetime.datetime.now()}] Recording started: {filename}")

    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32', device=device)
    sd.wait()  # Block until recording finishes

    # Save as 16-bit PCM WAV
    wav.write(filename, samplerate, (recording * 32767).astype(np.int16))

    print(f"[{datetime.datetime.now()}] Recording saved as {filename}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 record_audio.py <duration> <filename>")
        sys.exit(1)

    duration = int(sys.argv[1])  # Get duration from command-line argument
    filename = sys.argv[2]  # Get filename from command-line argument

    print(sd.query_devices())

    record_audio(duration, filename, device=23)