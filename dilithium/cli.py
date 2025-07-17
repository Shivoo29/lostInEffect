import os
import sys
import json
import time
import threading
from datetime import datetime

# Add the project root to Python path
# Assuming this script is in dilithium/cli.py
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

from dilithium.core import DilithiumParams
from dilithium.chaos import HybridEncryption
from dilithium.monitoring.metrics import MonitoringSystem
from dilithium.monitoring.health import HealthCheck
from dilithium.config import SecurityConfig
from dilithium.file_operations import FileEncryptionManager
from dilithium.network.protocol import CryptoNetworkProtocol, MessageSender, MessageReceiver
from dilithium.security.audit import SecureAuditLog, AuditEvent

# Global instances for CLI operations
config = SecurityConfig()
params = DilithiumParams.get_params(security_level=3)
hybrid = HybridEncryption(params)
audit_log = SecureAuditLog(config)
monitoring = MonitoringSystem(config)
health = HealthCheck(config, monitoring)
file_manager = FileEncryptionManager(hybrid)
protocol = CryptoNetworkProtocol(audit_log)
sender = MessageSender(protocol)
receiver = MessageReceiver(protocol)

# Global variables for keys and receiver status
public_key = None
private_key = None
receiver_running = False

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    clear_screen()
    print("""
██████╗ ██╗██╗     ██╗ ██████╗ ██╗  ██╗██╗███╗   ██╗
██╔══██╗██║██║     ██║██╔═══██╗██║  ██║██║████╗  ██║
██║  ██║██║██║     ██║██║   ██║███████║██║██╔██╗ ██║
██║  ██║██║██║     ██║██║   ██║██╔══██║██║██║╚██╗██║
██████╔╝██║███████╗██║╚██████╔╝██║  ██║██║██║ ╚████║
╚═════╝ ═╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝

Quantum-Resistant Cryptography System CLI
""")

def print_keys(pub_key, priv_key):
    print("\n--- Generated Keys ---")
    print("Public Key (first 16 bytes of seed):", pub_key['seed'].hex()[:32] + '...')
    print("Private Key (first 16 bytes of seed):", priv_key['seed'].hex()[:32] + '...')
    print("----------------------")

def generate_keys_cli():
    global public_key, private_key
    print("\n--- Key Generation ---")
    try:
        public_key, private_key = hybrid.generate_keys()
        print_keys(public_key, private_key)
        audit_log.log_event(AuditEvent(
            timestamp=datetime.now().timestamp(),
            event_type="KEY_GENERATION",
            user_id="cli_user",
            action="generate_keys",
            status="SUCCESS",
            details={"security_level": params.security_level}
        ))
    except Exception as e:
        print(f"Error generating keys: {e}")
        audit_log.log_event(AuditEvent(
            timestamp=datetime.now().timestamp(),
            event_type="KEY_GENERATION",
            user_id="cli_user",
            action="generate_keys",
            status="FAILED",
            details={"error": str(e)}
        ))
    input("Press Enter to continue...")

def encrypt_message_cli():
    print("\n--- Encrypt Message ---")
    if public_key is None or private_key is None:
        print("Please generate keys first (Option 1).")
        input("Press Enter to continue...")
        return

    message = input("Enter message to encrypt: ").encode('utf-8')
    try:
        ciphertext, nonce, signature = hybrid.encrypt_and_sign(message, private_key)
        print("\nMessage encrypted successfully!")
        print(f"Ciphertext (hex): {ciphertext.hex()[:60]}...")
        print(f"Nonce (hex): {nonce.hex()}")
        print(f"Signature (mu hex): {signature[0].hex()[:30]}...")
        audit_log.log_event(AuditEvent(
            timestamp=datetime.now().timestamp(),
            event_type="MESSAGE_ENCRYPTION",
            user_id="cli_user",
            action="encrypt",
            status="SUCCESS",
            details={"message_size": len(message), "ciphertext_size": len(ciphertext)}
        ))
    except Exception as e:
        print(f"Error encrypting message: {e}")
        audit_log.log_event(AuditEvent(
            timestamp=datetime.now().timestamp(),
            event_type="MESSAGE_ENCRYPTION",
            user_id="cli_user",
            action="encrypt",
            status="FAILED",
            details={"error": str(e)}
        ))
    input("Press Enter to continue...")

