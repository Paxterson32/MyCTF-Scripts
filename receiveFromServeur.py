from pwn import * 

connexion = remote('IP',PORT)

value = ""
flag = ""
index = 0
while value != '}':

        connexion.recvuntil('Text that displays:'.encode('latin-1'))

        connexion.sendline(str(index))
        data = (connexion.recvline()).decode('latin-1')
        value = data[-2]
        flag += value
        print(value) # Receive line after string is entered
        index += 1
        #connexion.interactive()

print(flag)
