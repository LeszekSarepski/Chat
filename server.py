import socket
import threading
import hashlib
import os

# Ustawienia serwera
HOST = '127.0.0.1'
PORT = 12346

clients = {}
files = {}  # słownik przechowujący pliki: {nazwa_pliku: (owner, ścieżka)}


def calculate_md5(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
    return md5_hash.hexdigest()


def broadcast(message, sender_client=None):
    for client in clients:
        if client != sender_client:
            client.send(message.encode('utf-8'))


def handle_client(client):
    nickname = clients[client]
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message.startswith('/sendfile'):
                file_name = message.split()[1]
                file_size = int(client.recv(1024).decode('utf-8'))
                file_data = client.recv(file_size)
                md5_sent = client.recv(1024).decode('utf-8')

                file_path = os.path.join("server_files", file_name)
                with open(file_path, 'wb') as f:
                    f.write(file_data)

                md5_received = calculate_md5(file_path)

                if md5_sent == md5_received:
                    files[file_name] = (client, file_path)
                    client.send('File transfer successful and verified!'.encode('utf-8'))
                else:
                    client.send('File transfer failed: MD5 mismatch.'.encode('utf-8'))
            elif message.startswith('/getfile'):
                file_name = message.split()[1]
                if file_name in files:
                    owner, file_path = files[file_name]
                    with open(file_path, 'rb') as f:
                        file_data = f.read()

                    file_size = os.path.getsize(file_path)
                    md5_hash = calculate_md5(file_path)

                    client.send(f'/sendfile {file_name}'.encode('utf-8'))
                    client.send(str(file_size).encode('utf-8'))
                    client.send(file_data)
                    client.send(md5_hash.encode('utf-8'))
                else:
                    client.send(f'File {file_name} not found.'.encode('utf-8'))
            else:
                broadcast(f'{nickname}: {message}', client)
        except Exception as e:
            print(f'Error handling client {nickname}: {e}')
            del clients[client]
            broadcast(f'{nickname} opuścił czat')
            client.close()
            break


def main():
    if not os.path.exists('server_files'):
        os.makedirs('server_files')

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f'Serwer uruchomiony na {HOST}:{PORT}')

    while True:
        client, address = server.accept()
        print(f'Połączono z {str(address)}')

        nickname = client.recv(1024).decode('utf-8')
        clients[client] = nickname

        print(f'Nick klienta: {nickname}')
        client.send(f'Połączono z serwerem jako {nickname}!'.encode('utf-8'))
        broadcast(f'{nickname} dołączył do czatu!', client)

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    main()