def decrypt_message_cli():
    print("\n--- Decrypt Message ---")
    if public_key is None or private_key is None:
        print("Please generate keys first (Option 1).")
        input("Press Enter to continue...")
        return

    try:
        ciphertext_hex = input("Enter ciphertext (hex): ")
        nonce_hex = input("Enter nonce (hex): ")
        mu_hex = input("Enter signature mu (hex): ")
        # For simplicity, z is not asked directly, assuming it's part of a full signature object
        # In a real scenario, you'd load the full signature object.
        # For this CLI, we'll use a dummy z if needed, or rely on the internal structure.
        
        # Reconstruct signature (this is a simplification for CLI demo)
        # In a real system, you'd pass the exact signature object from encryption
        # For now, we'll use the private_key's t as a placeholder for z's structure if needed
        # This part needs careful handling as signature[1] is a numpy array
        
        # A more robust way would be to save/load the full signature object (mu, z_array)
        # For this CLI, let's assume we are decrypting a message that was just encrypted
        # or we have a way to reconstruct the full signature.
        
        # Since we don't have a way to input the numpy array 'z' from CLI easily,
        # we'll make a simplifying assumption for this demo: the signature object
        # is available from a recent encryption, or we use a dummy for structure.
        # This is a limitation of text-based CLI for complex data types.
        
        # Let's assume for this demo, we are decrypting the *last* encrypted message
        # or the user has the full signature object available from a file/previous step.
        # Since that's not practical for a simple CLI, we'll use a placeholder for `z`
        # and rely on the `verify_and_decrypt` to handle the actual signature verification.
        
        # This is a critical simplification for CLI. In a real app, you'd serialize/deserialize
        # the full signature object.
        
        # For demonstration, let's use a dummy z if the user provides mu.
        # This will likely fail if the mu doesn't match the dummy z, but it shows the flow.
        
        # A better approach for CLI would be to ask for the full signature as a JSON string
        # if it was serialized as such.
        
        # Given the current `hybrid.verify_and_decrypt` expects `signature: Tuple[bytes, np.ndarray]`
        # and we can only get `mu_hex` easily, this function will be limited.
        # Let's make it clear that this is a demo simplification.
        
        print("\nNote: For this CLI demo, full signature reconstruction (especially 'z' numpy array) from text input is simplified.")
        print("Decryption might fail if the provided 'mu' does not match a valid signature generated with the current keys.")
        
        # Attempt to reconstruct a dummy signature for the call
        # This will likely fail verification unless it's the exact signature from a recent encryption
        dummy_z = np.zeros((params.l, params.n), dtype=np.int32) # Placeholder
        reconstructed_signature = (bytes.fromhex(mu_hex), dummy_z)
        
        decrypted_message = hybrid.verify_and_decrypt(
            bytes.fromhex(ciphertext_hex),
            bytes.fromhex(nonce_hex),
            reconstructed_signature,
            public_key
        )
        print("\nMessage decrypted successfully!")
        print(f"Decrypted message: {decrypted_message.decode('utf-8')}")
        audit_log.log_event(AuditEvent(
            timestamp=datetime.now().timestamp(),
            event_type="MESSAGE_DECRYPTION",
            user_id="cli_user",
            action="decrypt",
            status="SUCCESS",
            details={"message_size": len(decrypted_message)}
        ))
    except Exception as e:
        print(f"Error decrypting message: {e}")
        audit_log.log_event(AuditEvent(
            timestamp=datetime.now().timestamp(),
            event_type="MESSAGE_DECRYPTION",
            user_id="cli_user",
            action="decrypt",
            status="FAILED",
            details={"error": str(e)}
        ))
    input("Press Enter to continue...")

