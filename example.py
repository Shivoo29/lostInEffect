from dilithium.core import DilithiumParams
from dilithium.keygen import KeyGenerator
from dilithium.sign import Signer
from dilithium.verify import Verifier
import time

def main():
    # Initialize with security level 3
    params = DilithiumParams.get_params(security_level=3)
    
    # Time key generation
    start = time.time()
    keygen = KeyGenerator(params)
    public_key, private_key = keygen.generate_keypair()
    print(f"Key generation: {(time.time() - start)*1000:.2f}ms")
    
    # Time signing
    message = b"Hello, Quantum-Resistant World!"
    signer = Signer(params)
    start = time.time()
    signature = signer.sign(message, private_key)
    print(f"Signing: {(time.time() - start)*1000:.2f}ms")
    
    # Time verification
    verifier = Verifier(params)
    start = time.time()
    is_valid = verifier.verify(message, signature, public_key)
    print(f"Verification: {(time.time() - start)*1000:.2f}ms")
    
    print(f"Signature valid: {is_valid}")

if __name__ == "__main__":
    main() 