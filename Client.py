import socket
import time




class UDPClient:
    def __init__(self, HostIP, HostPort, Socket):
        self.HostIP = HostIP
        self.HostPort = HostPort
        self.client_socket = Socket
    def udp_echo_client_send(self, message):
        server_address = (self.HostIP, self.HostPort)
        try:
            t = time.time()
            message = str(t)+" "+message
            self.client_socket.sendto(message.encode('utf-8'), server_address)

        except Exception as e:
            print(f"Error: {e}")


