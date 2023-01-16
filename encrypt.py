from cryptography.fernet import Fernet
with open('key.txt', 'r') as f:
        key =f.read()


f = Fernet(key)
token = f.encrypt(b"my deep dark secret")

print(token)

print(f.decrypt(token))