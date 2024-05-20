# -*- coding: utf-8 -*-
"""
Created on Sun Feb  8 12:13:26 2023

@author: JAWAD
"""
import socket


# Define storage servers
storage1 = ("127.0.0.1", 5001)
storage2 = ("127.0.0.1", 5002)
storage3 = ("127.0.0.1", 5003)

# Define main DNS server
dns_server = ("127.0.0.1", 5000)

# Define storage data
storage_data = {
    "01010101": b"hello",
    "11001100": b"world",
    "00110011": b"Jawad",
    "10101010": b"Sarah",
}


def handle_request(data):
    """
    Handle a DNS request and return the corresponding IP address.
    """
    # convert request to binary
    request_binary = ''.join([format(x, '08b') for x in data])

    # divide binary into two halves
    half_len = len(request_binary) // 2
    half1 = request_binary[:half_len]
    half2 = request_binary[half_len:]

    # XOR the two halves to create the third piece
    piece3 = bin(int(half1, 2) ^ int(half2, 2))[2:].zfill(half_len)

    # send requests to the three storage servers
    response1 = send_request(storage1, piece3)
    response2 = send_request(storage2, half1)
    response3 = send_request(storage3, half2)

    # combine responses
    response_binary = response1 + response2 + response3

    # convert response to IP address
    response = bytes([int(response_binary[i:i+8], 2) for i in range(0, len(response_binary), 8)])

    return response


def serve_dns(ip, port):
    """
    Start the DNS server on the specified IP address and port.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((ip, port))

        print(f"DNS server listening on {ip}:{port}...")

        while True:
            # receive request
            data, address = server_socket.recvfrom(1024)

            # handle request
            response = handle_request(data)

            # send response
            server_socket.sendto(response, address)




def send_request(address, data):
    """
    Send a request to the specified DNS server and return the response.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.settimeout(5)  # set timeout to 5 seconds
        client_socket.sendto(data.encode(), address)

        try:
            response, _ = client_socket.recvfrom(1024)
        except socket.timeout:
            response = b""

    return response

def serve_storage(ip, port):
    """
    Start the storage server on the specified IP address and port.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((ip, port))

        print(f"Storage server listening on {ip}:{port}...")

        while True:
            # receive request
            data, address = server_socket.recvfrom(1024)

            # handle request
            response = handle_storage_request(data)

            # send response
            server_socket.sendto(response, address)


def handle_storage_request(data):
    """
    Handle a storage request and return the corresponding data.
    """
    # convert request to binary
    request_binary = ''.join([format(x, '08b') for x in data])

    # look up data in storage
    if request_binary in storage_data:
        response = storage_data[request_binary]
    else:
        response = b""

    return response


def test_functionality():
    # Define DNS request
    request = b"Jawad"

    # Send DNS request and receive response
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
        client_socket.settimeout(5)  # set timeout to 5 seconds
        client_socket.sendto(request, dns_server)

        try:
            response, _ = client_socket.recvfrom(1024)
        except socket.timeout:
            response = b""

    # Check if response is correct
    expected_response = b"Jawad"
    assert response == expected_response, f"Expected {expected_response}, but received {response}"

    # Print test result
    if response == expected_response:
        print("Test successful")
    else:
        print("Test failed")
        
        
test_functionality()