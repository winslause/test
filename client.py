import socket
import threading
import ssl
import time
import logging
from typing import Optional
from configparser import ConfigParser

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='DEBUG: %(message)s')

# Read configuration
config = ConfigParser()
config.read('config.ini')
file_path = config.get('DEFAULT', 'linuxpath')
reread_on_query = config.getboolean('DEFAULT', 'REREAD_ON_QUERY', fallback=True)
ssl_enabled = config.getboolean('DEFAULT', 'SSL_ENABLED', fallback=False)
ssl_cert_path = config.get('DEFAULT', 'SSL_CERT_PATH', fallback='cert.pem')
ssl_key_path = config.get('DEFAULT', 'SSL_KEY_PATH', fallback='key.pem')

# Function to search for the string in the file
def search_string_in_file(query: str, file_path: str, reread: bool) -> bool:
    start_time = time.time()
    with open(file_path, 'r') as file:
        for line in file:
            if query == line.strip():
                logging.debug(f'Search execution time: {(time.time() - start_time) * 1000} ms')
                return True
    logging.debug(f'Search execution time: {(time.time() - start_time) * 1000} ms')
    return False

# Client handler function
def handle_client_connection(client_socket, client_address):
    with client_socket:
        while True:
            data = client_socket.recv(1024).rstrip(b'\x00').decode('utf-8')
            if not data:
                break
            query = data.strip()
            logging.debug(f'Query received from {client_address}: {query}')

            if reread_on_query:
                result = search_string_in_file(query, file_path, reread=True)
            else:
                result = search_string_in_file(query, file_path, reread=False)

            response = 'STRING EXISTS\n' if result else 'STRING NOT FOUND\n'
            client_socket.sendall(response.encode('utf-8'))

# Main server function
def start_server(host: str, port: int):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    logging.info(f'Server listening on {host}:{port}')

    while True:
        client_socket, client_address = server_socket.accept()
        if ssl_enabled:
            client_socket = ssl.wrap_socket(client_socket, server_side=True, certfile=ssl_cert_path, keyfile=ssl_key_path)
        client_thread = threading.Thread(target=handle_client_connection, args=(client_socket, client_address))
        client_thread.start()

# Run the server
if __name__ == '__main__':
    start_server('0.0.0.0', 65432)
