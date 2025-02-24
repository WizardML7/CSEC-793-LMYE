import numpy as np
import sounddevice as sd
import time
import threading
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import spectrogram
#from Crypto.Cipher import AES
import os
import multiprocessing

# Audio recording parameters
SAMPLE_RATE = 96000  # Higher than the paper's sample rate
DURATION = 15  # Increased duration for more data
OUTPUT_FILE = "cpu_leakage_v2.wav"
STOP_EVENT = threading.Event()

# Intense CPU workload
def cpu_intensive():
    """Performs heavy floating-point and integer operations."""
    x = np.random.rand(1000000)  # Large array for floating point ops
    for _ in range(10**7):  # 10x more iterations
        np.multiply(123456, 654321)
        np.sin(x) + np.cos(x)  # Floating-point stress
        np.sqrt(x) / (np.log(x + 1) + 1e-6)  # Additional floating-point ops

# Intense Memory Workload (3GB RAM)
def memory_intensive():
    """Allocates and modifies a large 3GB array with random access patterns."""
    size = 1024 * 1024 * 1024 // 8  # 3GB array
    arr = np.zeros((size,), dtype=np.float64)
    indices = np.random.randint(0, size, size // 10)  # Random access pattern
    for _ in range(20):  # More iterations to sustain pressure
        arr[indices] += np.random.rand(len(indices))

# Multi-threaded workload function
def workload_loop():
    """Runs multiple CPU and memory tasks in parallel."""
    start_time = time.time()
    num_threads = max(2, multiprocessing.cpu_count() // 2)  # Utilize multiple CPU cores
    print(f"Starting {num_threads} worker threads...")

    # Create a mix of CPU and memory stress tasks
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=cpu_intensive if i % 2 == 0 else memory_intensive)
        t.start()
        threads.append(t)

    while time.time() - start_time < DURATION:
        if STOP_EVENT.is_set():
            break
        time.sleep(1)  # Let the tasks run

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

if __name__ == "__main__":
    workload_thread = threading.Thread(target=workload_loop, daemon=True)
    workload_thread.start()

    record_audio()
    print("Experiment complete. Displaying spectrogram...")

    # Display the spectrogram of the recorded file
    plot_audio_spectrum(OUTPUT_FILE)
