import ctypes
from ctypes import c_char_p, c_void_p, c_size_t, c_int, create_string_buffer, byref
import subprocess

# Load Libgcrypt
libgcrypt = ctypes.CDLL('libgcrypt.so')

# Function prototypes for Libgcrypt
libgcrypt.gcry_check_version.argtypes = [c_char_p]
libgcrypt.gcry_check_version.restype = c_char_p

# Initialize Libgcrypt
def initialize():
    version = libgcrypt.gcry_check_version(b'1.8.4')
    if version is None:
        raise RuntimeError("Libgcrypt initialization failed.")
    print("Libgcrypt initialized.", flush=True)

# Sign a message using GPG
def sign_message(message, private_key_path):
    print("Signing the message...", flush=True)

    # Use GPG command-line to sign the message
    process = subprocess.Popen(
        ['gpg', '--batch', '--yes', '--passphrase', '', '--sign', '--armor', '--output', '-', '--detach-sign'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True  # Enable text mode for input and output
    )

    # Send the message to GPG for signing as a string
    stdout, stderr = process.communicate(input=message.decode('utf-8'))  # Decode bytes to string

    if process.returncode != 0:
        raise RuntimeError(f"GPG signing failed: {stderr.strip()}")

    print(f"Generated signature: {stdout.strip()}", flush=True)  # Print signature in text format
    return stdout.strip()  # Return the generated signature
