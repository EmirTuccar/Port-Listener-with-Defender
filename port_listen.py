import socket
import os
import subprocess

def modify_firewall(action):
    command = ["sudo", "iptables", "-I", "INPUT", "-p", "tcp", "--dport", "12345", "-j", action]
    subprocess.run(command, check=True)


def start_listener(host, port):
    # Create a socket object
    listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Bind the socket to a specific address and port
        listener_socket.bind((host, port))
        
        # Listen for incoming connections
        listener_socket.listen(1)
        print(f"Listening on {host}:{port}")
        
        while True:
            # Accept a new connection
            #os.system("sudo iptables -I INPUT -p tcp --dport 12345 -j ACCEPT")
            modify_firewall("ACCEPT")
            client_socket, client_address = listener_socket.accept()
            
            if client_address[0] == "#Desired_ip_address":

                
                print(f"Accepted connection from {client_address}")
                
            
                # Receive and process data from the client
                data = client_socket.recv(1024).decode('utf-8')
                print(f"Received data: {data}")
                
            
                # Respond to the client
                response ="\n|\    \ \ \ \ \ \ \      __\n|  \    \ \ \ \ \ \ \   | O~-_\n|   >----|-|-|-|-|-|-|--|  __/\n|  /    / / / / / / /   |__\ \n|/     / / / / / / / \n "


                

                client_socket.sendall(response.encode('utf-8'))
                print("response: " + response)
            
                # Close the client socket
                client_socket.close()
            else:
                
                
                #modify_firewall("DROP")
                listener_socket.close()
            
    except Exception as e:
        print(f"Error: {e}")
        os.system("sudo iptables -I INPUT -p tcp --dport 12345 -j DROP")

    finally:
        # Close the listener socket
        listener_socket.close()

if __name__ == "__main__":
    host = input("ip: ")  # Listen on all available interfaces
    port = int(input("port: "))   # Choose a port number
    start_listener(host, port)
