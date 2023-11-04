from tkinter import Tk, Label, Button, Frame, Text, Entry, Toplevel, END, messagebox
from datetime import datetime
from tkinter import *
from PIL import Image, ImageTk
import random
import allfunctions as al
import pyodbc

win = Tk()
win.title("home")
entry = None
chatbox = None
original_image = Image.open("chatbot.png")
resized_image = original_image.resize((100, 100), Image.ANTIALIAS)
chatbot_image = ImageTk.PhotoImage(resized_image)

rules = {
    "hello": ["Namaste!", "Hello!", "Hey!"],
    "namestey":["Namestey","Hello","hey"],
    "ram ram":["JAI SHREE RAM "],
    "how are you": ["I'm doing well, thanks!", "I'm just a bot, so I don't have feelings, but I'm here to help!"],
    "what's your name": ["I'm a chatbot.", "I don't have a name, but you can call me ChatBot."],
    "bye": ["Goodbye!", "See you later!", "Have a great day!"],
    "how old are you": ["I don't have an age. I'm just a computer program.", "I exist in the digital realm, so I don't age."],
    "what is your purpose": ["My purpose is to assist you with information and answer your questions to the best of my knowledge."],
    "what is the eligibility for card_type": ["card_type  eligibility depends on various factors such as your age, health, and the type of card_type you are interested in. It's best to check the card application  page"],
    "how can i apply for card services": ["You can apply for card services by login in and choosing card services and then  filling out an online application form on our website. Make sure to provide all the necessary documents."],
    "how to convert normal account to fixed account": ["To convert a normal account to a fixed account login or register yourself then check for other services and select for conversion all the best!!."],
    "how many available schemes": ["We offer a variety of schemes, including savings accounts, fixed deposits, and insurence plans,and other schemes for that  Please visit our website"],
    "how to check profile": ["You can check your profile by logging into your online account or register yourself first to check profile if forgotten pssword choose forget password option then reset it "],
    "how to reset password": ["To reset your password, visit our website and click on the 'Forgot Password' link on the login page. Follow the instructions to reset your password."],
    "who is jesika": ["jesika is a good girl"],
    "who is gkb":["she is fantastic"]
}


def connect():
    try:
        server = 'localhost\SQLEXPRESS'
        database = 'bank'

        connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

        connection = pyodbc.connect(connection_string)

        print(f"Connected to SQL Server: {server}, Database: {database}")

        return connection

    except pyodbc.Error as e:
        print(f"Error connecting to the database: {e}")
        return None


def insert_data(name, phone, email, gender, nationality, state, address, password, username, dob,balance):
    
    connection=connect()
    if connection:
        try:
            cursor = connection.cursor()
            sql_insert = """
            INSERT INTO registration(Name, Phone, Email, Gender, Nationality, State, Address, Username, Password, DOB,balance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
            """
            values = (name, phone, email, gender, nationality, state, address, username, password, dob,balance)

            cursor.execute(sql_insert, values)
            connection.commit()
            cursor.close()

            print("Data inserted successfully") 

            messagebox.showinfo("welcome ", "vishnu legacy bank : " + username)

        except pyodbc.Error as e:
            messagebox.showinfo("DATABASE SERVER ERROR ",f"Error inserting data: {e}")
        finally:
            connection.close()


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
        ("NAME"), ("DATE OF BIRTH"), ("PHONE NO."),
        ("EMAIL ID"), ("GENDER"), ("NATION"),
        ("STATE"), ("ADDRESS"), ("Username"), ("PASSWORD")
    ]

    for i, (field_name) in enumerate(fields, start=1):
        label = Label(register_window, text=field_name,
                      bg="SystemButtonFace", font=("Arial", 16))
        label.grid(row=i, padx=400, sticky="w", pady=20)

    
    name_entry = Entry(register_window, textvariable=name, width=30)
    name_entry.grid(row=1, padx=650, sticky="w")
    phone_entry = Entry(register_window, textvariable=phone_no, width=30)
    phone_entry.grid(row=3, padx=650, sticky="w")
    email_entry = Entry(register_window, textvariable=emailid, width=30)
    email_entry.grid(row=4, padx=650, sticky="w")
    gender_entry = Entry(register_window, textvariable=gender, width=30)
    gender_entry.grid(row=5, padx=650, sticky="w")
    nation_entry = Entry(register_window, textvariable=nationality, width=30)
    nation_entry.grid(row=6, padx=650, sticky="w")
    state_entry = Entry(register_window, textvariable=state, width=30)
    state_entry.grid(row=7, padx=650, sticky="w")
    add_entry = Entry(register_window, textvariable=address, width=30)
    add_entry.grid(row=8, padx=650, sticky="w")
    pass_entry = Entry(register_window, textvariable=password, width=30)
    pass_entry.grid(row=10, padx=650, sticky="w")
    user_entry=Entry(register_window, textvariable=username, width=30)
    user_entry.grid(row=9, padx=650, sticky="w")
    
    heading_lb = Label(register_window, text="CREATE YOUR ACCOUNT",
                       bg="SystemButtonFace", font=("Arial", 25))
    heading_lb.grid(row=0, padx=400, sticky="w")

    dob_label = Label(register_window, text="DATE OF BIRTH",bg="SystemButtonFace", font=("Arial", 16))
    dob_label.grid(row=2, padx=400, sticky="w", pady=20)

    dob_entry = Entry(register_window, textvariable=DOB, width=30)
    dob_entry.grid(row=2, padx=650, sticky="w")

    balance=0

    register_btn = Button(register_window, text="REGISTER", bg="grey", fg="white", font=("bold", 20), width=10, command=lambda:insert_data(name_entry.get(),phone_entry.get(),email_entry.get(),gender_entry.get(),nation_entry.get(),state_entry.get(),add_entry.get(),pass_entry.get(),user_entry.get(),dob_entry.get(),balance))
    register_btn.grid(row=10, sticky="e")

    login_btn = Button(register_window, text="LOGIN", bg="grey",fg="white", font=("bold", 20), command=al.login_user)
    login_btn.grid(row=10, padx=55, sticky="w")

    register_window.mainloop()



