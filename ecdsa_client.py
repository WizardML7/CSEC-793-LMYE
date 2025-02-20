import socket

# Server details
HOST = '192.168.68.97'  # Replace with the server's IP or hostname if on another device
PORT = 65432

# Message to send
message = "Hello, World!"

for _ in range(25000):

    # Connect to the server
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))
            print(f"Connected to {HOST}:{PORT}")

            # Send the message
            client_socket.sendall(message.encode('utf-8') + b'\n')  # Add a newline to simulate PowerShell behavior
            print(f"Sent message: {message}")

            # Receive the signature
            received_data = b""
            while True:
                chunk = client_socket.recv(1024)
                if not chunk:
                    break
                received_data += chunk

            # Decode the received data
            response = received_data.decode('utf-8')

            # Extract the signature between BEGIN and END PGP SIGNATURE
            signature_lines = []
            inside_signature_block = False

            for line in response.splitlines():
                if line == "-----BEGIN PGP SIGNATURE-----":
                    inside_signature_block = True
                    continue
                if line == "-----END PGP SIGNATURE-----":
                    break
                if inside_signature_block:
                    signature_lines.append(line)

            # Join the extracted lines
            signature = "\n".join(signature_lines)

            if signature:
                print("Extracted Signature:")
                print(signature)
                print(f"Signature Length: {len(signature)} characters")
            else:
                print("No valid signature found in the response.")

    except ConnectionError as e:
        print(f"Connection error: {e}")
