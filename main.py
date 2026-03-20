import socket
import threading
import sys
import os
import paramiko
import traceback
from honeypot import HoneypotSession

# Persistent host key - generates once, then reuses
HOST_KEY_FILE = "honeypot_host_key.pem"

def load_or_generate_host_key():
    """Load existing host key or generate a new one and save it."""
    if os.path.exists(HOST_KEY_FILE):
        print(f"[*] Loading existing host key from {HOST_KEY_FILE}")
        return paramiko.RSAKey.from_private_key_file(HOST_KEY_FILE)
    else:
        print(f"[*] Generating new host key and saving to {HOST_KEY_FILE}")
        key = paramiko.RSAKey.generate(2048)
        key.write_private_key_file(HOST_KEY_FILE)
        return key

HOST_KEY = load_or_generate_host_key()

class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        # Honeypot: Accept specific users or all?
        # Let's accept known users from our "spec" + root/admin
        if username in ["root", "admin", "devops", "backup", "postgres"]:
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        # Accept keys for simplicity in simulation
        return paramiko.AUTH_SUCCESSFUL

    def get_allowed_auths(self, username):
        return 'password,publickey'

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

def handle_connection(client, addr):
    print(f"[*] Connection from {addr[0]}:{addr[1]}")
    transport = paramiko.Transport(client)
    transport.add_server_key(HOST_KEY)
    server = Server()
    
    try:
        transport.start_server(server=server)
    except paramiko.SSHException:
        print("[-] SSH Negotiation failed.")
        return

    # Wait for auth
    chan = transport.accept(20)
    if chan is None:
        print("[-] Channel check failed.")
        return

    server.event.wait(10)
    if not server.event.is_set():
        print("[-] Client never requested a shell.")
        chan.close()
        return


    # Start Honeypot Session
    username = transport.get_username()
    session = HoneypotSession(client_ip=addr[0], username=username)

    chan.send(f"Welcome to Ubuntu 20.04.6 LTS (GNU/Linux 5.4.0-150-generic x86_64)\n\n")
    chan.send(f" * Documentation:  https://help.ubuntu.com\n")
    chan.send(f" * Management:     https://landscape.canonical.com\n")
    chan.send(f" * Support:        https://ubuntu.com/advantage\n\n")
    chan.send(f"Last login: {datetime.datetime.now().strftime('%a %b %d %H:%M:%S %Y')} from 192.168.1.55\n")
    
    try:
        while True:
            # Prompt
            prompt = f"{session.username}@prod-db-01:{session.cwd.replace('/home/' + session.username, '~')}$ "
            if session.username == "root":
                prompt = prompt.replace("$", "#")
            
            chan.send(prompt)
            
            # Read input (byte by byte to handle basic edits would be ideal, 
            # but for simplicity we rely on client line buffering or simple recv)
            # Paramiko recv usually gets chunks. A proper shell needs line buffering.
            
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                data = chan.recv(1024)
                if not data:
                    break
                # Handle backspace (simple)
                decoded = data.decode("utf-8", errors="ignore")
                if "\x7f" in decoded: # Backspace
                    cmd_buffer = cmd_buffer[:-1]
                    # Send backspace sequence to client to update their visual
                    chan.send("\b \b") 
                elif "\r" in decoded: # Enter
                    cmd_buffer += "\n"
                    chan.send("\r\n") # Echo newline
                else: 
                    cmd_buffer += decoded
                    chan.send(decoded) # Echo back
            
            if not cmd_buffer:
                break
                
            cmd_str = cmd_buffer.strip()
            if cmd_str == "exit":
                break
            
            # Execute
            output = session.handle_command(cmd_str)
            chan.send(output.replace("\n", "\r\n"))
            
    except Exception as e:
        print(f"[-] Session Error: {e}")
        traceback.print_exc()
    finally:
        # End session and save recording
        try:
            summary = session.end_session()
            print(f"[*] Session ended: {summary['session_id']}")
            print(f"    Commands: {summary['command_count']}, Skill: {summary['current_skill_level']}")
        except Exception as e:
            print(f"[-] Error saving session: {e}")
        chan.close()
        transport.close()

def main():
    # Listen on verified port 2222
    bind_ip = "0.0.0.0"
    bind_port = 2222

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((bind_ip, bind_port))
    sock.listen(100)
    
    print(f"[*] Listening on {bind_ip}:{bind_port}...")

    while True:
        try:
            client, addr = sock.accept()
            t = threading.Thread(target=handle_connection, args=(client, addr))
            t.start()
        except KeyboardInterrupt:
            print("\n[*] Shutting down...")
            break
        except Exception as e:
            print(f"[-] Accept Error: {e}")

if __name__ == "__main__":
    import datetime
    main()
