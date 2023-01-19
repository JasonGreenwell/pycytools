import concurrent.futures
from tqdm import tqdm
import subprocess
from prettytable import PrettyTable
import socket
import ipaddress

def ping_host(ip):
    try:
        subprocess.check_output("ping -c 1 " + ip, shell=True)
        return ip
    except:
        pass

def scan_network():
    choice = input("Do you want to scan your current network or enter a specific network address? (1 for Current/2 for specific)")
    if choice == "1":
        hostname = socket.gethostbyname(socket.gethostname())
        ip = ipaddress.ip_address(hostname)
        subnet = ipaddress.ip_interface(f"{ip}/24")
        ip_range = str(subnet.network)
        subnet_mask = str(subnet.netmask)
        print(f"Detected {ip_range} as your network range and {subnet_mask} as your subnet mask\n Scanning Now")
    elif choice == "2":
        ip_range = input("Enter the network address in the format x.x.x.x/24: ")
    else:
        print("Invalid choice. Exiting...")
        return

    active_hosts = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(ping_host, ip_range[:-3] + str(i)) for i in range(1,256)]
        for future in tqdm(concurrent.futures.as_completed(futures), total=256, desc="Scanning network"):
            ip = future.result()
            if ip:
                active_hosts.append(ip)
    if active_hosts:
        table = PrettyTable()
        table.field_names = ["Active Hosts"]
        for host in active_hosts:
            table.add_row([host])
        print(table)
    else:
        print("No active hosts found.")

scan_network()