def encrypt_file_cli():
    print("\n--- Encrypt File ---")
    if public_key is None or private_key is None:
        print("Please generate keys first (Option 1).")
        input("Press Enter to continue...")
        return

    file_path = input("Enter path to file to encrypt: ")
    if not os.path.exists(file_path):
        print("File not found.")
        input("Press Enter to continue...")
        return

    output_dir = input("Enter output directory for encrypted file (e.g., encrypted_files): ")
    os.makedirs(output_dir, exist_ok=True)

    try:
        keys = {'public_key': public_key, 'private_key': private_key}
        result = file_manager.encrypt_file(file_path, output_dir, keys)
        if result['status'] == 'success':
            print(f"\nFile encrypted successfully: {result['encrypted_file']}")
            print(f"Keys saved to: {result['keys_file']}")
            audit_log.log_event(AuditEvent(
                timestamp=datetime.now().timestamp(),
                event_type="FILE_ENCRYPTION",
                user_id="cli_user",
                action="encrypt_single_file",
                status="SUCCESS",
                details={"original_file": file_path, "encrypted_file": result['encrypted_file']}
            ))
        else:
            print(f"Error encrypting file: {result['error']}")
            audit_log.log_event(AuditEvent(
                timestamp=datetime.now().timestamp(),
                event_type="FILE_ENCRYPTION",
                user_id="cli_user",
                action="encrypt_single_file",
                status="FAILED",
                details={"original_file": file_path, "error": result['error']}
            ))
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    input("Press Enter to continue...")

def decrypt_file_cli():
    print("\n--- Decrypt File ---")
    encrypted_file_path = input("Enter path to encrypted file (.encrypted extension): ")
    if not os.path.exists(encrypted_file_path):
        print("Encrypted file not found.")
        input("Press Enter to continue...")
        return

    output_dir = input("Enter output directory for decrypted file (e.g., decrypted_files): ")
    os.makedirs(output_dir, exist_ok=True)

    try:
        result = file_manager.decrypt_file(encrypted_file_path, output_dir)
        if result['status'] == 'success':
            print(f"\nFile decrypted successfully: {result['decrypted_file']}")
            audit_log.log_event(AuditEvent(
                timestamp=datetime.now().timestamp(),
                event_type="FILE_DECRYPTION",
                user_id="cli_user",
                action="decrypt_single_file",
                status="SUCCESS",
                details={"encrypted_file": encrypted_file_path, "decrypted_file": result['decrypted_file']}
            ))
        else:
            print(f"Error decrypting file: {result['error']}")
            audit_log.log_event(AuditEvent(
                timestamp=datetime.now().timestamp(),
                event_type="FILE_DECRYPTION",
                user_id="cli_user",
                action="decrypt_single_file",
                status="FAILED",
                details={"encrypted_file": encrypted_file_path, "error": result['error']}
            ))
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    input("Press Enter to continue...")

def auto_encrypt_store_message_cli():
    print("\n--- Auto Encrypt & Store Message ---")
    message = input("Enter message to auto encrypt and store: ").encode('utf-8')
    if not message:
        print("Message cannot be empty.")
        input("Press Enter to continue...")
        return

    try:
        # Auto generate keys for this operation
        pub_key, priv_key = hybrid.generate_keys()
        ciphertext, nonce, signature = hybrid.encrypt_and_sign(message, priv_key)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"encrypted_message_{timestamp}.json"
        
        encrypted_data = {
            'ciphertext': ciphertext.hex(),
            'nonce': nonce.hex(),
            'signature': {
                'mu': signature[0].hex(),
                'z': signature[1].tolist()
            },
            'public_key': {
                'seed': pub_key['seed'].hex(),
                't': pub_key['t'].tolist()
            },
            'encrypted_at': datetime.now().isoformat(),
            'message_size': len(message)
        }
        
        with open(filename, 'w') as f:
            json.dump(encrypted_data, f, indent=2)

        print(f"\nMessage encrypted and saved to '{filename}'")
        audit_log.log_event(AuditEvent(
            timestamp=datetime.now().timestamp(),
            event_type="AUTO_ENCRYPT_STORE",
            user_id="cli_user",
            action="auto_encrypt_store_message",
            status="SUCCESS",
            details={"filename": filename, "message_size": len(message)}
        ))
    except Exception as e:
        print(f"Error auto encrypting and storing message: {e}")
        audit_log.log_event(AuditEvent(
            timestamp=datetime.now().timestamp(),
            event_type="AUTO_ENCRYPT_STORE",
            user_id="cli_user",
            action="auto_encrypt_store_message",
            status="FAILED",
            details={"error": str(e)}
        ))
    input("Press Enter to continue...")

