import socket
import time
from netaddr import IPNetwork, IPAddress


def spray(subnet, message):
    time.sleep(5)
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    for ip in IPNetwork("192.168.1.0/24"):
        try:
            print(f"Sending {message.encode('utf-8')} to {ip}")
            sender.sendto(message.encode("utf-8"), (str(ip), 65212))
        except Exception as e:
            print(e)


spray("192.168.1.0/24", "BRRRRRT")
