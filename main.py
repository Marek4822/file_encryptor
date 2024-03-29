from cryptography.fernet import Fernet
import time

# def create_key():
#     key = Fernet.generate_key()
#     with open("key.key", "wb") as key_file:
#         key_file.write(key)

def get_path():
    # print('Please type path to file: ')
    # path = input('-->')
    path = "dunkfile.png"
    return path

def read_key():
    file = open("key.key", "rb")
    key = file.read()
    file.close
    return key

def read_file(path):
    file = open(path, 'rb')
    file_bytes = file.read()
    file.close
    return file_bytes

def encrypt_file(file_bytes, path):
    file_bytes = read_file(path) 
    encrypted_data = fer.encrypt(file_bytes)
    file = open(path, 'wb')
    file.write(encrypted_data)
    file.close()

def decrypt_file(file_bytes, path):
    file_bytes = read_file(path) 
    decrypted_data = fer.decrypt(file_bytes)
    file = open(path, 'wb')
    file.write(decrypted_data)
    file.close()

def main():
    start = time.time()
    path = get_path()
    file_bytes = read_file(path) 
    read_key()
    read_file(path)
    # encrypt_file(file_bytes, path)
    decrypt_file(file_bytes, path)
    end = time.time()

    print(round(end - start, 2), "sec")

if __name__ == "__main__":
    key = read_key()
    fer = Fernet(key)
    main()