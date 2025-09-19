import customtkinter as ctk


class SettingsFrame(ctk.CTkFrame):
    """Frame to hold password entry box, and iterations dropdown."""
    def __init__(self, master):
        super().__init__(master)
        self.master_ref = master
        self.password_entry = ctk.CTkEntry(self, placeholder_text='Password', show='*')
        self.password_icon = ctk.CTkLabel(self, text='', image=master.get_element_icon('Key.png'))
        self.iterations_dropdown = ctk.CTkOptionMenu(self, values=['100000', '200000', '500000', '1000000', '2000000'])

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(0, weight=1)

        self.password_icon.grid(row=0, column=0, pady=10, padx=(10, 5), sticky='w')
        self.password_entry.grid(row=0, column=1, pady=10, padx=(5, 10), sticky='ew')
        self.iterations_dropdown.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky='ew')

    def get_password(self) -> str:
        """Returns the user chosen password."""
        return self.password_entry.get()
    
    def get_iterations(self) -> int:
        """Returns the user chosen number of iterations."""
        return int(self.iterations_dropdown.get())