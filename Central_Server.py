import socket

def udp_server(host='0.0.0.0', port=5005):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind the socket to the server address
    server_address = (host, port)
    print(f'Starting UDP server on {host}:{port}')
    sock.bind(server_address)
    
    try:
        while True:
            print('Waiting to receive message...')
            data, address = sock.recvfrom(4096)  # Buffer size is 4096 bytes
            
            print(f'Received {len(data)} bytes from {address}')
            print(data.decode())  # Assuming data is in UTF-8 format
    except KeyboardInterrupt:
        print('Exiting the server.')
    finally:
        sock.close()

if __name__ == "__main__":
    udp_server()