def modify_account_window(win):
    def connect_to_database():
        try:
            connection = pyodbc.connect(
                "Driver={SQL Server};"
                "Server=localhost\\SQLEXPRESS;"
                "Database=bank;"
                "Trusted_Connection=yes;"
            )
            return connection
        except pyodbc.Error as e:
            print(f"Database connection error: {e}")
            return None

    def update_user_info(username, field_var, new_value,password):
        connection = connect_to_database()
        if not connection:
            return
        
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT username FROM registration WHERE username = ? AND password=?", (username,password))
            existing_username = cursor.fetchone()

            if existing_username:
            
                cursor.execute(f"UPDATE registration SET {field_var} = ? WHERE username = ?", (new_value, username))
                connection.commit()
                status_label.config(text="Account information updated successfully!", fg="green")
            else:
                status_label.config(text="Username not found in the database.", fg="red")
        except pyodbc.Error as e:
                print(f"Error updating registration info: {e}")
                status_label.config(text="Error updating account information.", fg="red")
        finally:
            connection.close()

    def modify_account():
        username = username_var.get()
        field = field_var.get()
        new_value = entry_var.get()
        password=password_var.get()
    
        if not username or not field or not new_value:
            status_label.config(text="Please fill in all fields.", fg="red")
            return
    
        update_user_info(username, field, new_value,password)

    modify = Toplevel(win)
    modify.title("Modify Account Information")
    head_lb = Label(modify, text="MODIFY YOUR ACCOUNT", font=("Helvetica", 25), bg="SystemButtonFace")
    head_lb.grid(row=0, sticky="w", padx=40, pady=10)
    frame = Frame(modify, padx=20, pady=20)
    frame.grid()
    username_label = Label(frame, text="Username:", font=("Helvetica", 16), bg="SystemButtonFace")
    username_label.grid(row=0, sticky="w", padx=60)
    password_label = Label(frame, text="Password:", font=("Helvetica", 16), bg="SystemButtonFace")
    password_label.grid(row=1, sticky="w", padx=60)

    global username_var
    global password_var
    username_var = StringVar()
    username_entry = Entry(frame, textvariable=username_var)
    username_entry.grid(row=0, sticky="w", padx=250)
    password_var = StringVar()
    password_entry = Entry(frame, textvariable=password_var)
    password_entry.grid(row=1, sticky="w", padx=250)

    field_label = Label(frame, text="Modify", font=("bold", 16), bg="SystemButtonFace")
    field_label.grid(row=2, sticky="w", padx=60)

    fields = ["name", "phone", "email", "gender", "nationality", "state", "address","username"]
    global field_var
    field_var = StringVar()
    field_dropdown = OptionMenu(frame, field_var, *fields)
    field_dropdown.grid(row=2, sticky="w", padx=250)

    entry_label = Label(frame, text="New Value:", font=("Helvetica", 16), bg="SystemButtonFace")
    entry_label.grid(row=4, sticky="w", padx=60)

    global entry_var
    entry_var = StringVar()
    entry = Entry(frame, textvariable=entry_var)
    entry.grid(row=4, sticky="w", padx=250)
    modify_button = Button(frame, text="Modify", command=modify_account, font=("Helvetica", 16, "bold"), bg="grey", fg="white")
    modify_button.grid(row=6, sticky="w", padx=60)

    global status_label
    status_label = Label(frame, text="", fg="green", font=("Helvetica", 16), bg="SystemButtonFace")
    status_label.grid(row=7, columnspan=2)

    modify.mainloop()

def navigate(label):
    if label == "SERVICES":
        al.services()
        print("Services function called")
    elif label == "EXPENSE PREDICTOR":
        al.expense_predictor()
        print("Expense Predictor function called")
    elif label == "CARD SERVICES":
        al.card_application_page()
        print("card application window opened")
    elif label == "MODIFY ACCOUNT":
        modify_account_window(win)
        print("Modify Account function called")
    elif label == "HISTORY":
        print("History function called")


def generate_response(user_input):
    for key in rules:
        if key in user_input:
            return random.choice(rules[key])
    return "I'm sorry, I don't understand that."


