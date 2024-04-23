import socket
import json

HOST = '127.0.0.1'  # Localhost
PORT = 65432        # Port to listen on
DATA_FILE = 'data.json'  # File to store data

#Function to read data from file
def read_data():
    try:
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

#Function to write data to file
def write_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)

def handle_client_connection(conn, addr):
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            command = data.decode().strip()
            response = execute_command(command)
            conn.sendall(response.encode())

#Function to process client command
def execute_command(command):
    try:
        print("Received command:", command)
        parts = command.split('"')
        print("Split parts:", parts)
        action = parts[0].strip()
        attribute = parts[1].strip()
        name = parts[2].strip()
        data = read_data()
        if action == "Read":
            if name in data:
                return data[name].get(attribute, "Attribute not found")
            else:
                return "Person not found"
        elif action == "Write":
            value = parts[-1].strip() if len(parts) > 3 else ""
            if name not in data:
                data[name] = {}
            data[name][attribute] = value
            write_data(data)  # Write the updated data to the file
            return "Attribute successfully written"
        else:
            return "Invalid command"
    except Exception as e:
        return str(e)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print('Server listening on', (HOST, PORT))
        while True:
            conn, addr = s.accept()
            handle_client_connection(conn, addr)

if __name__ == "__main__":
    main()

