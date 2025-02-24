import time
import psutil
import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import scipy.io.wavfile as wav
import datetime

def log_system_metrics():
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    temperatures = psutil.sensors_temperatures()
    temp_readings = {sensor: [f'{temp.current}°C' for temp in temps] for sensor, temps in temperatures.items()}
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] CPU Usage: {cpu_usage}%, Memory Used: {memory_usage}%, Temperature: {temp_readings}")

def cpu_intensive_task(duration=3):
    print(f"[{datetime.datetime.now()}] CPU-intensive task started.")
    start_time = time.time()
    while time.time() - start_time < duration:
        [x ** 2 for x in range(5000000)]  # Increased computation to reach 80% CPU usage
        log_system_metrics()
    print(f"[{datetime.datetime.now()}] CPU-intensive task completed.")

def memory_intensive_task(duration=3):
    print(f"[{datetime.datetime.now()}] Memory-intensive task started.")
    try:
        size = int(psutil.virtual_memory().total * 0.75 // 8)  # Allocate ~75% of total memory
        arr = np.ones((size,), dtype=np.float64)
        time.sleep(duration)  # Simulate memory load
        log_system_metrics()
    except MemoryError:
        print("Memory allocation failed!")
    print(f"[{datetime.datetime.now()}] Memory-intensive task completed.")

def record_audio(duration=30, filename="cpu_leakage.wav"):
    print(f"[{datetime.datetime.now()}] Recording started.")
    samplerate = 44100
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()
    wav.write(filename, samplerate, recording)
    print(f"[{datetime.datetime.now()}] Recording saved as {filename}")

def generate_spectrogram(filename):
    print(f"[{datetime.datetime.now()}] Generating spectrogram...")
    samplerate, data = wav.read(filename)
    plt.specgram(data, Fs=samplerate, cmap='inferno')
    plt.xlabel('Time [s]')
    plt.ylabel('Frequency [Hz]')
    plt.title('Spectrogram')
    plt.colorbar()
    plt.show()
    print(f"[{datetime.datetime.now()}] Spectrogram displayed.")

def run_experiment(iterations=5):
    print(f"[{datetime.datetime.now()}] Experiment started.")
    record_audio(duration=30)
    
    for i in range(iterations):
        print(f"[{datetime.datetime.now()}] Iteration {i+1}: Starting active workload period.")
        start_time = time.time()
        while time.time() - start_time < 3:
            cpu_intensive_task(duration=0.1)
            memory_intensive_task(duration=0.1)
        
        print(f"[{datetime.datetime.now()}] Iteration {i+1}: Starting inactive period.")
        time.sleep(3)
    
    print(f"[{datetime.datetime.now()}] Experiment complete. Displaying spectrogram...")
    generate_spectrogram("cpu_leakage.wav")
    print(f"[{datetime.datetime.now()}] Experiment finished.")

if __name__ == "__main__":
    run_experiment()
