import multiprocessing
import time
import psutil
import datetime
import os

LOG_FILE = "cpu_timestamps.log"

def log_system_metrics():
    """Logs current CPU usage."""
    cpu_usage = psutil.cpu_percent(interval=0.1)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] CPU Usage: {cpu_usage}%")

def log_cpu_start_time(worker_id):
    """Logs the timestamp of when a worker starts."""
    timestamp = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]  # Keep milliseconds
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp}\n")
    print(f"Worker {worker_id} (PID {os.getpid()}) started at {timestamp}.")

def heavy_computation(worker_id):
    """Performs CPU-intensive operations for a fixed duration."""
    log_cpu_start_time(worker_id)
    end_time = time.time() + 2  # Run for 2 seconds

    # Introduce a large array to force memory/cache pressure
    arr = [i for i in range(100_000)]  # Forces memory allocation

    while time.time() < end_time:
        for i in range(len(arr)):
            arr[i] = (arr[i] * arr[i]) % 123456789  # Introduce dependency on previous computations
            if time.time() >= end_time:
                break  # Exit if the time is up

    print(f"Worker {worker_id} (PID {os.getpid()}) finished.")

def cpu_intensive_task(num_workers=None):
    """Runs CPU load using multiple independent worker processes."""
    if num_workers is None:
        num_workers = multiprocessing.cpu_count()  # Use all available cores

    print(f"Starting CPU-intensive task with {num_workers} workers.")

    workers = []
    for i in range(num_workers):
        p = multiprocessing.Process(target=heavy_computation, args=(i,))
        workers.append(p)
        p.start()

    for p in workers:
        p.join()

    print("CPU-intensive task completed.")

def run_cpu_experiment(iterations=5):
    """Runs the CPU-intensive workload for a set number of iterations."""
    print(f"[{datetime.datetime.now()}] CPU workload experiment started.")

    for i in range(iterations):
        print(f"[{datetime.datetime.now()}] Iteration {i+1}: Starting active workload period.")
        cpu_intensive_task()
        print(f"[{datetime.datetime.now()}] Iteration {i+1}: Starting inactive period.")
        time.sleep(1)  # Rest period between tasks

    print(f"[{datetime.datetime.now()}] CPU workload experiment complete.")

if __name__ == "__main__":
    time.sleep(2)  # Small delay to ensure recording has started
    run_cpu_experiment()
