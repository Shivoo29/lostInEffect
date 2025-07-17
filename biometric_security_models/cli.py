import os
import json
import sys
import time
import random

from main import SecureBiometricSystem

# Initialize the biometric system once
system = SecureBiometricSystem()

# ANSI escape codes for colors
GREEN = '\033[92m'
RESET = '\033[0m'

def clear_terminal():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_matrix_banner():
    """Displays a fancy matrix-style ASCII art banner."""
    banner = r"""
 ▄            ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄        ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ 
▐░▌          ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░▌      ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌
▐░▌          ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀  ▀▀▀▀█░█▀▀▀▀  ▀▀▀▀█░█▀▀▀▀ ▐░▌░▌     ▐░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀  ▀▀▀▀█░█▀▀▀▀ 
▐░▌          ▐░▌       ▐░▌▐░▌               ▐░▌          ▐░▌     ▐░▌▐░▌    ▐░▌▐░▌          ▐░▌          ▐░▌          ▐░▌          ▐░▌               ▐░▌     
▐░▌          ▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄▄▄      ▐░▌          ▐░▌     ▐░▌ ▐░▌   ▐░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌               ▐░▌     
▐░▌          ▐░▌       ▐░▌▐░░░░░░░░░░░▌     ▐░▌          ▐░▌     ▐░▌  ▐░▌  ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌               ▐░▌     
▐░▌          ▐░▌       ▐░▌ ▀▀▀▀▀▀▀▀▀█░▌     ▐░▌          ▐░▌     ▐░▌   ▐░▌ ▐░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░▌               ▐░▌     
▐░▌          ▐░▌       ▐░▌          ▐░▌     ▐░▌          ▐░▌     ▐░▌    ▐░▌▐░▌▐░▌          ▐░▌          ▐░▌          ▐░▌          ▐░▌               ▐░▌     
▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄█░▌ ▄▄▄▄▄▄▄▄▄█░▌     ▐░▌      ▄▄▄▄█░█▄▄▄▄ ▐░▌     ▐░▐░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░▌          ▐░▌          ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄      ▐░▌     
▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ▐░▌     ▐░░░░░░░░░░░▌▐░▌      ▐░░▌▐░░░░░░░░░░░▌▐░▌          ▐░▌          ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌     ▐░▌     
 ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀       ▀       ▀▀▀▀▀▀▀▀▀▀▀  ▀        ▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀            ▀            ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀       ▀      
                                                                                                                                                            
"""
    for line in banner.splitlines():
        print(GREEN + line + RESET)
        time.sleep(0.005) # Simulate matrix effect

def display_banner():
    """Clears terminal and displays the fancy banner."""
    clear_terminal()
    display_matrix_banner()
    print(GREEN + "\n" + "="*50 + RESET)
    print(GREEN + "          LOSTINEFFECT BIOMETRIC CLI" + RESET)
    print(GREEN + "="*50 + "\n" + RESET)

def display_menu():
    """Displays the main menu options."""
    print("Please choose an option:")
    print("1. Test Adversarial Detector")
    print("2. Test Behavioral Analytics")
    print("3. Run Full Biometric Authentication Flow")
    print("4. Contextual Spoofing Defense (Simulated)")
    print("5. Edge AI Poisoning Defense (Simulated)")
    print("6. Exit")
    print("-" * 50)

def run_test_adversarial():
    """Handles the interactive 'test-adversarial' command."""
    print("\n--- Test Adversarial Detector ---")
    print("This module analyzes metadata of a given image file to determine if it might be synthetic or an adversarial sample.")
    
    while True:
        image_path = input("Enter the path to the face image file (e.g., ../dummy_face.jpg): ").strip()
        if not os.path.exists(image_path):
            print(f"Error: File not found at '{image_path}'. Please try again.")
        else:
            break

    print("Analyzing image...")
    result = system.adversarial_detector.detect_adversarial_attack(image_path)
    print("\nAnalysis Result:")
    print(json.dumps(result, indent=4))
    input("\nPress Enter to continue...")

def run_test_behavioral():
    """Handles the interactive 'test-behavioral' command."""
    print("\n--- Test Behavioral Analytics ---")
    print("This module analyzes a fingerprint hex string for demonstrable patterns to detect anomalies.")
    
    fingerprint_image_path = input("Enter the path to the fingerprint image file (e.g., ../fingerprintencryptor/capture_sessions/SESSION_20250630_203945_22ba9bbb_fingerprint.hex): ").strip()
    if not os.path.exists(fingerprint_image_path):
        print(f"Error: File not found at '{fingerprint_image_path}'. Please try again.")
        return

    print("Analyzing fingerprint data...")
    result = system.behavioral_analytics.analyze_fingerprint_image(fingerprint_image_path)
    print("\nAnalysis Result:")
    print(json.dumps(result, indent=4))
    input("\nPress Enter to continue...")