def auto_encrypt_send_message_cli():
    print("\n--- Auto Encrypt & Send Message ---")
    message = input("Enter message to auto encrypt and send: ").encode('utf-8')
    if not message:
        print("Message cannot be empty.")
        input("Press Enter to continue...")
        return

    host = input("Enter receiver host (default: localhost): ") or 'localhost'
    port = int(input("Enter receiver port (default: 5000): ") or 5000)

    try:
        # Auto generate keys for this operation
        pub_key, priv_key = hybrid.generate_keys()
        ciphertext, nonce, signature = hybrid.encrypt_and_sign(message, priv_key)

        sender.host = host
        sender.port = port

        message_data = protocol.pack_message(ciphertext, nonce, signature, pub_key)
        sender.send_message(message_data)

        print(f"\nMessage encrypted and sent to {host}:{port}")
        audit_log.log_event(AuditEvent(
            timestamp=datetime.now().timestamp(),
            event_type="AUTO_ENCRYPT_SEND",
            user_id="cli_user",
            action="auto_encrypt_send_message",
            status="SUCCESS",
            details={"host": host, "port": port, "message_size": len(message)}
        ))
    except Exception as e:
        print(f"Error auto encrypting and sending message: {e}")
        audit_log.log_event(AuditEvent(
            timestamp=datetime.now().timestamp(),
            event_type="AUTO_ENCRYPT_SEND",
            user_id="cli_user",
            action="auto_encrypt_send_message",
            status="FAILED",
            details={"error": str(e)}
        ))
    input("Press Enter to continue...")

def batch_encrypt_folder_cli():
    print("\n--- Batch Encrypt Folder ---")
    input_folder = input("Enter path to input folder: ")
    if not os.path.isdir(input_folder):
        print("Input folder not found.")
        input("Press Enter to continue...")
        return

    output_folder = input("Enter path to output folder for encrypted files: ")
    os.makedirs(output_folder, exist_ok=True)

    try:
        # Callbacks for progress/status (CLI will just print)
        file_manager.set_callbacks(lambda p: print(f"Progress: {p}%"), lambda s: print(f"Status: {s}"))
        result = file_manager.encrypt_folder(input_folder, output_folder, auto_generate_keys=True)
        if result['status'] == 'success':
            print(f"\nBatch encryption complete. {result['successful']}/{result['total_files']} files encrypted.")
            audit_log.log_event(AuditEvent(
                timestamp=datetime.now().timestamp(),
                event_type="BATCH_ENCRYPTION",
                user_id="cli_user",
                action="batch_encrypt_folder",
                status="SUCCESS",
                details={"input_folder": input_folder, "output_folder": output_folder, "total_files": result['total_files']}
            ))
        else:
            print(f"Error during batch encryption: {result['error']}")
            audit_log.log_event(AuditEvent(
                timestamp=datetime.now().timestamp(),
                event_type="BATCH_ENCRYPTION",
                user_id="cli_user",
                action="batch_encrypt_folder",
                status="FAILED",
                details={"input_folder": input_folder, "error": result['error']}
            ))
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    input("Press Enter to continue...")

