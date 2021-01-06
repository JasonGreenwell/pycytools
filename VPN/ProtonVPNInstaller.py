"""
Just a simple tool to automate installtion of protonVPN CLI requirements and then start the program
"""
import subprocess
from time import sleep


def installer():

    try:
        subprocess.check_output(['which', 'protonvpn-cli'])
    except subprocess.CalledProcessError:
        print("Proton VPN CLI is not installed.  Installing...")
        sleep(3)
        subprocess.run('wget -q -O - https://repo.protonvpn.com/debian/public_key.asc | sudo apt-key add - ', shell=True)
        subprocess.run('sudo add-apt-repository \'deb https://repo.protonvpn.com/debian unstable main\'', shell=True)
        subprocess.run('sudo apt-get update && sudo apt-get install protonvpn', shell=True)

    subprocess.run('protonvpn-cli', shell=True)


def main():
    installer()


if __name__ == "__main__":
    main()
