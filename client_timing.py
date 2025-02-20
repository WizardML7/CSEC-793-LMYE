import socket
import time
import csv

SERVER_HOST = '192.168.68.101' 
SERVER_PORT = 65432
NUM_SIGNINGS = 10000
MESSAGE = "Hello, World!"
OUTPUT_FILE = "timing_results.csv"

def main():
    try:
        with open(OUTPUT_FILE, mode='w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Request Number", "Send Timestamp", "Receive Timestamp", "Duration (ms)"])

            # Start the signing requests
            print(f"Connecting to {SERVER_HOST}:{SERVER_PORT}...")
            for i in range(NUM_SIGNINGS):
                try:
                    # Create a new connection for each request
                    with socket.create_connection((SERVER_HOST, SERVER_PORT)) as client_socket:
                        # Record the time before sending the request
                        send_time = time.perf_counter()

                        # Send the message
                        client_socket.sendall(MESSAGE.encode('utf-8'))

                        # Receive the response (signature)
                        signature = client_socket.recv(4096).decode('utf-8')

                        # Record the time after receiving the response
                        receive_time = time.perf_counter()

                        # Calculate duration in milliseconds
                        duration = (receive_time - send_time) * 1000

                        # Log the results
                        csv_writer.writerow([i + 1, send_time, receive_time, duration])
                        print(f"Request {i + 1}: Duration = {duration:.3f} ms")

                except (socket.error, BrokenPipeError) as e:
                    print(f"Error on request {i + 1}: {e}")
                    time.sleep(0.1)  # Add a delay to avoid overwhelming the server

        print(f"Results saved to {OUTPUT_FILE}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
