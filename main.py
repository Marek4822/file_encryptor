from cryptography.fernet import Fernet

# def create_key():
#     key = Fernet.generate_key()
#     with open("key.key", "wb") as key_file:
#         key_file.write(key)

def read_key():
    file = open("key.key", "rb")
    key = file.read()
    file.close
    return key

key = read_key()
fer = Fernet(key)

def read_file():
    file = open("test.txt", 'rb')
    file_bytes = file.read()
    file.close
    return file_bytes

def encrypt_file(file_bytes):
    file_bytes = read_file() 
    encrypted_data = fer.encrypt(file_bytes)
    file = open("test.txt", 'wb')
    file.write(encrypted_data)
    file.close()

def decrypt_file(file_bytes):
    file_bytes = read_file() 
    decrypted_data = fer.decrypt(file_bytes)
    file = open("test.txt", 'wb')
    file.write(decrypted_data)
    file.close()

def main():
    file_bytes = read_file() 
    read_key()
    read_file()
    # encrypt_file(file_bytes)
    decrypt_file(file_bytes)

main()
