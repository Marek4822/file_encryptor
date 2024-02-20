import ttkbootstrap as ttk
from tkinter import filedialog
from cryptography.fernet import Fernet
import os
import time

class App():
    def __init__(self) -> None:
        super().__init__()
        self = ttk.Window(
            title='File encryptor',
            size=(350, 500),
            themename='darkly',
            # resizable=(False, False)
        )
        self.file_encryptor = File_encryptor(self)
        self.mainloop()


class File_encryptor(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=(10, 10))
        self.place(x=0, y=0, relwidth=1, relheight=1)
        self.key = ''
        self.widgets()
        

    def widgets(self):
        self.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1, uniform='a')
        
        title_label = ttk.Label(self, text='File encryptor', font='arial 30') # title label
        open_bttn = ttk.Button(self, text='Open file', command=lambda: [self.get_files(), self.scrollbar(), self.function_button()]) # button
        key_bttn = ttk.Button(self, text='Open Key', command=lambda: [self.key_button()]) # button
        self.key_label = ttk.Label(self, text=f'Your key: {self.key}') # key label

        open_bttn.grid(row=1, column=0, sticky='ewn', columnspan=2, padx=10) # grid button
        key_bttn.grid(row=1, column=2, sticky='ewn', columnspan=2, padx=10) # grid button
        title_label.grid(row=0, column=0, sticky='', columnspan=4) # grid title
        self.key_label.grid(row=7, column=0, sticky='w', rowspan=7) # grid key
        

    def function_button(self):
        global encrypt_bttn, decrypt_bttn, checkbox
        encrypt_bttn = ttk.Button(self, text='Encrypt files', command=lambda: [self.encrypt_file()]) # button
        decrypt_bttn = ttk.Button(self, text='Decrypt files', command=lambda: [self.decrypt_file()]) # button
        self.checkbox_var = ttk.IntVar()
        checkbox = ttk.Checkbutton(self, text='Do you want to encrypt name to?',variable=self.checkbox_var , onvalue=1, offvalue=0, command=self.checker) # checkbox
        encrypt_bttn.grid(row=6, column=0, sticky='ewn', columnspan=2, padx=10) # grid button
        decrypt_bttn.grid(row=6, column=2, sticky='ewn', columnspan=2, padx=10) # grid button
        checkbox.grid(row=5, column=0, sticky='w', columnspan=4) # grid checkbox


    def checker(self):
        if self.checkbox_var.get() == 1:
            # self.key_label.config(text="Checked!")
            print('you clicked checkbox!')
        else:
            # self.key_label.config(text="Unchecked!")
            print('you unclicked checkbox!')


    def key_button(self):
        create_key_bttn = ttk.Button(self, text='Create key', command=lambda: [self.create_key()]) # button
        select_key_bttn = ttk.Button(self, text='Select key', command=lambda: [self.select_key()]) # button
        create_key_bttn.grid(row=2, column=0, sticky='new', columnspan=2, padx=10) # grid button
        select_key_bttn.grid(row=2, column=2, sticky='new', columnspan=2, padx=10) # grid button

        elements = scrollbar_text, scrollbar, encrypt_bttn, decrypt_bttn, checkbox
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
            self.key = Fernet.generate_key()
            with open(key_name, "wb") as key_file:
                key_file.write(self.key)
            self.fer = Fernet(self.key)
            self.key_location = current_dir + key_name
            print(f'your key is: {self.key}\nKey location: {self.key_location}')
            self.update_key_label()

        else:
            print('you already created key!, check your directory')
            file = open(key_name, "rb")
            self.key = file.read()
            self.fer = Fernet(self.key)
            print(f'Your key is loaded!\nKey: {self.key}')
            self.update_key_label()


    def select_key(self):
        current_dir = os.getcwd()
        key = filedialog.askopenfilenames(
            title='Open a file',
            initialdir=current_dir,
            filetypes=(('.key', '.key'),))
        key = ''.join(key)        
        file = open(key, "rb")
        self.key = file.read()
        self.fer = Fernet(self.key)
        print(f'Your key is loaded!\nKey: {self.key}')
        self.update_key_label()


    def update_key_label(self):
        self.key_label.config(text = f'Your key: {self.key}')
            

    def encrypt_file(self):
        start = time.time()
        print(f'encrypt key --> {self.key}')
        for filename in self.filenames:
            file = open(filename, 'rb')
            file_bytes = file.read()
            file.close
            print(filename)
            encrypted_data = self.fer.encrypt(file_bytes)
            file = open(filename, 'wb')
            file.write(encrypted_data)
            file.close()
        end = time.time()
        print(round(end - start, 2), "sec")

    def decrypt_file(self):
        start = time.time()
        print(f'encrypt key --> {self.key}')
        for filename in self.filenames:
            file = open(filename, 'rb')
            file_bytes = file.read()

            file.close
            print(filename)
            encrypted_data = self.fer.decrypt(file_bytes)
            file = open(filename, 'wb')
            file.write(encrypted_data)
            file.close()
        end = time.time()
        print(round(end - start, 2), "sec")

App()