import customtkinter as ctk

class HelpWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)
        ctk.set_widget_scaling(1.5)
        ctk.set_window_scaling(1.5)
        ctk.set_appearance_mode("light")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        min_width = int(screen_width * 0.2)
        min_height = int(screen_height * 0.25)
        self.minsize(min_width, min_height)

        self.title('Help & Instructions')

        title = ctk.CTkLabel(self, text='How to Use The Program', font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=(10, 5))

        instructions_frame = ctk.CTkScrollableFrame(self)
        instructions_frame.pack(pady=10, padx=10, fill='both', expand=True)

        instructions = (
            '1. Click "Select Files" to add file(s) for encryption or decryption.\n'
            '2. (Optional) Click "Select Output Folder" to choose where to output the resulting file(s).\n'
            '3. Use the password entry to input a password.\n'
            '   -This password is needed for decryption, do not forget it!\n'
            '   -If you forget the password, you cannot decrypt the file(s)\n'
            '4. Use the dropdown to select the number of iterations\n'
            '   -This affects security/speed\n'
            '   -More iterations = better encryption, takes longer\n'
            '   -Less iterations = weaker encryption, faster\n'
            '5. The progress bars show the progress for each file\n'
        )

        label = ctk.CTkLabel(instructions_frame, text=instructions, justify='left', anchor='nw', wraplength=500)
        label.pack(padx=10, pady=10)