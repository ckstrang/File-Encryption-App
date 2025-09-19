import customtkinter as ctk


class EncryptionFrame(ctk.CTkFrame):
    """Frame to hold encryption and decryption buttons."""
    def __init__(self, master, encrypt_event, decrypt_event):
        super().__init__(master)
        self.master_ref = master

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self.encryption_button = ctk.CTkButton(self, text='Encrypt', command=encrypt_event, image=master.get_element_icon('Encrypt.png'))
        self.decryption_button = ctk.CTkButton(self, text='Decrypt', command=decrypt_event, image=master.get_element_icon('Decrypt.png'))

        self.encryption_button.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        self.decryption_button.grid(row=0, column=2, padx=10, pady=10, sticky='ew')