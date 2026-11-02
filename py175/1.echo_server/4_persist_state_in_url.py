# https://launchschool.com/lessons/b42e8978/assignments/c64068b8

import socket
import random

PORT = 3004
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', PORT))
server_socket.listen()

print(f"Server is running on localhost:{PORT}")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")

    request = client_socket.recv(1024).decode()
    if not request or 'favicon.ico' in request:
        client_socket.close()
        continue

    request_line = request.splitlines()[0]
    http_method, path_and_params, _ = request_line.split(" ")
    if '?' in path_and_params:
        path, params = path_and_params.split("?")
    else:
        path = path_and_params
        params = 'number=0'

    params = params.split("&")
    params_dict = {}
    for param in params:
        key, value = param.split("=")
        params_dict[key] = value
    
    number = int(params_dict.get('number', 0))

    response_body = ("<html><head><title>Counter</title></head><body>"
                     f"<h1>HTTP Request Information:</h1>"
                     f"<p><strong>Request Line:</strong> {request_line}</p>"
                     f"<p><strong>HTTP Method:</strong> {http_method}</p>"
                     f"<p><strong>Path:</strong> {path}</p>"
                     f"<p><strong>Parameters:</strong> {params_dict}</p>"
                     "<h2>Counter:</h2>"
                     f"<p style='color: red;'>The current number is: {number}</p>"
                     f"<p><a href='?number={number + 1}'>Add one</a>"
                     f"&nbsp;&nbsp;"    # adds 2 special spaces that prevents words from wrapping to new lines (treat multiple words as 1 word)
                     f"<a href='?number={number - 1}'>Subtract one</a></p>"
                     "</body></html>")

    response = ("HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                f"Content-Length: {len(response_body)}\r\n"
                "\r\n"
                f"{response_body}")

    client_socket.sendall(response.encode())
    client_socket.close()
    