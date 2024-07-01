import socket
import threading
import hashlib
import os
from cryptography.fernet import Fernet

HOST = '127.0.0.1'
PORT = 12346

# Wczytywanie klucza szyfrowania
with open("secret.key", "rb") as key_file:
    secret_key = key_file.read()

cipher_suite = Fernet(secret_key)

def calculate_md5(file_path):
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            md5_hash.update(byte_block)
    return md5_hash.hexdigest()

def receive_messages(client):
    while True:
        try:
            encrypted_message = client.recv(1024)
            message = cipher_suite.decrypt(encrypted_message).decode('utf-8')
            if message.startswith('/sendfile'):
                file_name = message.split()[1]
                file_size = int(client.recv(1024).decode('utf-8'))
                file_data = client.recv(file_size)
                md5_received = client.recv(1024).decode('utf-8')

                file_path = os.path.join("client_files", file_name)
                with open(file_path, 'wb') as f:
                    f.write(file_data)

                md5_calculated = calculate_md5(file_path)

                if md5_received == md5_calculated:
                    print(f'File {file_name} received successfully and verified!')
                else:
                    print(f'File {file_name} transfer failed: MD5 mismatch.')
            else:
                print(message)
        except Exception as e:
            print(f'Błąd odbierania wiadomości: {e}')
            client.close()
            break

def send_messages(client):
    while True:
        try:
            message = input()
            if message.startswith('/sendfile'):
                file_path = message.split()[1]
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    md5_hash = calculate_md5(file_path)

                    client.send(cipher_suite.encrypt(f'/sendfile {os.path.basename(file_path)}'.encode('utf-8')))
                    client.send(str(file_size).encode('utf-8'))

                    with open(file_path, 'rb') as f:
                        client.send(f.read())

                    client.send(md5_hash.encode('utf-8'))
                else:
                    print('Plik nie istnieje!')
            elif message.startswith('/getfile'):
                file_name = message.split()[1]
                client.send(cipher_suite.encrypt(f'/getfile {file_name}'.encode('utf-8')))
            else:
                client.send(cipher_suite.encrypt(message.encode('utf-8')))
        except Exception as e:
            print(f'Błąd wysyłania wiadomości: {e}')
            client.close()
            break

def main():
    if not os.path.exists('client_files'):
        os.makedirs('client_files')

    nickname = input('Podaj swój nick: ')

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        client.send(nickname.encode('utf-8'))

        receive_thread = threading.Thread(target=receive_messages, args=(client,))
        receive_thread.start()

        send_thread = threading.Thread(target=send_messages, args=(client,))
        send_thread.start()
    except Exception as e:
        print(f'Błąd połączenia z serwerem: {e}')

if __name__ == "__main__":
    main()