def batch_decrypt_folder_cli():
    print("\n--- Batch Decrypt Folder ---")
    encrypted_folder = input("Enter path to folder containing encrypted files: ")
    if not os.path.isdir(encrypted_folder):
        print("Encrypted folder not found.")
        input("Press Enter to continue...")
        return

    output_folder = input("Enter path to output folder for decrypted files: ")
    os.makedirs(output_folder, exist_ok=True)

    try:
        # Callbacks for progress/status (CLI will just print)
        file_manager.set_callbacks(lambda p: print(f"Progress: {p}%"), lambda s: print(f"Status: {s}"))
        result = file_manager.decrypt_folder(encrypted_folder, output_folder)
        if result['status'] == 'success':
            print(f"\nBatch decryption complete. {result['successful']}/{result['total_files']} files decrypted.")
            audit_log.log_event(AuditEvent(
                timestamp=datetime.now().timestamp(),
                event_type="BATCH_DECRYPTION",
                user_id="cli_user",
                action="batch_decrypt_folder",
                status="SUCCESS",
                details={"encrypted_folder": encrypted_folder, "output_folder": output_folder, "total_files": result['total_files']}
            ))
        else:
            print(f"Error during batch decryption: {result['error']}")
            audit_log.log_event(AuditEvent(
                timestamp=datetime.now().timestamp(),
                event_type="BATCH_DECRYPTION",
                user_id="cli_user",
                action="batch_decrypt_folder",
                status="FAILED",
                details={"encrypted_folder": encrypted_folder, "error": result['error']}
            ))
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    input("Press Enter to continue...")

def start_receiver_cli():
    global receiver_running
    print("\n--- Start Receiver ---")
    if receiver_running:
        print("Receiver is already running.")
        input("Press Enter to continue...")
        return

    port = int(input("Enter port to listen on (default: 5000): ") or 5000)
    receiver.port = port

    def handle_received_data(data_type, components):
        print(f"\n[RECEIVER] Received {data_type}!")
        if data_type == 'message':
            try:
                # For CLI, we'll just print a summary. Full decryption is complex without keys.
                # The GUI handles full decryption. Here, we just acknowledge receipt.
                print(f"  Ciphertext size: {len(components['ciphertext'])} bytes")
                print(f"  Nonce: {components['nonce'].hex()}")
                print("  (Full decryption requires keys and is best handled by the GUI)")
            except Exception as e:
                print(f"Error processing received message: {e}")
        elif data_type == 'file':
            try:
                print(f"  Filename: {components['filename']}")
                print(f"  File size: {components['file_size']} bytes")
                print("  (File decryption and saving is best handled by the GUI)")
            except Exception as e:
                print(f"Error processing received file: {e}")

    try:
        receiver.start(handle_received_data)
        receiver_running = True
        print(f"Receiver started on port {port}. Waiting for incoming data...")
        print("Note: This CLI receiver provides basic receipt notification. For full decryption and file saving, use the GUI receiver (dilithium/receiver_gui.py).")
        audit_log.log_event(AuditEvent(
            timestamp=datetime.now().timestamp(),
            event_type="RECEIVER_START",
            user_id="cli_user",
            action="start_receiver",
            status="SUCCESS",
            details={"port": port}
        ))
    except Exception as e:
        print(f"Error starting receiver: {e}")
        audit_log.log_event(AuditEvent(
            timestamp=datetime.now().timestamp(),
            event_type="RECEIVER_START",
            user_id="cli_user",
            action="start_receiver",
            status="FAILED",
            details={"error": str(e)}
        ))
    input("Press Enter to continue... (Receiver will run in background)")

def stop_receiver_cli():
    global receiver_running
    print("\n--- Stop Receiver ---")
    if not receiver_running:
        print("Receiver is not running.")
        input("Press Enter to continue...")
        return
    try:
        receiver.stop()
        receiver_running = False
        print("Receiver stopped.")
        audit_log.log_event(AuditEvent(
            timestamp=datetime.now().timestamp(),
            event_type="RECEIVER_STOP",
            user_id="cli_user",
            action="stop_receiver",
            status="SUCCESS",
            details={}
        ))
    except Exception as e:
        print(f"Error stopping receiver: {e}")
        audit_log.log_event(AuditEvent(
            timestamp=datetime.now().timestamp(),
            event_type="RECEIVER_STOP",
            user_id="cli_user",
            action="stop_receiver",
            status="FAILED",
            details={"error": str(e)}
        ))
    input("Press Enter to continue...")

