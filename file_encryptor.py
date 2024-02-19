import ttkbootstrap as ttk
from tkinter import filedialog
from cryptography.fernet import Fernet
import os


class App():
    def __init__(self) -> None:
        super().__init__()
        self = ttk.Window(
            title='File encryptor',
            size=(350, 500),
            themename='darkly',
            resizable=(False, False)
        )
        self.file_encryptor = File_encryptor(self)
        self.mainloop()


class File_encryptor(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=(10, 10))
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.widgets()


    def widgets(self):
        self.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        self.rowconfigure((0, 1, 2, 3, 4, 5), weight=1, uniform='a')
        
        title_label = ttk.Label(self, text='File encryptor', font='arial 30') # title label
        open_bttn = ttk.Button(self, text='Open file', command=lambda: [self.get_files(), self.scrollbar(), self.function_button()]) # button
        key_bttn = ttk.Button(self, text='Open Key', command=lambda: [self.key_button()]) # button

        open_bttn.grid(row=1, column=0, sticky='ewn', columnspan=2, padx=10) # grid button
        key_bttn.grid(row=1, column=2, sticky='ewn', columnspan=2, padx=10) # grid button
        title_label.grid(row=0, column=0, sticky='', columnspan=4) # title label

    def function_button(self):
        global encrypt_bttn, decrypt_bttn
        encrypt_bttn = ttk.Button(self, text='Encrypt files', command=lambda: [self.create_key(), self.encrypt_file()]) # button
        decrypt_bttn = ttk.Button(self, text='Decrypt files') # button
        encrypt_bttn.grid(row=5, column=0, sticky='', columnspan=2) # grid button
        decrypt_bttn.grid(row=5, column=2, sticky='', columnspan=2) # grid button

    def key_button(self):
        create_key_bttn = ttk.Button(self, text='Create key', command=lambda: [self.create_key()]) # button
        select_key_bttn = ttk.Button(self, text='Select key', command=lambda: [self.select_key()]) # button
        create_key_bttn.grid(row=2, column=0, sticky='new', columnspan=2, padx=10) # grid button
        select_key_bttn.grid(row=2, column=2, sticky='new', columnspan=2, padx=10) # grid button

        elements = scrollbar_text, scrollbar, encrypt_bttn, decrypt_bttn
        print(type(elements))
        for element in elements:
            element.destroy()

    def get_files(self):
        self.filenames = filedialog.askopenfilenames(
            title='Open a file',
            initialdir='/',
            filetypes=(('All files', '*'),))
        
    def scrollbar(self):
        global scrollbar_text, scrollbar
        scrollbar_text = ttk.Text(self, height=10)
        scrollbar_text.grid(row=2, column=0, sticky='nes', columnspan=4, rowspan=3)

        scrollbar = ttk.Scrollbar(self, orient='vertical', command=scrollbar_text.yview)
        scrollbar.grid(row=2, column=2, sticky='nes', columnspan=4, rowspan=3)
        scrollbar_text.config(yscrollcommand=scrollbar.set)

        for filename in self.filenames:
            scrollbar_text.insert('end', f'{filename}\n')

    def create_key(self):
        key_name = 'key_gui.key'
        current_dir = os.getcwd()
        if not os.path.exists(key_name):
            key = Fernet.generate_key()
            with open(key_name, "wb") as key_file:
                key_file.write(key)
            self.fer = Fernet(key)
            self.key_location = current_dir + key_name
            print(f'your key is: {key}\nKey location: {self.key_location}')
        else:
            print('you already created key!, check your directory')
            file = open(key_name, "rb")
            key = file.read()
            self.fer = Fernet(key)
            print(f'Your key is loaded!\nKey: {key}')
        

    def select_key(self):
        current_dir = os.getcwd()
        key = filedialog.askopenfilenames(
            title='Open a file',
            initialdir=current_dir,
            filetypes=(('.key', '.key'),))
        key = ''.join(key)        
        file = open(key, "rb")
        key = file.read()
        self.fer = Fernet(key)
        print(f'Your key is loaded!\nKey: {key}')
       
    
    def read_file(self):
        self.readed_files = []
        for filename in self.filenames:
            file = open(filename, 'rb')
            self.file_bytes = file.read()
            file.close
            print(self.file_bytes)


    def encrypt_file(self):
        for filename in self.filenames:
            file = open(filename, 'rb')
            file_bytes = file.read()
            file.close
            print(filename)
            encrypted_data = self.fer.encrypt(file_bytes)
            file = open(filename, 'wb')
            file.write(encrypted_data)
            file.close()
            print(encrypted_data)

    def decrypt_file():
        pass

App()