def send_message():
    global entry, chatbox
    user_input = entry.get().lower()
    if user_input == "exit":
        chatbox.config(state=NORMAL)
        chatbox.insert(END, "You: " + user_input + "\n")
        chatbox.insert(END, "ChatBot: Goodbye!\n")
        chatbox.config(state=DISABLED)
        entry.config(state=DISABLED)
    else:
        response = generate_response(user_input)
        chatbox.config(state=NORMAL)
        chatbox.insert(END, "You: " + user_input + "\n")
        chatbox.insert(END, "ChatBot: " + response + "\n")
        chatbox.config(state=DISABLED)
        entry.delete(0, END)


def open_chatbot_window():
    global entry, chatbox
    chatbot_window = Toplevel(win)
    chatbot_window.title("ChatBot")
    chatbot_window.geometry("500x600")

    chatbot_label = Label(chatbot_window, image=chatbot_image)
    chatbot_label.pack()

    greeting_label = Label(
        chatbot_window, text="Namaste ,How Can I Help You? ", fg="black", font=("Arial", 12))
    greeting_label.pack()

    chatbox = Text(chatbot_window, state=DISABLED)
    chatbox.pack()

    entry = Entry(chatbot_window)
    entry.pack()

    send_button = Button(chatbot_window, text="Send", command=send_message)
    send_button.pack()


def update_time():
    current_time = datetime.now().strftime("%H:%M:%S %d %Y-%m")
    time_label.config(text=current_time)
    win.after(1000, update_time)

time_label = Label(win, font=("Helvetica", 20), bg="SystemButtonFace")
time_label.grid(row=0, pady=6, padx=6, sticky="w")
update_time()

register_btn_m = Button(win, text="REGISTER", font=("Helvetica", 20), bg="SystemButtonFace", bd=0, command=register)
register_btn_m.grid(row=0, pady=6, padx=130, sticky="e")

login_btn = Button(win, text="LOGIN", font=("Helvetica", 20),bg="SystemButtonFace", bd=0, command=al.login_user)
login_btn.grid(row=0, pady=6, padx=30, sticky="e")

left_image = Image.open("namaste.png")
left_photo = ImageTk.PhotoImage(left_image)
left_label = Label(win, image=left_photo, bg="SystemButtonFace")
left_label.grid(row=3, sticky="w", padx=655)

head_lb = Label(win, text="VISHNU LEGACY BANK", font=(
    "Helvetica", 35), bg="SystemButtonFace", bd=0)
head_lb.grid(row=3, sticky="w", padx=100)

right_image = Image.open("namaste.png")
right_photo = ImageTk.PhotoImage(right_image)
right_label = Label(win, image=right_photo, bg="SystemButtonFace")
right_label.grid(row=3, sticky="w")

nav_frame = Frame(win, bg="gray")
nav_frame.grid(row=4, pady=20, sticky="we")
win.columnconfigure(0, weight=1)

nav_links = ["Services", "Expense Predictor",
             "card services", "Modify Account", "history"]
nav_links = [link.upper() for link in nav_links]
for i, link in enumerate(nav_links):
    link_button = Button(nav_frame, text=link, command=lambda l=link: navigate(l), font=("Helvetica", 16))
    link_button.grid(row=4, column=i, padx=60, pady=10)

intro_lb = Label(win, text="Who Are We ?..", font=("Helvetica", 24))
intro_lb.grid(row=5, sticky="w", padx=10)

para_text = """where tradition and innovation converge to redefine your banking experience. Our cutting-edge face recognition technology ensures the utmost security for your accounts, while our intelligent expense predictor helps you plan for the future with precision. Say hello to Naidy our round-the-clock chat bot, ready to assist you with questions and transactions at any hour. At Vishnu Legacy Bank, we're dedicated to delivering exceptional service and building enduring customer relationships. Join us on this journey towards modern banking excellence, where your financial well-being is our top priority.
At Vishnu Legacy Bank, we are committed to delivering exceptional service and building lasting relationships with our customers. Our range of traditional and modern banking services, coupled with our innovative technology features, ensures that your financial needs are not only met but exceeded.
Join us on this exciting journey towards modern banking excellence. Experience the future of banking with Vishnu Legacy Bank """

para_text = para_text.upper()

para_lines = para_text.split('\n')
for i, line in enumerate(para_lines):
    para_line_lb = Label(win, text=line, font=(
        16), wraplength=1500, justify="left", anchor="w")
    para_line_lb.grid(row=7+i, sticky="nsew", padx=15, pady=10)

original_image = Image.open("chatbot.png")
resized_image = original_image.resize((100, 100), Image.ANTIALIAS)
chatbot_button = Button(win, image=chatbot_image, command=open_chatbot_window)
chatbot_button.grid(row=10, sticky="e", padx=100, pady=20)
chatbot_lb = Label(win, text="How Can I Help You ? ",
                   bg="SystemButtonFace", fg="black", font=("Arial", 16))
chatbot_lb.grid(row=11, sticky="e", padx=60)

win.mainloop()

