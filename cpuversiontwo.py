import numpy as np
import sounddevice as sd
import time
import threading
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import spectrogram
from Crypto.Cipher import AES
import os

# Audio recording parameters
SAMPLE_RATE = 96000  # Higher than the paper's sample rate
DURATION = 15  # Increased duration for more data
OUTPUT_FILE = "cpu_leakage_v2.wav"
STOP_EVENT = threading.Event()

# AES-based CPU-intensive function
def cpu_intensive():
    """Performs AES encryption repeatedly to stress the CPU."""
    key = os.urandom(16)  # 128-bit AES key
    cipher = AES.new(key, AES.MODE_ECB)
    plaintext = os.urandom(16)  # Random 16-byte block

    for _ in range(10**7):  # High iteration count
        _ = cipher.encrypt(plaintext)

# Multi-threaded workload function
def workload_loop():
    """Runs multiple CPU tasks in parallel without sleep."""
    start_time = time.time()
    threads = []
    num_threads = os.cpu_count() // 2  # Utilize multiple cores
    print(f"Starting {num_threads} worker threads...")

    for _ in range(num_threads):
        t = threading.Thread(target=cpu_intensive)
        t.start()
        threads.append(t)

    while time.time() - start_time < DURATION:
        if STOP_EVENT.is_set():
            break

    # Stop all workload threads
    STOP_EVENT.set()
    for t in threads:
        t.join()

# Recording function
def record_audio():
    print("Recording audio...")
    audio_data = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
    sd.wait()

    # Normalize audio
    audio_data = audio_data / np.max(np.abs(audio_data))

    # Save recording
    wav.write(OUTPUT_FILE, SAMPLE_RATE, (audio_data * 32767).astype(np.int16))
    print(f"Recording saved as {OUTPUT_FILE}")

# Spectrogram plotting function
def plot_audio_spectrum(wav_file_path, nfft=8192, cmap='viridis'):
    """Plots the spectrogram with high resolution and normalization."""
    sample_rate, samples = wavfile.read(wav_file_path)

    # Convert to float32 for better processing
    samples = samples.astype(np.float32) / 32767.0  

    # Generate the spectrogram
    f, t, Sxx = spectrogram(samples, fs=sample_rate, nperseg=nfft, noverlap=nfft // 2)

    plt.figure(figsize=(15, 4))
    plt.pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud', cmap=cmap)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.title('High-Resolution Spectrogram of CPU Leakage')
    plt.colorbar(label='Intensity [dB]')
    plt.ylim(500, 20000)  # Ignore low-frequency noise
    plt.show()

# Run workload and recording simultaneously
if __name__ == "__main__":
    workload_thread = threading.Thread(target=workload_loop)
    workload_thread.start()

    record_audio()

    # Stop workload after recording
    STOP_EVENT.set()
    workload_thread.join()

    print("Experiment complete. Displaying spectrogram...")
    plot_audio_spectrum(OUTPUT_FILE)

    print("Exiting program.")
