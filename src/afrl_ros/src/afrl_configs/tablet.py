import socket

def start_server(ip_address, port):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the IP address and port
    server_socket.bind((ip_address, port))
    
    # Listen for incoming connections with a maximum backlog of 5
    server_socket.listen(5)
    
    print(f"Server is listening on {ip_address}:{port}...")
    
    while True:
        # Accept an incoming connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}.")

        # Read data from the client
        data = client_socket.recv(1024).decode("utf-8")
        print(f"Received data: {data}")
        
        # Send a response to the client
        response = f"Hello, {client_address}. You sent: {data}"
        client_socket.send(response.encode("utf-8"))
        
        # Close the client socket
        client_socket.close()



if __name__ == "__main__":
    ip_address = "192.168.1.123"  # Change this to the desired IP address
    port = 8000  # Change this to the desired port
    start_server(ip_address, port)
