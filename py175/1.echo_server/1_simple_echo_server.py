"""
Simple Echo Server
https://launchschool.com/lessons/b42e8978/assignments/fcdeb69f
"""
import socket
import random

# create a TCP Server
#    AF_INET: Specifies the address family (IPv4 in this case)
#    SOCK_STREAM: Indicates that we are using a TCP socket, designed for continuous streams of data
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# We need to tell our server where to listen for requests. We'll use 'localhost' and port 3003 for this purpose. 
# In other words, we need to bind the server to an address.
server_socket.bind(('localhost', 3003))
server_socket.listen()

print("Server is running on localhost:3003")

# We want the server to run in an infinite loop, constantly listening for new connections. 
# accept method waits for a connection from a client, which is often a browser
# Once the connection is received, accept returns a tuple where the first value is a new socket object, 
# representing the connection and the second value is the address of the client. 
# Now we are not only listening for connections, but accepting them and capturing information about the connection.
while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")

    # With the connection established, we can read the incoming data
    # 1024 in this case, is the buffer size
    # decode method then converts those bytes to a string, as network data is transmitted in bytes.
    request = client_socket.recv(1024).decode()

    # skip empty requests and favicon icons
    if (not request) or ('favicon.ico' in request):
        client_socket.close()
        continue
    
    # grab the first line of the request, construct a valid HTTP response, and send it to the client
    request_line = request.splitlines()[0]
    
    # add roll to next line below request
    roll = random.randint(1, 6)
    response_body = f"{request_line}\n{roll}\n"


    response = ("HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                f"Content-Length: {len(response_body)}\r\n"
                "\r\n"
                f"{response_body}\n")

    # convert the response string to bytes for transmission
    client_socket.sendall(response.encode())

    # send the response to the client
    client_socket.close()       