def run_full_authentication():
    """Handles the interactive 'authenticate' command."""
    print("\n--- Run Full Biometric Authentication Flow ---")
    print("This runs a multi-modal authentication flow, integrating various biometric security models.")
    
    user_id = input("Enter the user ID: ").strip()
    
    while True:
        face_image_path = input("Enter the path to the face image file (e.g., ../dummy_face.jpg): ").strip()
        if not os.path.exists(face_image_path):
            print(f"Error: File not found at '{face_image_path}'. Please try again.")
        else:
            break

    fingerprint_image_path = input("Enter the path to the fingerprint image file (e.g., ../datasets/Sokoto_conventry_Fingerprint_Dataset/SOCOFing/Real/1__M_Left_index_finger.BMP): ").strip()
    if not os.path.exists(fingerprint_image_path):
        print(f"Error: File not found at '{fingerprint_image_path}'. Please try again.")
        return

    # Optional context data
    location_change = input("Is there a location change? (y/n): ").strip().lower() == 'y'
    device_change = input("Is there a device change? (y/n): ").strip().lower() == 'y'
    network_change = input("Is there a network change? (y/n): ").strip().lower() == 'y'
    
    failed_attempts_input = input("Number of recent failed attempts (default: 0): ").strip()
    failed_attempts = int(failed_attempts_input) if failed_attempts_input.isdigit() else 0

    biometric_data = {
        "face_image_path": face_image_path,
        "fingerprint_image_path": fingerprint_image_path
    }

    context_data = {
        'location_change': location_change,
        'device_change': device_change,
        'network_change': network_change,
        'failed_attempts': failed_attempts,
        'lighting': 'good',  # Assuming good lighting for CLI demo
        'noise_level': 0.1    # Assuming low noise for CLI demo
    }

    print("\nRunning authentication...")
    result = system.authenticate_user(user_id, biometric_data, context_data)
    print("\nAuthentication Result:")
    print(json.dumps(result, indent=4))
    input("\nPress Enter to continue...")

def run_contextual_spoofing_defense_sim():
    """Simulates Contextual Spoofing Defense features."""
    print("\n--- Contextual Spoofing Defense (Simulated) ---")
    print("This section demonstrates techniques to defend against contextual spoofing attacks.")
    print("\n1. Data Augmentation (Simulated):")
    print("   - Simulates training with augmented data (e.g., varying lighting, blur, noise).")
    print("   - Result: Model robustness against environmental changes is improved.")
    print(f"   - Simulated Accuracy Improvement: {random.uniform(5.0, 15.0):.2f}%")

    print("\n2. Sensor Fusion (Simulated):")
    print("   - Simulates combining data from multiple sensors (e.g., RGB, IR, Depth, Audio).")
    print("   - For demonstration, we assume access to these modalities.")
    print("   - Result: Enhanced verification accuracy and spoof detection.")
    print(f"   - Simulated Fusion Score: {random.uniform(0.7, 0.95):.2f}")

    print("\n3. Temporal Consistency Checks (Simulated):")
    print("   - Simulates using RNN/LSTMs to model biometric sequences over time.")
    print("   - Detects inconsistencies in spoofed sequences (e.g., unnatural movements).")
    print("   - Result: Detection of dynamic adversarial inputs.")
    print(f"   - Simulated Consistency Score: {random.uniform(0.6, 0.9):.2f}")

    input("\nPress Enter to continue...")

def run_edge_ai_poisoning_defense_sim():
    """Simulates Edge AI Poisoning Defense features."""
    print("\n--- Edge AI Poisoning Defense (Simulated) ---")
    print("This section demonstrates techniques to defend against edge AI poisoning attacks.")

    print("\n1. Federated Learning with Differential Privacy (Simulated):")
    print("   - Simulates training models across edge devices without sharing raw data.")
    print("   - Adds noise to gradients to ensure privacy.")
    print("   - Result: Privacy-preserving and robust model updates.")
    print(f"   - Simulated Privacy Budget Used: {random.uniform(0.1, 1.0):.2f}")

    print("\n2. Model Integrity Checks (Simulated):")
    print("   - Simulates using hash-based verification to ensure model integrity.")
    print("   - Detects unauthorized modifications to the model.")
    print("   - Result: Tamper-proof model deployment.")
    print(f"   - Simulated Integrity Check Status: {'PASSED' if random.random() > 0.1 else 'FAILED'}")

    print("\n3. Poison Detection (Simulated):")
    print("   - Simulates detecting poisoned samples in training data.")
    print("   - Uses techniques like activation clustering or spectral signature analysis.")
    print("   - Result: Identification and mitigation of poisoned data.")
    print(f"   - Simulated Poisoned Samples Detected: {random.randint(0, 5)}")

    input("\nPress Enter to continue...")

def main():
    """Main function to run the interactive CLI."""
    while True:
        display_banner()
        display_menu()
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            run_test_adversarial()
        elif choice == '2':
            run_test_behavioral()
        elif choice == '3':
            run_full_authentication()
        elif choice == '4':
            run_contextual_spoofing_defense_sim()
        elif choice == '5':
            run_edge_ai_poisoning_defense_sim()
        elif choice == '6':
            print("Exiting CLI. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")
        
        print("\n") # Add a newline for better readability between operations

if __name__ == "__main__":
    main()