#!/usr/bin/env python3
import subprocess, platform
from re import search
from cryptography.fernet import Fernet
import os.path
import sys
import tldextract

# Import from external variables file
import variables

program_name = "autovpn"

def extract_domain(url):
    '''
    If str = https://bonjour.com/weuhriu/ewrweurh/rtyrtu
    Returns = bonjour.com
    '''
    extracted = tldextract.extract(url)
    return extracted.fqdn

def quitandclose():
    sys.exit(0)
 
def ping(host):
    '''
    Ping devices from this script
    '''
    # Detects whether the operating system is Windows, if so, variable set to True, otherwise False
    isWin = platform.system().lower() == "windows"
    # 'try' allows you to handle errors if any (to customize the display, for example)
    try:
        # Allows you to run the ping command on the system terminal and adapts its syntax according to the OS: 'n' for Windows; 'c' for Linux
        output = subprocess.check_output("ping -{} 1 {}".format('n' if isWin else 'c', host), shell=True)
        # If Windows
        if isWin:
            # If the regex matches (and therefore the ping worked), return True
            if search("[0-9] *ms", str(output)):
                return True
            # Else False
            else:
                return False
    # If error, then:
    except Exception as e:
        return False

    # If ping Linux OK, return True
    return True

def decrypt(token: bytes, key: bytes) -> bytes:
    '''
    Decrypt a token with a key
    '''
    try:
        result = Fernet(key).decrypt(token)
    except Exception as e:
        print("ERROR: Looks like the key linked to your password has changed, please regenerate your password's hash with the new key and paste the result in \"variables.py\".")
        sys.exit(1)
    return result

def mykeygen() -> bytes:
    '''
    Generate a key and store it in a file
    '''
    # Does the key already exists?
    if os.path.isfile(".key"):
        # If yes, read it
        with open(".key", "rb") as file:
            key = file.read()
    else:
        # If no, generate it and write it in a file
        key = Fernet.generate_key()  # store in a secure location
        with open(".key", "wb") as file:
            file.write(key)
    # Encode the key in bytes if it is not already
    if type(key) != bytes:
        key = key.encode("utf-8")
    return key

# ----

###
# Main program
###

def main():
    # Get or create the key use for password encryption
    mykey = mykeygen()

    i = 0
    while not ping(extract_domain(variables.vpn_url)):
        print("We are unable to access VPN URL: " + extract_domain(variables.vpn_url) + "\nPlease try again!")
        i += 1
        if i >= 5:
            quitandclose()

    # If an error appears asking you to disconnect from other tabs
    try:
        '''
        Try connecting to the Company's VPN
        '''

        if type(variables.vpn_pw) != bytes:
            variables.vpn_pw = variables.vpn_pw.encode("utf-8")
        subprocess.check_output([variables.vpn_launcher, "-url", variables.vpn_url, "-u", variables.vpn_user, "-p", decrypt(variables.vpn_pw, mykey).decode(), "-r", variables.vpn_domain])

    # If error, then:
    except Exception as e:
        # There were no login errors
        print("An error occured while connecting!\nCheck if your username and password are correct!\nOr else, is there an issue with the VPN client?\nPlease try again.")
        return

    quitandclose()

if __name__ == '__main__':
    main()