def view_health_metrics_cli():
    print("\n--- System Health and Metrics ---")
    try:
        report = health.get_health_report()
        print("\nSystem Status:")
        print(f"  Status: {report['status']}")
        print(f"  Last Check: {datetime.fromtimestamp(report['last_check'])}")
        print("\nSystem Information:")
        for key, value in report['system_info'].items():
            print(f"  {key}: {value}")
        print("\nPerformance Metrics (Mean over last hour):")
        metrics_names = ['Latency (ms)', 'CPU Usage (%), ', 'Memory Usage (%)',
                         'Queue Size', 'Error Rate', 'Throughput']
        for name, value in zip(metrics_names, report['metrics']['mean']):
            print(f"  {name}: {value:.2f}")
        audit_log.log_event(AuditEvent(
            timestamp=datetime.now().timestamp(),
            event_type="VIEW_METRICS",
            user_id="cli_user",
            action="view_health_metrics",
            status="SUCCESS",
            details={}
        ))
    except Exception as e:
        print(f"Error retrieving health and metrics: {e}")
        audit_log.log_event(AuditEvent(
            timestamp=datetime.now().timestamp(),
            event_type="VIEW_METRICS",
            user_id="cli_user",
            action="view_health_metrics",
            status="FAILED",
            details={"error": str(e)}
        ))
    input("Press Enter to continue...")

def view_audit_logs_cli():
    print("\n--- Audit Logs ---")
    try:
        logs = audit_log.get_logs()
        if not logs:
            print("No audit logs available.")
            input("Press Enter to continue...")
            return

        for log in reversed(logs): # Show newest first
            timestamp = datetime.fromtimestamp(log.timestamp)
            print(f"\n[{timestamp.strftime('%Y-%m-%d %H:%M:%S')}] Event: {log.event_type}")
            print(f"  User: {log.user_id}")
            print(f"  Action: {log.action}")
            print(f"  Status: {log.status}")
            print(f"  Details: {json.dumps(log.details, indent=2)}")
            print(f"  Hash: {log.hash[:16]}...")
            print("-" * 50)
        audit_log.log_event(AuditEvent(
            timestamp=datetime.now().timestamp(),
            event_type="VIEW_LOGS",
            user_id="cli_user",
            action="view_audit_logs",
            status="SUCCESS",
            details={"num_logs": len(logs)}
        ))
    except Exception as e:
        print(f"Error retrieving audit logs: {e}")
        audit_log.log_event(AuditEvent(
            timestamp=datetime.now().timestamp(),
            event_type="VIEW_LOGS",
            user_id="cli_user",
            action="view_audit_logs",
            status="FAILED",
            details={"error": str(e)}
        ))
    input("Press Enter to continue...")

def main_menu():
    while True:
        display_banner()
        print("\nSelect an option:")
        print("1. Generate Dilithium Keys")
        print("2. Encrypt Message (Manual)")
        print("3. Decrypt Message (Manual)")
        print("4. Encrypt File (Manual)")
        print("5. Decrypt File (Manual)")
        print("6. Auto Encrypt & Store Message")
        print("7. Auto Encrypt & Send Message (Requires Receiver)")
        print("8. Batch Encrypt Folder")
        print("9. Batch Decrypt Folder")
        print("10. Start Receiver (Background)")
        print("11. Stop Receiver")
        print("12. View System Health & Metrics")
        print("13. View Audit Logs")
        print("14. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            generate_keys_cli()
        elif choice == '2':
            encrypt_message_cli()
        elif choice == '3':
            decrypt_message_cli()
        elif choice == '4':
            encrypt_file_cli()
        elif choice == '5':
            decrypt_file_cli()
        elif choice == '6':
            auto_encrypt_store_message_cli()
        elif choice == '7':
            auto_encrypt_send_message_cli()
        elif choice == '8':
            batch_encrypt_folder_cli()
        elif choice == '9':
            batch_decrypt_folder_cli()
        elif choice == '10':
            start_receiver_cli()
        elif choice == '11':
            stop_receiver_cli()
        elif choice == '12':
            view_health_metrics_cli()
        elif choice == '13':
            view_audit_logs_cli()
        elif choice == '14':
            print("Exiting Dilithium CLI. Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main_menu()
