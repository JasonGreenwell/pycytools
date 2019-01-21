import threading
import time
import socket
import os
import struct
from ctypes import *
from netaddr import IPNetwork, IPAddress


class Listen:

    def __init__(self, host, subnet, option):
        self.host = host
        self.option = option
        self.subnet = subnet
        global socket_protocol
        if os.name == "nt":
            try:
                socket_protocol = socket.IPPROTO_IP
            except Exception as e:
                print(e)
        else:
            try:
                socket_protocol = socket.IPPROTO_ICMP
            except Exception as e:
                print(e)
        sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

        sniffer.bind((self.host, 0))

        sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

        if os.name == "nt":
            sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

        # print(sniffer.recvfrom(65565))
        try:
            while True:
                raw_buffer = sniffer.recvfrom(65565)[0]

                ip_header = IP(raw_buffer[0:20])


                if self.option == 1:
                    print(f"Protocol: {ip_header.protocol}, {ip_header.src_address} --> {ip_header.dst_address} ")
                elif self.option == 2:
                    if ip_header.protocol == "ICMP":
                        offset = ip_header.ihl * 4
                        buf = raw_buffer[offset:offset + sizeof(ICMP)]
                        icmp_header = ICMP(buf)
                        print(f"Protocol: {ip_header.protocol}, {ip_header.src_address} --> {ip_header.dst_address} ")
                        print(f"ICMP -> Type: {icmp_header.type} Code: {icmp_header.code}")
                elif self.option == 3:
                    offset = ip_header.ihl * 4
                    buf = raw_buffer[offset:offset + sizeof(ICMP)]
                    icmp_header = ICMP(buf)
                    if icmp_header.code == 3: # and icmp_header.type == 3:
                        if IPAddress(ip_header.src_address) in IPNetwork(subnet):
                            # if raw_buffer[len(raw_buffer) - len(b'BRRRRRT'):] == b'BRRRRRT':
                            print(f"Host Up: {ip_header.src_address}")

        except KeyboardInterrupt:
            if os.name == "nt":
                sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

    def host_check(self):
        pass


class IP(Structure):
    _fields_ = [
        ("ihl", c_ubyte, 4),
        ("version", c_ubyte, 4),
        ("tos", c_ubyte),
        ("len", c_ushort),
        ("id", c_ushort),
        ("offset", c_ushort),
        ("ttl", c_ubyte),
        ("protocol_num", c_ubyte),
        ("sum", c_ushort),
        ("src", c_ulong),
        ("dst", c_ulong)
    ]

    def __new__(self, socket_buffer = None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer = None):
        self.protocol_map = {1: "ICMP", 2: "IGMP", 6: "TCP", 17: "UDP"}

        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))

        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))

        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)


class ICMP(Structure):

    _fields_ = [
        ("type", c_ubyte),
        ("code", c_ubyte),
        ("checksum", c_ushort),
        ("unused", c_ushort),
        ("net_hop_mtu", c_ushort)
    ]

    def __new__(self, socket_buffer):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer):
        pass


class Scan:

    def __init__(self, host, subnet):
        self.host = host
        self.subnet = subnet

    def spray(self):
        time.sleep(5)
        sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        for ip in IPNetwork(self.subnet):
            try:
                sender.sendto("BRRRRRT", (f"{ip}", 65212))
            except:
                pass


Listen("192.168.1.103", "192.168.1.0/24", 3)
