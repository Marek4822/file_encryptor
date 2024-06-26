import ttkbootstrap as ttk
from tkinter import filedialog
from cryptography.fernet import Fernet
import os
import time
from threading import Thread

class App():
    def __init__(self) -> None:
        super().__init__()
        self = ttk.Window(
            title='File encryptor',
            size=(500, 600),
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
        self.function_ui = False
        self.function_ui_key = False
        self.is_checked = False
        self.isfinished = False

        self.tag_encrypted = 'ENCRYPTED'
        self.widgets()
        

    def widgets(self):
        self.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')
        self.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1, uniform='a')
        
        title_label = ttk.Label(self, text='ENCRYPTOR', font='arial 30') # title label
        open_bttn = ttk.Button(self, text='Open file', command=lambda: [self.handle_open_files()]) # button
        key_bttn = ttk.Button(self, text='Open Key', command=lambda: [self.key_button()]) # button
        self.key_label = ttk.Label(self, text=f'{self.key}') # key label

        open_bttn.grid(row=1, column=0, sticky='ewn', columnspan=2, padx=10) # grid button
        key_bttn.grid(row=1, column=2, sticky='ewn', columnspan=2, padx=10) # grid button
        title_label.grid(row=0, column=0, sticky='', columnspan=4) # grid title
        self.key_label.grid(row=8, column=0, sticky='w', columnspan=4) # grid key
        

    def function_button(self):
        self.function_ui = True
        self.encrypt_bttn = ttk.Button(self, text='Encrypt files', command=lambda: [self.encrypt_threading()]) # button
        self.decrypt_bttn = ttk.Button(self, text='Decrypt files', command=lambda: [self.decrypt_threading()]) # button
        self.checkbox_var = ttk.IntVar()
        self.checkbox = ttk.Checkbutton(self, text='Do you want to encrypt/decrypt name?',variable=self.checkbox_var , onvalue=1, offvalue=0, command=self.checker) # checkbox
        self.gauge = ttk.Floodgauge(self, bootstyle='info', mask='{}%', maximum=100, value=0, mode='determinate') # Floodgauge

        self.encrypt_bttn.grid(row=6, column=0, sticky='ewn', columnspan=2, padx=10) # grid button
        self.decrypt_bttn.grid(row=6, column=2, sticky='ewn', columnspan=2, padx=10) # grid button
        self.checkbox.grid(row=5, column=0, sticky='w', columnspan=4) # grid checkbox
        self.gauge.grid(row=7, column=0, sticky='ew', columnspan=4) # grid Floodgauge


    def checker(self):
        if self.checkbox_var.get() == 1:
            self.is_checked = True
            print(f'you clicked checkbox! {self.is_checked}')
        else:
            self.is_checked = False
            print(f'you clicked checkbox! {self.is_checked}')


    def key_button(self):
        print(self.function_ui)
        if self.function_ui:
            self.destroy_function_buttons()
        self.function_ui_key = True
        self.create_key_bttn = ttk.Button(self, text='Create key', command=lambda: [self.create_key()]) # button
        self.select_key_bttn = ttk.Button(self, text='Select key', command=lambda: [self.select_key()]) # button
        self.create_key_bttn.grid(row=2, column=0, sticky='new', columnspan=2, padx=10) # grid button
        self.select_key_bttn.grid(row=2, column=2, sticky='new', columnspan=2, padx=10) # grid button


    def destroy_function_buttons(self):
        elements = self.scrollbar_text, self.scrollbar_ui, self.encrypt_bttn, self.decrypt_bttn, self.checkbox, self.gauge
        for element in elements:
            element.destroy()

    def get_files(self):
        self.filenames = filedialog.askopenfilenames(
            title='Open a file',
            # initialdir="/",
            initialdir="C:\\Users\\marekbax\\Downloads\\encrypt",
            filetypes=(('All files', '*'),))


    def handle_open_files(self):
        if self.function_ui_key:
            self.destroy_key_buttons()
        self.get_files()
        if self.filenames:
            pass
        else:
            raise Exception('no files selected')
        self.scrollbar()
        self.function_button()

    def destroy_key_buttons(self):
        elements = self.create_key_bttn, self.select_key_bttn
        for element in elements:
            element.destroy()
        
        
    def scrollbar(self):
        self.scrollbar_text = ttk.Text(self, height=10)
        self.scrollbar_text.grid(row=2, column=0, sticky='nes', columnspan=4, rowspan=3)
        self.scrollbar_ui = ttk.Scrollbar(self, orient='vertical', command=self.scrollbar_text.yview, bootstyle="round")
        self.scrollbar_ui.grid(row=2, column=2, sticky='nes', columnspan=4, rowspan=3)
        self.scrollbar_text.config(yscrollcommand=self.scrollbar_ui.set)

        for filename in self.filenames:
            self.scrollbar_text.insert('end', f'{filename}\n')

    def create_key(self):
        self.key_name = 'key_gui.key'
        current_dir = os.getcwd()
        if not os.path.exists(self.key_name):
            self.key = Fernet.generate_key()
            with open(self.key_name, "wb") as key_file:
                key_file.write(self.key)
            self.fer = Fernet(self.key)
            self.key_location = current_dir + self.key_name
            print(f'your key is: {self.key}\nKey location: {self.key_location}')
            self.update_key_label()
        else:
            print('you already created key!, check your directory')
            file = open(self.key_name, "rb")
            self.key = file.read()
            self.fer = Fernet(self.key)
            print(f'Your key is loaded!\nKey: {self.key}')
            self.update_key_label()
        self.create_tag()


    def select_key(self):
        current_dir = os.getcwd()
        self.key_name = filedialog.askopenfilenames(
            title='Open a file',
            initialdir=current_dir,
            filetypes=(('.key', '.key'),))
        self.key_name = ''.join(self.key_name)        
        file = open(self.key_name, "rb")
        self.key = file.read()
        self.fer = Fernet(self.key)
        print(f'Your key is loaded!\nKey: {self.key}')
        self.update_key_label()
        self.create_tag()

    def update_key_label(self):
        short_key = self.key_name.split('/')
        short_key = short_key[-1]
        self.key_label.config(text = f'Your key: {short_key}')

    def encrypt_name(self):
        for filename in self.filenames:
            file_path = os.path.dirname(filename)
            short_name = filename.split('/')
            short_name = short_name[-1]
            encrypt_name = self.fer.encrypt(short_name.encode()).decode()
            encrypt_name = str(f"{file_path}/{encrypt_name}")
            os.rename(filename, encrypt_name)
            print(encrypt_name)

    def create_tag(self):
        self.tag_code = ''
        string_key = str(self.key)
        for i, value in enumerate(string_key):
            if (i%5) == 0:
                self.tag_code += value 
        print(self.tag_code)
            

    def tag(self):
        for filename in self.filenames:
            file = open(filename, 'r+')
            file_data = file.read() 
            file.seek(0, 0)
            file.write(f"{self.tag_encrypted}\n{self.tag_code}\n{file_data}")
            file.close


    def decrypt_name(self):
        for filename in self.filenames:
            file_path = os.path.dirname(filename)
            short_name = filename.split('/')
            short_name = short_name[-1]
            encrypt_name = self.fer.decrypt(short_name.encode()).decode()
            encrypt_name = str(f"{file_path}/{encrypt_name}")
            os.rename(filename, encrypt_name)
            print(encrypt_name)

    def untag(self):
        for filename in self.filenames:
            file = open(filename, 'rb+')
            lines = file.readlines()
            file.seek(0)
            file.truncate()
            file.writelines(lines[2:])


    def tag_checker(self):
        for filename in self.filenames:
            file = open(filename, 'rb')
            two_lines = file.readlines()[0:2]
            first = two_lines[0].strip()
            second = two_lines[1].strip()
            tag_code = f"b'{self.tag_code}'"
            tag_encrypted = f"b'{self.tag_encrypted}'"

            if str(first) == tag_encrypted:
                if str(second) == tag_code:
                    raise Exception("File is already encrypted!")
                else:
                    raise Exception("File is encrypted with different key!")
            else:
                continue

    def untag_checker(self):
        for filename in self.filenames:
            file = open(filename, 'rb')
            two_lines = file.readlines()[0:2]
            first = two_lines[0].strip()
            second = two_lines[1].strip()
            tag_code = f"b'{self.tag_code}'"
            tag_encrypted = f"b'{self.tag_encrypted}'"

            if str(first) == tag_encrypted:
                if str(second) == tag_code:
                    continue
                else:
                    raise Exception("File is encrypted with different key!")
            else:
                raise Exception("File is not encrypted!")
            
    def handle_gauge_stop(self):
        self.gauge.stop()
        self.gauge.configure(bootstyle='SUCCESS')
        self.gauge.configure(value=100)

    def handle_gauge_start(self):
        self.gauge.configure(bootstyle='INFO')
        self.gauge.configure(value=0)
        self.gauge.start()

    def encrypt_file(self):
        start = time.time()
        self.create_tag()
        self.tag_checker()
        self.handle_gauge_start()
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
        self.tag()
        if self.is_checked:
            self.encrypt_name()
        self.end = time.time()
        print(round(self.end - start, 2), "sec")
        self.handle_gauge_stop()


    def decrypt_file(self):
        start = time.time()
        self.untag_checker()
        self.untag()
        self.handle_gauge_start()
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
        if self.is_checked:
            self.decrypt_name()
        end = time.time()
        print(round(end - start, 2), "sec")
        self.handle_gauge_stop()

    def encrypt_threading(self):
        Thread(target = self.encrypt_file).start()
    
    def decrypt_threading(self):
        Thread(target = self.decrypt_file).start()

App()
# TODOADD https://ttkbootstrap.readthedocs.io/en/latest/api/tooltip/, ADD  https://ttkbootstrap.readthedocs.io/en/latest/api/widgets/floodgauge/ ADD NOTIFICATIONS, AUTO KEY LOAD
