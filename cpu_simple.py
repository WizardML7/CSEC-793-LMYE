#cpu_simple.py
def heavy_computation():
    x = 1
    while True:
        x = (x * x) % 123456789

if __name__ == "__main__":
    try:
        heavy_computation()
    except KeyboardInterrupt:
        print("\nProcess terminated by user.")