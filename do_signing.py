import os
import ecdsa

def generate_key_pair():
    """Generate a new ECDSA key pair."""
    # Generate a new private key
    private_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
    public_key = private_key.get_verifying_key()
    
    return private_key, public_key

def sign_message(private_key, message):
    """Sign a message using the provided private key."""
    signature = private_key.sign(message)
    return signature

def verify_signature(public_key, message, signature):
    """Verify the signature of a message using the public key."""
    try:
        return public_key.verify(signature, message)
    except ecdsa.BadSignatureError:
        return False

def main():
    # Generate key pair
    private_key, public_key = generate_key_pair()
    print("Private key:", private_key.to_string().hex())
    print("Public key:", public_key.to_string().hex())

    # Message to be signed
    message = b"This is a test message."
    print("Message:", message)

    # Sign the message
    signature = sign_message(private_key, message)
    print("Signature:", signature.hex())

    # Verify the signature
    is_valid = verify_signature(public_key, message, signature)
    print("Is the signature valid?", is_valid)

if __name__ == "__main__":
    main()
