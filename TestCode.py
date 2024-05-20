# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 12:32:04 2023

@author: JAWAD
"""

import socket

# Define DNS server
dns_server = ("127.0.0.1", 5000)

# Define DNS requests
requests = [
    b"hello",
    b"world",
    b"foo",
    b"bar",
]

# Send DNS requests and print responses
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
    for request in requests:
        client_socket.sendto(request, dns_server)
        response, _ = client_socket.recvfrom(1024)
        print(f"Request: {request.decode()} Response: {response.decode()}")
        