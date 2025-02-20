import numpy as np
import sounddevice as sd
import time
import threading
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import wave
import numpy as np
import argparse
from scipy.io import wavfile
from scipy.fft import fft, ifft
import os
from scipy.signal import spectrogram
from scipy.io.wavfile import write
import math
import multiprocessing


# Audio recording parameters
SAMPLE_RATE = 48000  # 48 kHz sample rate
DURATION = 10  # Duration of recording in seconds
OUTPUT_FILE = "cpu_leakage.wav"
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
    size = 3 * 1024 * 1024 * 1024 // 8  # 3GB array
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
    audio_data = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='int16')
    sd.wait()
    wav.write(OUTPUT_FILE, SAMPLE_RATE, audio_data)
    print(f"Recording saved as {OUTPUT_FILE}")


def plot_audio_spectrum(wav_file_path, time_range=None, frequency_range=None, nfft=512, cmap='viridis'):
    """
    Plots the spectrogram of an audio file specified by 'wav_file_path'.
    
    This function reads a WAV file, converts its frames into a NumPy array to represent the audio signal, 
    and uses the matplotlib library to plot a spectrogram of the audio signal, which is a visual representation 
    of the spectrum of frequencies in the audio signal as they vary with time. The spectrogram is plotted with 
    the time on the x-axis and frequency on the y-axis.
    
    Parameters:
    - wav_file_path: Path to the WAV file to be analyzed.
    - time_range: Optional tuple specifying the time range (start, end) in seconds to plot. If None, plots the entire duration.
    - frequency_range: Optional tuple specifying the frequency range (low, high) in Hz to plot. If None, plots the full frequency range captured.
    - nfft: Number of FFT points; higher values provide finer frequency resolution. Default is 1024.
    - cmap: Colormap for the spectrogram. Default is 'plasma'.
    """
    # Read the WAV file
    sample_rate, samples = wavfile.read(wav_file_path)

    # Check if stereo and take one channel
    if samples.ndim == 2:
        samples = samples[:, 0]

    # Generate the spectrogram
    f, t, Sxx = spectrogram(samples, fs=sample_rate, nperseg=nfft)

    plt.figure(figsize=(15, 4))
    plt.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud', cmap=cmap)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.title('Spectrogram of the Audio File')
    plt.colorbar(label='Intensity [dB]')

    # Set x-axis limits based on the specified time range
    if time_range:
        plt.xlim(0,time_range)

    # Set y-axis limits based on the specified frequency range
    if frequency_range:
        plt.ylim(frequency_range,20000)

    plt.show()



if __name__ == "__main__":
    workload_thread = threading.Thread(target=workload_loop, daemon=True)
    workload_thread.start()

    record_audio()
    print("Experiment complete. Displaying spectrogram...")

    # Display the spectrogram of the recorded file
    plot_audio_spectrum(OUTPUT_FILE)