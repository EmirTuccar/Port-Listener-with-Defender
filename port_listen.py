import socket
import os
import subprocess
import threading
import time

def modify_firewall(action):
    command = ["sudo", "iptables", "-I", "INPUT", "-p", "tcp", "--dport", "12345", "-j", action]
    subprocess.run(command, check=True)

password = 1

def controller():
    global password
    if password == 1:
        modify_firewall("ACCEPT")
    elif password == 0:
        modify_firewall("DROP")

def start_listener(host, port):
    print("-----------------------------------------------------------")
    
    listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        
        listener_socket.bind((host, port))
        listener_socket.listen(1)
        print(f"Listening on {host}:{port}")
        
        while True:
            controller()
            client_socket, client_address = listener_socket.accept()

            if client_address[0] == "192.168.56.101":
                modify_firewall("ACCEPT")

            # Handle each client in a separate thread
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
            
    except Exception as e:
        print(f"Error: {e}")
        #modify_firewall("DROP")

    finally:
        listener_socket.close()
        #modify_firewall("DROP")

def accepted(client_socket, client_address):
    modify_firewall("ACCEPT")
    print(f"Accepted connection from {client_address}")
    
    data = client_socket.recv(1024).decode('utf-8')
    print(f"Received data: {data}")

    response = "\n|\    \ \ \ \ \ \ \      __\n|  \    \ \ \ \ \ \ \   | O~-_\n|   >----|-|-|-|-|-|-|--|  __/\n|  /    / / / / / / /   |__\ \n|/     / / / / / / / \n "
    client_socket.sendall(response.encode('utf-8'))
    print("response: " + response)

    global password

    password = 1


def denied(client_socket, client_address):
    
    response = "Access denied."
            
    print("response: " + response)
    #modify_firewall("DROP")

    os.system("sudo iptables -I INPUT -p tcp -s" + client_address[0] + "-j ACCEPT ")
    os.system("sudo iptables -I OUTPUT -p tcp -d" + client_address[0] + "-j ACCEPT")

    



    #global password
    #password = 0

def handle_client(client_socket, client_address):
    controller()
    try:
        if client_address[0] == "192.168.56.101":
            accepted(client_socket,client_address)
            """
            modify_firewall("ACCEPT")
            print(f"Accepted connection from {client_address}")

            # Modify firewall to ACCEPT for authorized client
            

            # Receive and process data from the client
            data = client_socket.recv(1024).decode('utf-8')
            print(f"Received data: {data}")
            modify_firewall("ACCEPT")
            # Respond to the client
            response = "\n|\    \ \ \ \ \ \ \      __\n|  \    \ \ \ \ \ \ \   | O~-_\n|   >----|-|-|-|-|-|-|--|  __/\n|  /    / / / / / / /   |__\ \n|/     / / / / / / / \n "
            client_socket.sendall(response.encode('utf-8'))
            print("response: " + response)"""
        else:
            denied(client_socket,client_address)
            """
            # Respond to the client
            response = "Access denied."
            
            print("response: " + response)
            modify_firewall("DROP")"""

    except Exception as e:
        print(f"Error: {e}")

    finally:
        client_socket.close()
        print("lolo")

if __name__ == "__main__":
    #modify_firewall("ACCEPT")
    #os.system("sudo iptables -I INPUT -p tcp --dport 12345 -j ACCEPT")
    host = input("ip: ")
    port = int(input("port: "))
    modify_firewall("ACCEPT")  # Initialize the firewall rule
    start_listener(host, port)
