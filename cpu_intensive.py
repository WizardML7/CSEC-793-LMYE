import numpy as np
import sounddevice as sd
import time
import threading
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt
import os
import psutil
import multiprocessing
from scipy.signal import spectrogram
from datetime import datetime

# Audio recording parameters
SAMPLE_RATE = 48000  
DURATION = 30  
OUTPUT_FILE = "cpu_leakage.wav"
STOP_EVENT = threading.Event()

# Debugging log function
def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

# Monitor system resources
def monitor_resources(interval=1):
    while not STOP_EVENT.is_set():
        cpu_usage = psutil.cpu_percent()
        mem_info = psutil.virtual_memory()
        temp_info = psutil.sensors_temperatures() if hasattr(psutil, "sensors_temperatures") else {}
        temp_str = ", ".join([f"{k}: {v[0].current}°C" for k, v in temp_info.items() if v]) if temp_info else "N/A"
        
        log_event(f"CPU Usage: {cpu_usage}%, Memory Used: {mem_info.percent}%, Temperature: {temp_str}")
        time.sleep(interval)

# CPU-intensive function
def cpu_intensive():
    try:
        log_event("CPU-intensive task started.")
        x = np.random.rand(500000)  
        for _ in range(5 * 10**6):  
            np.multiply(123456, 654321)
            np.sin(x) + np.cos(x)
            np.sqrt(x) / (np.log(x + 1) + 1e-6)
        log_event("CPU-intensive task completed.")
    except Exception as e:
        log_event(f"CPU task error: {e}")

# Memory-intensive function
def memory_intensive():
    try:
        log_event("Memory-intensive task started.")
        size = 1024 * 1024 * 500 // 8  
        arr = np.zeros((size,), dtype=np.float64)
        indices = np.random.randint(0, size, size // 10)  
        for _ in range(10):  
            arr[indices] += np.random.rand(len(indices))
        log_event("Memory-intensive task completed.")
    except MemoryError:
        log_event("Memory allocation failed!")
    except Exception as e:
        log_event(f"Memory task error: {e}")

# Workload loop with improved logging
def workload_loop():
    start_time = time.time()
    num_threads = max(2, multiprocessing.cpu_count() // 2)  
    log_event(f"Starting {num_threads} worker threads...")

    iteration = 0
    while time.time() - start_time < DURATION:
        if STOP_EVENT.is_set():
            break

        iteration += 1
        log_event(f"Iteration {iteration}: Starting active workload period.")

        # Start CPU and memory tasks
        threads = []
        for i in range(num_threads):
            t = threading.Thread(target=cpu_intensive if i % 2 == 0 else memory_intensive)
            t.start()
            threads.append(t)
        
        time.sleep(5)  # Run for 5 seconds
        
        STOP_EVENT.set()
        for t in threads:
            t.join()
        
        STOP_EVENT.clear()
        log_event(f"Iteration {iteration}: Inactive period started. Sleeping for 5 seconds.")
        time.sleep(5)  

    log_event("Workload loop completed.")

# Audio recording function
def record_audio():
    log_event("Recording started.")
    audio_data = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype='float32')
    sd.wait()
    wav.write(OUTPUT_FILE, SAMPLE_RATE, audio_data)
    log_event(f"Recording saved as {OUTPUT_FILE}")

# Spectrogram analysis
def plot_audio_spectrum(wav_file_path):
    log_event("Generating spectrogram...")
    sample_rate, samples = wav.read(wav_file_path)
    
    if samples.ndim == 2:
        samples = samples[:, 0]

    f, t, Sxx = spectrogram(samples, fs=sample_rate, nperseg=512)
    plt.figure(figsize=(15, 4))
    plt.pcolormesh(t, f, 10 * np.log10(Sxx + 1e-10), shading='gouraud', cmap='viridis')  
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.title('Spectrogram of Recorded Audio')
    plt.colorbar(label='Intensity [dB]')
    plt.show()
    log_event("Spectrogram displayed.")

# Main execution
if __name__ == "__main__":
    log_event("Experiment started.")
    
    monitor_thread = threading.Thread(target=monitor_resources, daemon=True)
    monitor_thread.start()

    workload_thread = threading.Thread(target=workload_loop, daemon=True)
    workload_thread.start()
    
    record_audio()
    
    log_event("Experiment complete. Displaying spectrogram...")
    plot_audio_spectrum(OUTPUT_FILE)
    log_event("Experiment finished.")
