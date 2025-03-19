import tkinter as tk
from tkinter import ttk
#from database import *
 
#conn, cursor = initialize_connection()
 
def center_window(width, height):
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
 
 
class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("Cricketers Database")
        center_window(800, 400)
        
        tools_frame = tk.Frame(root, width=200, height=400, bg="turquoise")
        tools_frame.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.Y)
        tk.Label(
            tools_frame,
            text="Cricketers Database",
            bg="olive",
            font=20
        ).pack(padx=5, pady=5)

        notebook = ttk.Notebook(tools_frame)
        notebook.pack(expand=True, fill="both")

        tools_tab = tk.Frame(notebook, bg="wheat")
        tools_var = tk.StringVar(value="None")
        for tool in ["View All", "Find By Name", "View Top Score"]:
            tk.Button(
                tools_tab,
                text=tool
            ).pack(anchor="w", padx=5, pady=5)

        edit_mode_tab = tk.Frame(notebook, bg="pink")
        for tool in ["Insert New", "Update by ID", "Delete by ID"]:
            tk.Button(
                edit_mode_tab,
                text=tool
            ).pack(anchor="w", padx=5, pady=5)

        notebook.add(tools_tab, text="Search Records")
        notebook.add(edit_mode_tab, text="Edit Records")

        tk.Button(
            tools_frame,
            text="Quit",
            command = root.destroy,
            width = 6
        ).pack(padx=5, pady=5)

        results_frame = tk.Frame(root, width=400, height=400, bg="violet")
        results_frame.pack(padx=5, pady=5, side=tk.TOP,fill=tk.BOTH)
        tk.Label(
            results_frame,
            text="Results",
            bg="grey",
            fg="white",
        ).pack(padx=5, pady=5,expand=True)

        tk.Label(results_frame).pack(padx=5, pady=5)

        self.pack()
         
    def open_login_window(self):
        for widget in self.winfo_children(): 
            widget.destroy()
        self.destroy()
        LoginWindow(self.master)
         
    def open_register_window(self):
        for widget in self.winfo_children(): 
            widget.destroy()
        self.destroy()
        RegisterWindow(self.master)
 
 
 
class LoginWindow(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("Login")
        self.master.resizable(False, False)
        center_window(240, 150)
         
        tk.Label(self, text="Username:").grid(row=0, column=0)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)
         
        tk.Label(self, text="Password:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)
         
        submit_button = tk.Button(self, text="Submit", width=8, command=self.submit)
        submit_button.grid(row=2, column=1, sticky="e", padx=10, pady=(10, 0))
 
        submit_button = tk.Button(self, text="Back", width=8, command=self.back)
        submit_button.grid(row=2, column=0, sticky="w", padx=10, pady=(10, 0))
        self.pack()
             
    def submit(self):
        data = {}
        data["email"] = self.username_entry.get()
        data["password"] = self.password_entry.get()
         
        if login(cursor, data) == True:
            print("successful login")
            for widget in self.winfo_children(): 
                widget.destroy()
            self.destroy()
            MainWindow(self.master)
        else:
            print("unsuccessful login")
 
    def back(self):
        for widget in self.winfo_children(): 
            widget.destroy()
        self.destroy()
        WelcomeWindow(self.master)
 
 
class RegisterWindow(tk.Frame):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("Register")
        self.master.resizable(False, False)
        center_window(320, 350)
         
        tk.Label(self, text="First Name:").grid(row=0, column=0, sticky="w")
        self.first_name_entry = tk.Entry(self, width=26)
        self.first_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="e")
         
        tk.Label(self, text="Last Name:").grid(row=1, column=0, sticky="w")
        self.last_name_entry = tk.Entry(self, width=26)
        self.last_name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="e")
         
        tk.Label(self, text="Password:").grid(row=2, column=0, sticky="w")
        self.password_entry = tk.Entry(self, show="*", width=26)
        self.password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="e")
         
        tk.Label(self, text="Email:").grid(row=3, column=0, sticky="w")
        self.email_entry = tk.Entry(self, width=26)
        self.email_entry.grid(row=3, column=1, padx=10, pady=10, sticky="e")
         
        tk.Label(self, text="Gender:").grid(row=4, column=0, sticky="w")
        self.gender_entry = tk.Entry(self, width=10)
        self.gender_entry.grid(row=4, column=1, padx=10, pady=10, sticky="e")
         
        tk.Label(self, text="Age:").grid(row=5, column=0, sticky="w")
        self.age_entry = tk.Entry(self, width=10)
        self.age_entry.grid(row=5, column=1, padx=10, pady=10, sticky="e")
         
        tk.Label(self, text="Address:").grid(row=6, column=0, sticky="w")
        self.address_entry = tk.Text(self, width=20, height=3)
        self.address_entry.grid(row=6, column=1, padx=10, pady=10, sticky="e")
         
        submit_button = tk.Button(self, text="Submit", width=8, command=self.submit)
        submit_button.grid(row=7, column=1, padx=10, pady=10, sticky="e")
 
        submit_button = tk.Button(self, text="Back", width=8, command=self.back)
        submit_button.grid(row=7, column=0, sticky="w", padx=10, pady=(10, 10))
        self.pack()
         
    def submit(self):
        data = {}
        data["firstName"] = self.first_name_entry.get()
        data["lastName"] = self.last_name_entry.get()
        data["password"] = self.password_entry.get()
        data["email"] = self.email_entry.get()
        data["gender"] = self.gender_entry.get()
        data["age"] = self.age_entry.get()
        data["address"] = self.address_entry.get(1.0, tk.END)
 
        register(cursor, conn, data)
 
    def back(self):
        for widget in self.winfo_children(): 
            widget.destroy()
        self.destroy()
        MainWindow(self.master)
 
 
root = tk.Tk()
root.eval('tk::PlaceWindow . center')
MainWindow(root)
root.mainloop()