import requests

import monitor

# ip = "2605:e000:1f00:4a05:5971:bb5e:c56d:fde7"
# result = requests.get(f"https://json.geoiplookup.io/{ip}")
# dict = result.json()
# # print(dict.keys())
# try:
#     print(f"{dict['city']}, {dict['country_name']}")
# except KeyError as k:
#     print(k)
# except Exception as e:
#     print(e)

#print(monitor.get_location("1.1.1.1"))

monitor.Monitor()



