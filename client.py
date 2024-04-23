import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            command = input("Enter command (e.g., 'Read \"Person Name\" \"Attribute\"'): ")
            s.sendall(command.encode())
            response = s.recv(1024)
            print("Response:", response.decode())

if __name__ == "__main__":
    main()
