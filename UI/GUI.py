import os
from concurrent.futures import ThreadPoolExecutor
from tkinter import messagebox

import customtkinter as ctk
from PIL import Image

from Core.CryptoManager import CryptoManager
from UI.EncryptionFrame import EncryptionFrame
from UI.FileInfoFrame import FileInfoFrame
from UI.SettingsFrame import SettingsFrame


class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_widget_scaling(1.5)
        ctk.set_window_scaling(1.5)
        ctk.set_appearance_mode("light")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        min_width = int(screen_width * 0.2)
        min_height = int(screen_height * 0.25)
        self.minsize(min_width, min_height)

        self.files = []
        self.output_directory = ''

        self.title('Encryption Manager')
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.file_frame = FileInfoFrame(self)
        self.file_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nesw')

        self.settings_frame = SettingsFrame(self)
        self.settings_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nesw')

        self.encryption_frame = EncryptionFrame(self, self.on_encrypt_clicked, self.on_decrypt_clicked)
        self.encryption_frame.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

    def get_element_icon(self, name: str):
        """
        Helper function to get icons for UI elements
        Parameters:
            name (str): name of the icon png.

        Returns:
            CTkImage: The requested icon as 16x16 CTkImage.
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))

        icon_dir = os.path.abspath(os.path.join(current_dir, '..', 'Assets', 'Icons'))
        
        icon_path = os.path.join(icon_dir, name)
        return ctk.CTkImage(light_image=Image.open(icon_path), size=(16,16))


    def on_encrypt_clicked(self):
        """Handles initiation of encryption process."""
        self.encryption_frame.encryption_button.configure(state='disabled')

        password   = self.settings_frame.get_password()
        iterations = self.settings_frame.get_iterations()

        if self._check_for_encryption_errors(password):
            self.encryption_frame.encryption_button.configure(state='normal')
            return

        self._run_crypto_loop('encrypt', password, iterations)
        self.encryption_frame.encryption_button.configure(state='normal')

    def on_decrypt_clicked(self):
        """Handles initiation of decryption process."""
        self.encryption_frame.decryption_button.configure(state='disabled')

        password   = self.settings_frame.get_password()
        iterations = self.settings_frame.get_iterations()

        if self._check_for_decryption_errors(password):
            self.encryption_frame.decryption_button.configure(state='normal')
            return

        self._run_crypto_loop('decrypt', password, iterations)
        self.encryption_frame.decryption_button.configure(state='normal')


    def _Message(self, warnings: str):
            """Displays any and all warnings to the user."""
            warnings += '\nPress the Help button for more info.'
            messagebox.showerror(title='Error During Operation', message=warnings)
            self.encryption_frame.decryption_button.configure(state='normal')

    def _check_for_encryption_errors(self, password: str) -> bool:
        """Checks to make sure all required components are present for encryption."""
        warnings = ''
        if not self.files:
            warnings += 'Please select files for encryption.\n'
        if not password:
            warnings += 'Please input a password to be used for encryption.\nDo not forget this password, you will need it for decryption.\n'
        if len(warnings) > 0:
            self._Message(warnings)
            return True
        return False
    
    def _check_for_decryption_errors(self, password: str) -> bool:
        """
        Checks to make sure all required components are present for decryption.
        
        Parameters:
            password (str): Password to use when deriving key used in cipher.

        Returns:
            boolean: True if errors are present, false if there are none.
        
        """
        def _verify_file_types() -> bool:
            """Verifies that all files to be decrypted are encrypted."""
            all_encrypted = True
            for file in self.files:
                file_ext = os.path.splitext(file)[1]
                if file_ext != '.encrypted':
                    all_encrypted = False
            return all_encrypted
        
        warnings = ''
        if not self.files:
            warnings += 'Please select files for decryption.\n'
        if not password:
            warnings += 'Please input a password to be used for decryption.\nThis must be the same password used for encryption of the file to be decrypted.\n'
        if not _verify_file_types():
            warnings += 'Selected files are not all encrypted.\nPlease only decrypt ".encrypted" files.\n'

        if warnings:
            self._Message(warnings)
            return True
        return False

    def _run_crypto_loop(self, mode: str, password: str, iterations: int) -> None:
        """
        Helper function that makes calls to encrypt and decrypt files.
        
        Parameters:
            mode       (str): 'encrypt' or 'decrypt' based on desired operation.
            password   (str): Password to use when deriving key used in cipher.
            iterations (int): Number of iterations for key generation.
        
        """
        max_workers = min(len(self.files), os.cpu_count() or 4)
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

        for file_path in self.files:
            cm = CryptoManager()
            self.file_frame.entry_dict[file_path].crypto = cm

            if mode == 'encrypt':
                self.executor.submit(self._encrypt_task, cm, file_path, password, iterations)
            else:
                self.executor.submit(self._decrypt_task, cm, file_path, password)
        
        self._poll_progress()

    def _encrypt_task(self, crypto: CryptoManager, file_path: str, password: str, iterations: int) -> None:
        """Worker task for encrypting files."""
        crypto.encrypt(file_path, password, iterations, self.output_directory)

    def _decrypt_task(self, crypto: CryptoManager, file_path: str, password: str) -> None:
        """
        Worker task for decrypting files.
        Parameters:
            crypto (CryptoManager): The CryptoManager to execute the decryption.
            file_path        (str): Path to the file to be decrypted
            password         (str): Password to use when deriving key used in cipher.
        """
        try:
            crypto.decrypt(file_path, password, self.output_directory)
        except ValueError:
            self._Message('Decryption of ' + file_path + ' has failed!\n'
            'Please verify the you are using the correct password.\n'
            'This password should be the same one you used for encryption.')

            entry = self.file_frame.entry_dict.get(file_path)
            assert entry is not None
            entry.button.configure(image=self.get_element_icon('X.png'))
            entry.progress_bar.configure(progress_color='red')

    def _poll_progress(self) -> None:
        """Helper function to update progress bars for each file currently being worked on"""
        all_done = True
        for file_path in self.files:
            entry = self.file_frame.entry_dict.get(file_path)
            assert entry is not None
            cm = entry.crypto
            if cm and entry:
                entry.button.configure(image=self.get_element_icon('Working.png'))
                progress = cm.get_progress()
                entry.progress_bar.set(progress)
                if progress < 1.0:
                    all_done = False
                else:
                    entry.button.configure(image=self.get_element_icon('Done.png'))
                    entry.progress_bar.configure(progress_color='green')
        if not all_done:
            self.after(100, self._poll_progress)