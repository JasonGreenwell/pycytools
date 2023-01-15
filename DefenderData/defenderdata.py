import wmi

def get_defender_scan_results(computer_name):
    computer = wmi.WMI(computer = computer_name)
    scan_results = c.Win32_SecurityCenter()[0].AntiVirusProduct.getProductInfo()
    return scan_results

computer_name = "target_computer_name"
print(get_defender_scan_results(computer_name))

#TODO
