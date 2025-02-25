import multiprocessing
import time
import psutil
import datetime
import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np

# Ensure compatibility with Windows multiprocessing
multiprocessing.set_start_method("spawn", force=True)

def log_system_metrics():
    """Logs current CPU usage."""
    cpu_usage = psutil.cpu_percent(interval=0.1)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] CPU Usage: {cpu_usage}%")

def heavy_computation(_):
    """Performs CPU-intensive operations for a fixed time."""
    start_time = time.time()
    while time.time() - start_time < 0.8:  # Ensure the task runs for 0.8 seconds
        [x * x for x in range(50_000_000)]  

def cpu_intensive_task(num_workers=None):
    """Runs CPU load using multiple workers in a process pool."""
    if num_workers is None:
        num_workers = multiprocessing.cpu_count()  # Use all available cores

    print(f"[{datetime.datetime.now()}] CPU-intensive task started with {num_workers} workers.")

    with multiprocessing.Pool(num_workers) as pool:
        pool.map(heavy_computation, range(num_workers))  

    log_system_metrics()
    print(f"[{datetime.datetime.now()}] CPU-intensive task completed.")

def record_audio(duration, samplerate=44100):
    """Records audio and returns the audio data."""
    print(f"[{datetime.datetime.now()}] Recording started.")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()  # Block until recording is done
    print(f"[{datetime.datetime.now()}] Recording complete.")
    return recording, samplerate

def run_experiment(iterations=5):
    """Runs the experiment with CPU workload alternating with idle periods, while recording audio."""
    print(f"[{datetime.datetime.now()}] Experiment started.")

    total_duration = iterations * (0.8 + 0.4)  # Total recording time
    recording, samplerate = record_audio(total_duration)  # Start recording synchronously

    for i in range(iterations):
        print(f"[{datetime.datetime.now()}] Iteration {i+1}: Starting active workload period.")
        cpu_intensive_task()
        print(f"[{datetime.datetime.now()}] Iteration {i+1}: Starting inactive period.")
        time.sleep(0.4)

    # Save recorded audio after experiment is done
    filename = "cpu_leakage.wav"
    wav.write(filename, samplerate, (recording * 32767).astype(np.int16))  # Convert to 16-bit PCM
    print(f"[{datetime.datetime.now()}] Recording saved as {filename}")
    print(f"[{datetime.datetime.now()}] Experiment complete.")

if __name__ == "__main__":
    run_experiment()
