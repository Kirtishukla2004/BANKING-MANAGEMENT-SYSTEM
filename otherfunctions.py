from tkinter import *
import databaseconnet as db
import facerecorgination as fc
from databaseconnet import profile
from tkinter import messagebox
import services as sc


def register():
    register_window = Tk()
    register_window.title("REGISTER")
    name = StringVar()
    DOB = StringVar()
    phone_no = StringVar()
    emailid = StringVar()
    gender = StringVar()
    nationality = StringVar()
    state = StringVar()
    address = StringVar()
    password = StringVar()
    username = StringVar()

    fields = [
        ("NAME", name), ("DATE OF BIRTH", DOB), ("PHONE NO.", phone_no),
        ("EMAIL ID", emailid), ("GENDER", gender), ("NATION", nationality),
        ("STATE", state), ("ADDRESS", address), ("Username", username), ("PASSWORD", password)
    ]

    for i, (field_name, field_variable) in enumerate(fields, start=1):
        label = Label(register_window, text=field_name, bg="SystemButtonFace", font=("Arial", 16))
        label.grid(row=i, padx=400, sticky="w", pady=20)

        entry = Entry(register_window, textvariable=field_variable, width=30)
        entry.grid(row=i, padx=650, sticky="w")

    heading_lb = Label(register_window, text="CREATE YOUR ACCOUNT", bg="SystemButtonFace", font=("Arial", 25))
    heading_lb.grid(row=0, padx=400, sticky="w")

    register_btn = Button(register_window, text="REGISTER", bg="grey", fg="white", font=("bold", 20), width=10, command=lambda: db.insert_data(name.get(), phone_no.get(), emailid.get(), gender.get(), nationality.get(), state.get(), address.get(), password.get(), username.get(), DOB.get()))

    register_btn.grid(row=10, sticky="e")
    login_btn = Button(register_window, text="LOGIN", bg="grey", fg="white", font=("bold", 20), command=login_user)
    login_btn.grid(row=10, padx=55, sticky="w")

    register_window.mainloop()




username = None
password = None

def login_user():
    login_window = Tk()
    login_window.title("LOGIN")

    def login_button_click():
        entered_username = username_entry.get()
        entered_password = password_entry.get()
        print("Entered Username:", entered_username)
        print("Entered Password:", entered_password)

        if not entered_username or not entered_password:
            print("Please enter both username and password")
            return

        if db.login_data(entered_username, entered_password):
            print("Login successful")

    heading_lb = Label(login_window, text="LOGIN", bg="SystemButtonFace", font=("Arial", 25))
    heading_lb.grid(row=0, padx=470, sticky="w")

    username_label = Label(login_window, text="USERNAME", bg="SystemButtonFace", font=("Arial", 16))
    username_label.grid(row=1, padx=400, sticky="w", pady=20)
    username_entry = Entry(login_window, width=30)
    username_entry.grid(row=1, padx=650, sticky="w")

    password_label = Label(login_window, text="PASSWORD", bg="SystemButtonFace", font=("Arial", 16))
    password_label.grid(row=2, padx=400, sticky="w", pady=20)
    password_entry = Entry(login_window, show="*", width=30)  # Use show="*" to hide password
    password_entry.grid(row=2, padx=650, sticky="w")

    login_btn = Button(login_window, text="LOGIN", bg="grey", fg="white", font=("bold", 20), width=10, command=login_button_click)
    login_btn.grid(row=4, sticky="w", padx=470, pady=30)
    
    forget_btn = Button(login_window, text="FORGET PASSWORD", bg="SystemButtonFace", bd=0, font=("Arial", 16),command=sc.forgot_password)
    forget_btn.grid(row=4, padx=800, sticky="w")
    img_btn=Button(login_window,text="take image",bg="SystemButtonFace", bd=0, font=("Arial", 16),command=fc.TakeImages)
    img_btn.grid(row=4,sticky="w")
    login_window.mainloop()
