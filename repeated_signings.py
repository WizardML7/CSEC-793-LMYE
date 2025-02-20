import socket
import os
import libgcrypt_wrapper as gcrypt  # Import the wrapper
import re

# Define the host and port for the server
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 65432      # Port to listen on

# Load the signing key
def load_signing_key():
    key_path = "private_key.pem"
    if not os.path.exists(key_path):
        # Create a temporary file for the key parameters
        key_params = (
            "Key-Type: default\n"
            "Key-Usage: sign\n"
            "Subkey-Type: default\n"
            "Subkey-Usage: sign\n"
            "Name-Real: Test User\n"
            "Name-Comment: Test Comment\n"
            "Name-Email: test@example.com\n"
            "Expire-Date: 1y\n"
        )
        with open("key_params.txt", "w") as f:
            f.write(key_params)

        print("Generating GPG key...", flush=True)
        # Generate the key using the temporary file
        os.system("gpg --batch --gen-key --pinentry-mode loopback --passphrase '' key_params.txt")
        print("GPG key generation completed.", flush=True)

        # Clean up the temporary file
        os.remove("key_params.txt")
        
    return key_path

def main():
    # Initialize Libgcrypt
    print("Initializing Libgcrypt...", flush=True)
    gcrypt.initialize()
    print("Libgcrypt initialized.", flush=True)

    # Load the signing key
    private_key_path = load_signing_key()
    print("Private key loaded from:", private_key_path, flush=True)

    # Create a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Listening on {HOST}:{PORT}", flush=True)

        while True:
            conn, addr = server_socket.accept()
            print(f"Connection accepted from {addr}", flush=True)
            with conn:
                print(f"Connected by {addr}", flush=True)
                data = conn.recv(1024)
                if not data:
                    print("No data received, closing connection.", flush=True)
                    break
                
                message = data.decode('utf-8')
                print(f"Received message: '{message}'", flush=True)

                # Sign the message using the wrapper
                print("Signing the message...", flush=True)
                signature = gcrypt.sign_message(message.encode('utf-8'), private_key_path)

                # Check if the signature generation was successful
                if signature is not None:
                    # Use regex to extract the entire PGP signature block
                    signature_match = re.search(r'(-----BEGIN PGP SIGNATURE-----.*?-----END PGP SIGNATURE-----)', signature, re.DOTALL)
                    if signature_match:
                        extracted_signature = signature_match.group(0)  # Capture the full signature block
                    else:
                        extracted_signature = signature  # Fallback if no match is found

                    print(f"Generated signature: {extracted_signature}", flush=True)

                    # Send the signature back to the client
                    conn.sendall(extracted_signature.encode('utf-8'))  # Ensure the signature is sent as bytes
                    print(f"Sent signature: '{extracted_signature}'", flush=True)
                else:
                    print("Failed to generate a signature. Sending placeholder.", flush=True)
                    conn.sendall(b'signature_placeholder')

                print("Closing connection with client.", flush=True)
            print("Waiting for the next connection...", flush=True)

if __name__ == "__main__":
    main()
