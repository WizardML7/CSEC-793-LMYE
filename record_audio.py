import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
import time
import datetime

def record_audio(duration, filename="cpu_leakage.wav", samplerate=44100):
    """Records audio for the specified duration and saves it to a file."""
    print(f"[{datetime.datetime.now()}] Recording started.")
    
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()  # Block until recording finishes

    # Save as 16-bit PCM WAV
    wav.write(filename, samplerate, (recording * 32767).astype(np.int16))

    print(f"[{datetime.datetime.now()}] Recording saved as {filename}")

if __name__ == "__main__":
    duration = 25  # Adjust to match the expected experiment runtime
    record_audio(duration)
