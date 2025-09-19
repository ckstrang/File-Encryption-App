import os

import customtkinter as ctk
from PIL import Image

from Assets.File_Icons import FILE_ICONS
from Core.CryptoManager import CryptoManager
from UI.HelpWindow import HelpWindow


class FileInfoFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.masterRef = master
        self.entries = []
        self.entry_dict: dict[str, FileEntry] = {}


        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=0)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        

        self.help_button = ctk.CTkButton(self, text='Help', command=self.show_help_event, image=master.get_element_icon('Help.png'))
        self.help_button.grid(row=0, column=2, padx=10, pady=10, sticky='e')

        self.file_list = ctk.CTkScrollableFrame(self)
        self.file_list.grid(row=1, column=0, columnspan=4, pady=10, padx=10, sticky='nesw')
        self.file_list.grid_columnconfigure(0, weight=0)
        self.file_list.grid_columnconfigure(1, weight=0)
        self.file_list.grid_columnconfigure(2, weight=1)
        self.file_list.grid_columnconfigure(3, weight=0)

        self.select_button = ctk.CTkButton(self, text='Select Files', command=self.select_files_event, image=master.get_element_icon('Add.png'))
        self.select_button.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

        self.output_button = ctk.CTkButton(self, text='Select Output Folder', command=self.select_output_event, image=master.get_element_icon('Directory.png'))
        self.output_button.grid(row=2, column=2, padx=10, pady=10, sticky='ew')

    def select_files_event(self):
        files = ctk.filedialog.askopenfilenames()
        for file_path in files:
            if file_path not in self.masterRef.files:
                self.masterRef.files.append(file_path)
                entry = FileEntry(self.file_list, file_path, self)
                self.entry_dict[file_path] = entry
                
                row = len(self.entries)
                entry.icon.grid(row=row, column=0, sticky='w', padx=(10, 5), pady=2)
                entry.label.grid(row=row, column=1, sticky='w', padx=(0, 10), pady=2)
                entry.progress_bar.grid(row=row, column=2, sticky='ew', padx=(0, 5), pady=2)
                entry.button.grid(row=row, column=3, sticky='e', padx=(0, 10), pady=2)

                entry.progress_bar.set(0)
                self.file_list.grid_columnconfigure(0, weight=0)
                self.file_list.grid_columnconfigure(1, weight=0)
                self.file_list.grid_columnconfigure(2, weight=1)
                self.file_list.grid_columnconfigure(3, weight=0)
                self.entries.append(entry)

    def select_output_event(self):
        output_directory = ctk.filedialog.askdirectory()
        print(output_directory)
        self.masterRef.output_directory = output_directory
    
    def remove_file_entry(self, entry):
        entry.icon.destroy()
        entry.label.destroy()
        entry.progress_bar.destroy()
        entry.button.destroy()
        self.entries.remove(entry)
        self.masterRef.files.remove(entry.file_path)
        self.entry_dict.pop(entry.file_path)

        for i, e in enumerate(self.entries):
            e.icon.grid(row=i, column=0, sticky='w', padx=(10,0), pady=2)
            e.label.grid(row=i, column=1, sticky='w', padx=(10, 0), pady=2)
            e.progress_bar.grid(row=i, column=2, padx=(10, 0), pady=2)
            e.button.grid(row=i, column=3, sticky='e', padx=(0, 10), pady=2)

    def get_icon_for_file(self, file_path: str) -> ctk.CTkImage:
        ext = os.path.splitext(file_path)[1].lower()
        icon_path = FILE_ICONS.get(ext, FILE_ICONS.get('default', ''))
        icon_image = ctk.CTkImage(Image.open(icon_path), size=(16, 16))
        return icon_image
    
    def show_help_event(self):
        HelpWindow(self).attributes("-topmost", True)

class FileEntry:
        def __init__(self, parent, file_path: str, container):
            self.file_path = file_path
            self.container = container
            self.crypto = CryptoManager()
            file_name = os.path.basename(file_path)
            
            try:
                icon_image = container.get_icon_for_file(file_path)
                self.icon = ctk.CTkLabel(parent, image=icon_image, text="", compound='left')
            except:
                self.icon = ctk.CTkLabel(parent, text="", compound='left')

            self.label = ctk.CTkLabel(parent, text=file_name, compound='left')
            self.progress_bar = ctk.CTkProgressBar(parent)
            self.button = ctk.CTkButton(parent, text='', image=self.container.masterRef.get_element_icon('Trash.png'), command=self._remove_event)

        def _remove_event(self):
            self.container.remove_file_entry(self)