from scapy.all import *
import sqlite3
import requests


class Monitor:

    def __init__(self):
        try:
            conf.sniff_promisc = True
        except:
            pass
        sniff(prn=self.packet_callback, store=0)

    def packet_callback(self, packet):
        try:
            print(f"Proto: {self.proto_lookup(packet[IP].proto)} | Source: {packet[IP].src} --> Dest: {packet[IP].dst} "
                  f"({self.get_location(packet[IP].dst)})")
        except IndexError as ie:
            pass

    @staticmethod
    def proto_lookup(number):
        conn = sqlite3.connect("db")
        cur = conn.cursor()
        lookup = f"SELECT kw FROM protocols WHERE num = '{number}'"
        protocol = cur.execute(lookup)
        return protocol.fetchone()[0]

    @staticmethod
    def get_location(ip):
        result = requests.get(f"https://json.geoiplookup.io/{ip}")
        dict = result.json()
        # print(dict.keys())
        try:
            return f"{dict['city']}, {dict['region']} , {dict['country_name']}"
        except KeyError as k:
            print(k)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    Monitor()
