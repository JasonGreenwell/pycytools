from scapy.all import *


def packet_callback(packet):
    try:
        print(f"Proto: {packet[IP].proto} | Source: {packet[IP].src} --> Dest: {packet[IP].dst}")
    except IndexError as ie:
        pass


conf.sniff_promisc = True

sniff(prn=packet_callback, store=0)
