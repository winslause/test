import pytest
import socket
import threading
import ssl
import time

from server_script import start_server, handle_client_connection

# Mock configuration
file_path = 'test_file.txt'
reread_on_query = True
ssl_enabled = False

# Helper function to start the server in a separate thread
def start_test_server():
    server_thread = threading.Thread(target=start_server, args=('127.0.0.1', 65432))
    server_thread.daemon = True
    server_thread.start()
    time.sleep(1)  # Give the server some time to start

# Unit tests
def test_string_exists():
    with open(file_path, 'w') as f:
        f.write('test_string\n')

    start_test_server()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 65432))
    client_socket.sendall(b'test_string\x00')

    response = client_socket.recv(1024).decode('utf-8')
    assert response == 'STRING EXISTS\n'

def test_string_not_found():
    with open(file_path, 'w') as f:
        f.write('another_string\n')

    start_test_server()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 65432))
    client_socket.sendall(b'test_string\x00')

    response = client_socket.recv(1024).decode('utf-8')
    assert response == 'STRING NOT FOUND\n'

# Add more tests for different edge cases and configurations
