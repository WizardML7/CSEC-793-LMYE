#cpu_alternate.py
import time

def heavy_computation():
    start_time = time.time()
    current_time = time.time()
    x = 1
    while (current_time - start_time) < 5:
        x = (x * x) % 123456789
        current_time = time.time()

if __name__ == "__main__":
    try:
        heavy_computation()
    except KeyboardInterrupt:
        print("\nProcess terminated by user.")