from dilithium.core import DilithiumParams
from dilithium.keygen import KeyGenerator
from dilithium.sign import Signer
from dilithium.verify import Verifier
import time
import numpy as np
from dilithium.chaos import HybridEncryption

def print_key(name: str, key: dict):
    print(f"\n{name}:")
    for k, v in key.items():
        if isinstance(v, np.ndarray):
            print(f"  {k}: array of shape {v.shape}, first few values: {v.flatten()[:5]}")
        else:
            print(f"  {k}: {v[:20]}..." if isinstance(v, bytes) else f"  {k}: {v}")

def main():
    # Initialize hybrid system
    params = DilithiumParams.get_params(security_level=3)
    hybrid = HybridEncryption(params)
    
    # Generate keys
    print("\nGenerating keys...")
    start = time.time()
    public_key, private_key = hybrid.generate_keys()
    print(f"Key generation: {(time.time() - start)*1000:.2f}ms")
    
    # Print keys
    print_key("Public Key", public_key)
    print_key("Private Key", private_key)
    
    # Original message
    message = b"Hello, Quantum-Resistant World!"
    print(f"\nOriginal message: {message.decode()}")
    
    # Encrypt and sign
    start = time.time()
    ciphertext, nonce, signature = hybrid.encrypt_and_sign(message, private_key)
    print(f"Encryption and signing: {(time.time() - start)*1000:.2f}ms")
    print(f"Ciphertext (hex): {ciphertext.hex()[:50]}...")
    print(f"Nonce (hex): {nonce.hex()}")
    
    # Verify and decrypt
    start = time.time()
    decrypted = hybrid.verify_and_decrypt(ciphertext, nonce, signature, public_key)
    print(f"Verification and decryption: {(time.time() - start)*1000:.2f}ms")
    print(f"Decrypted message: {decrypted.decode()}")
    
    # Verify integrity
    print("\nVerification summary:")
    print(f"Message integrity: {message == decrypted}")

if __name__ == "__main__":
    main() 