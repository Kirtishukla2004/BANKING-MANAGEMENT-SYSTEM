from tkinter import Tk, Label, Button, Frame, Text, Entry, Toplevel, END,messagebox
from datetime import datetime
from tkinter import*
from PIL import Image, ImageTk
import random
import pyodbc
from tkinter import ttk
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd
def connect_to_database(server='localhost\SQLEXPRESS', database='bank'):
    try:
        # Define the connection string
        connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        # Connect to the database
        connection = pyodbc.connect(connection_string)

        print(f"Connected to SQL Server: {server}, Database: {database}")

        return connection

    except pyodbc.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def insert_data(name, phone, email, gender, nationality, state, address, password, username, dob,balance):
    
    connection=connect_to_database()
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
            print(f"Error inserting data: {e}")
        finally:
            connection.close()
    else:
        print("connection not found ")

def fetch_user_data(username):
    try:
        connection=connect_to_database()
        cursor = connection.cursor()

      
        cursor.execute("SELECT Name, DOB, Phone, Email FROM registration WHERE username = ?", (username))
        user_data = cursor.fetchone()

        if user_data:
            user_info = {
                'Name': user_data[0],
                'DOB': user_data[1],
                'Phone': user_data[2],
                'Email': user_data[3]
            }
            return user_info

    except pyodbc.Error as e:
        print(f"pyodbc error: {e}")
    finally:
        connection.close()
    return {
        'Name': 'User Not Found',
        'DOB': '',
        'Phone': '',
        'Email': '',
    }


    profile = Tk()
    profile.title("PROFILE PAGE ")
    def update_time():
        current_time = datetime.now().strftime("%H:%M:%S %d %Y-%m")
        time_label.config(text=current_time)
        profile.after(1000, update_time)
    time_label = Label(profile, font=("Helvetica", 20), bg="SystemButtonFace")
    time_label.grid(row=0, pady=6, padx=6, sticky="w")
    update_time()


    head_lb = Label(profile, text="VISHNU LEGACY BANK", font=(
        "Helvetica", 35), bg="SystemButtonFace", bd=0)
    head_lb.grid(row=3, sticky="w", padx=100)

    nav_frame = Frame(profile, bg="gray")
    nav_frame.grid(row=4, pady=20, sticky="we")
    profile.columnconfigure(0, weight=1)
    nav_links = ["Services", "Expense Predictor", "card services", "Modify Account", "history"]
    nav_links = [link.upper() for link in nav_links]
    for i, link in enumerate(nav_links):
        link_button = Button(nav_frame, text=link, command=lambda l=link:navigate(l), font=("Helvetica", 16))
        link_button.grid(row=4, column=i, padx=60, pady=10)

    login_btn = Button(profile, text="LOGOFF", font=(
        "Helvetica", 20), bg="SystemButtonFace", bd=0)
    login_btn.grid(row=0, pady=6, padx=6, sticky="ne")
    user_data = fetch_user_data(username)
    user_name_label = Label(profile, text=f"Name: {user_data['Name']}", font=("Arial", 20))
    user_name_label.grid(row=5, padx=100, sticky="w",pady=50)

    dob_label = Label(profile, text=f"Date of Birth: {user_data['DOB']}", font=("Arial", 20))
    dob_label.grid(row=6, padx=100, sticky="w",pady=10)

    contact_no_label = Label(profile, text=f"Contact No.: {user_data['Phone']}", font=("Arial", 20))
    contact_no_label.grid(row=7, padx=100, sticky="w",pady=20)

    email_label = Label(profile, text=f"Email: {user_data['Email']}", font=("Arial", 20))
    email_label.grid(row=8, padx=100, sticky="w",pady=30)
    profile.mainloop()

def clear_placeholder(entry_widget, placeholder_text):
    if entry_widget.get() == placeholder_text:
        entry_widget.delete(0, "end")

def set_entry_placeholder(entry_widget, placeholder_text):
    entry_widget.insert(0, placeholder_text)
    entry_widget.bind("<FocusIn>", lambda event: clear_placeholder(entry_widget, placeholder_text))

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

    dob_label = Label(register_window, text="DATE OF BIRTH", bg="SystemButtonFace", font=("Arial", 16))
    dob_label.grid(row=2, padx=400, sticky="w", pady=20)

    dob_entry = Entry(register_window, textvariable=DOB, width=30)
    dob_entry.grid(row=2, padx=650, sticky="w")

    set_entry_placeholder(dob_entry, "YYYY-MM-DD")
    balance=0
    register_btn = Button(register_window, text="REGISTER", bg="grey", fg="white", font=("bold", 20), width=10, command=lambda: insert_data(name.get(), phone_no.get(), emailid.get(), gender.get(), nationality.get(), state.get(), address.get(), password.get(), username.get(), DOB.get(),balance))
    register_btn.grid(row=10, sticky="e")

    login_btn = Button(register_window, text="LOGIN", bg="grey", fg="white", font=("bold", 20), command=login_user)
    login_btn.grid(row=10, padx=55, sticky="w")

    register_window.mainloop()

def calculator():
    def button_click(number):
        current = entry.get()
        entry.delete(0, END)
        entry.insert(0, current + str(number))

    def clear():
        entry.delete(0, END)

    def calculate():
        try:
            expression = entry.get()
            result = eval(expression)
            entry.delete(0, END)
            entry.insert(0, result)
        except Exception as e:
            entry.delete(0, END)
            entry.insert(0, "Error")

   
    cal_win = Tk()
    cal_win.title("Calculator")

    
    entry = Entry(cal_win, width=20)
    entry.grid(row=0, column=0, columnspan=4)

   
    buttons = [
        ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
        ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
        ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
        ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3)
    ]

    for (text, row, col) in buttons:
        button = Button(cal_win, text=text, padx=20, pady=20, command=lambda t=text: button_click(t))
        button.grid(row=row, column=col)

    clear_button = Button(cal_win, text='C', padx=20, pady=20, command=clear)
    clear_button.grid(row=5, column=0, columnspan=3)

    
    equal_button = Button(cal_win, text='=', padx=20, pady=20, command=calculate)
    equal_button.grid(row=5, column=3)


    cal_win.mainloop()

def deposit_page():

    def authenticate_and_deposit():
            username = username_entry.get()
            password = password_entry.get()
            amount = amount_entry.get()
            try:
                server = 'localhost\SQLEXPRESS'
                database = 'bank'
                connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

                connection = pyodbc.connect(connection_string)
                cursor = connection.cursor()

                cursor.execute("SELECT username, password FROM registration WHERE username=? AND password=?", (username, password))
                user_data = cursor.fetchone()

                if user_data:
                    if amount is not None and amount != "" and float(amount)>0:
                        cursor.execute("UPDATE registration SET balance=balance+? WHERE username=?", (amount, username))
                        connection.commit()
                        connection.close()
                        lb=Label(message_label,text=f'Deposited Successfully......{username},Amount {amount}',font=('bold',16),fg='green')
                        lb.grid(row=5)
                    else:
                        connection.close()
                        messagebox.showinfo("AMOUNT ERROR......",'Amount Cannot be NULL')
                else:
                    connection.close()
                    messagebox.showinfo("INVAILD......", f"WRONG INPUTS : {username},{password}")
            except Exception as e:
                    connection.rollback() 
                    messagebox.showinfo("Database error: " + str(e))


    depo_win = Tk()
    depo_win.title("Deposit Page")

    head_lb=Label(depo_win,text="DEPOSIT",font=("bold",25))
    head_lb.grid(row=0,sticky="w",padx=0)
    username_label = Label(depo_win, text="Username:",font=("bold",16))
    username_label.grid(row=1,padx=16,sticky="w")
    username_entry = Entry(depo_win)
    username_entry.grid(row=1,sticky="w",padx=200)

    password_label = Label(depo_win, text="Password:",font=("bold",16))
    password_label.grid(row=2,padx=16,sticky="w")
    password_entry = Entry(depo_win, show="*")
    password_entry.grid(row=2,sticky="w",padx=200)

    amount_label = Label(depo_win, text="Amount:",font=("bold",16))
    amount_label.grid(row=3,padx=16,sticky="w")
    amount_entry = Entry(depo_win)
    amount_entry.grid(row=3,sticky="w",padx=200)

    find_button = Button(depo_win, text="Deposit", bg="grey", fg="white",font=("bold",16) , command=authenticate_and_deposit)
    find_button.grid(row=4,padx=116,sticky="w",pady=10)

    message_label = Label(depo_win, text="", fg="green")
    message_label.grid()

    depo_win.mainloop()

def withdraw_page():
    def authenticate_and_withdraw():
        # Get data from the entry widgets
        username = username_entry.get()
        password = password_entry.get()
        amount = amount_entry.get()

        try:
            server = 'localhost\SQLEXPRESS'
            database = 'bank'
            connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            cursor.execute("SELECT username, password, balance FROM registration  WHERE username=? AND password=?", (username, password))
            user_data = cursor.fetchone()

            if user_data:
                current_balance = user_data[2]
                if current_balance >= float(amount) and float(amount)>0:
                    new_balance = current_balance - float(amount)
                    cursor.execute("UPDATE registration SET balance=? WHERE username=?", (new_balance, username))
                    connection.commit()
                    connection.close()
                    message_label.config(text=f"Withdrawn {amount} successfully for {username}")
                else:
                    message_label.config(text="Insufficient balance or wrong inputs ")
            else:
                
                message_label.config(text="Invalid username or password")
        except Exception as e:
            message_label.config(text="Database error: " + str(e))

    withdraw_win = Tk()
    withdraw_win.title("Withdraw Page")

    head_lb = Label(withdraw_win, text="WITHDRAW", font=("bold", 25))
    head_lb.grid(row=0, sticky="w", padx=0)

    username_label = Label(withdraw_win, text="Username:", font=("bold", 16))
    username_label.grid(row=1, padx=16, sticky="w")
    username_entry = Entry(withdraw_win)
    username_entry.grid(row=1, sticky="w", padx=200)

    password_label = Label(withdraw_win, text="Password:", font=("bold", 16))
    password_label.grid(row=2, padx=16, sticky="w")
    password_entry = Entry(withdraw_win, show="*")
    password_entry.grid(row=2, sticky="w", padx=200)

    amount_label = Label(withdraw_win, text="Amount:", font=("bold", 16))
    amount_label.grid(row=3, padx=16, sticky="w")
    amount_entry = Entry(withdraw_win)
    amount_entry.grid(row=3, sticky="w", padx=200)

    withdraw_button = Button(withdraw_win, text="Withdraw", bg="grey", fg="white", font=("bold", 16), command=authenticate_and_withdraw)
    withdraw_button.grid(row=4, padx=116, sticky="w", pady=10)

    message_label = Label(withdraw_win, text="", fg="green")
    message_label.grid()

    withdraw_win.mainloop()

def transfer_page():
    def authenticate_and_transfer():
    
        sender_username = sender_username_entry.get()
        sender_password = sender_password_entry.get()
        receiver_username = receiver_username_entry.get()
        amount = amount_entry.get()

        try:
            server = 'localhost\SQLEXPRESS'
            database = 'bank'
            connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            # Authenticate sender
            cursor.execute("SELECT username, password, balance FROM registration WHERE username=? AND password=?", (sender_username, sender_password))
            sender_data = cursor.fetchone()

            # Authenticate receiver
            cursor.execute("SELECT username FROM registration WHERE username=?", (receiver_username,))
            receiver_data = cursor.fetchone()

            if sender_data and receiver_data:
                sender_balance = sender_data[2]
                if sender_balance >= float(amount)and float(amount)>0:
                    # Update sender's balance
                    new_sender_balance = sender_balance - float(amount)
                    cursor.execute("UPDATE registration SET balance=? WHERE username=?", (new_sender_balance, sender_username))

                    # Update receiver's balance
                    cursor.execute("UPDATE registration SET balance=balance+? WHERE username=?", (amount, receiver_username))
                    
                    connection.commit()
                    connection.close()
                    message_label.config(text=f"Transferred {amount} to {receiver_username} successfully")
                else:
                    connection.close()
                    message_label.config(text="Insufficient balance or WRONG inputs")
            else:
                connection.close()
                message_label.config(text="Invalid sender or receiver username")
        except Exception as e:
            message_label.config(text="Database error: " + str(e))

    transfer_win = Tk()
    transfer_win.title("Transfer Page")

    head_lb = Label(transfer_win, text="TRANSFER WITHIN BANK", font=("bold", 16))
    head_lb.grid(row=0, column=1, padx=20, pady=10)

    sender_username_label = Label(transfer_win, text="Sender Username:", font=("bold", 12))
    sender_username_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
    sender_username_entry = Entry(transfer_win)
    sender_username_entry.grid(row=1, column=1, padx=20, pady=10)

    sender_password_label = Label(transfer_win, text="Sender Password:", font=("bold", 12))
    sender_password_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
    sender_password_entry = Entry(transfer_win, show="*")
    sender_password_entry.grid(row=2, column=1, padx=20, pady=10)

    receiver_username_label = Label(transfer_win, text="Receiver Username:", font=("bold", 12))
    receiver_username_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")
    receiver_username_entry = Entry(transfer_win)
    receiver_username_entry.grid(row=3, column=1, padx=20, pady=10)

    amount_label = Label(transfer_win, text="Amount:", font=("bold", 12))
    amount_label.grid(row=4, column=0, padx=20, pady=10, sticky="w")
    amount_entry = Entry(transfer_win)
    amount_entry.grid(row=4, column=1, padx=20, pady=10)

    transfer_button = Button(transfer_win, text="Transfer", bg="grey", fg="white", font=("bold", 12), command=authenticate_and_transfer)
    transfer_button.grid(row=5, column=1, padx=20, pady=10)

    message_label = Label(transfer_win, text="", fg="green")
    message_label.grid(row=6, column=1, padx=20, pady=10)

    transfer_win.mainloop()

def card_application_page():
    def submit_application():
        username = username_entry.get()
        card_type = card_type_combo.get()
        try:
            server = 'localhost\SQLEXPRESS'
            database = 'bank'
            connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
 
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            cursor.execute("SELECT username FROM  card_application WHERE username=?", (username,))
            existing_application = cursor.fetchone()

            if existing_application:
                cursor.execute("UPDATE card_application SET card_type=? WHERE username=?", (card_type, username))
                connection.commit()
                connection.close()
                messagebox.showinfo("Application Status", "Card type updated successfully.")
            else:
                cursor.execute("INSERT INTO card_application (username, card_type) VALUES (?, ?)", (username, card_type))
                connection.commit()
                connection.close()
                messagebox.showinfo("Application Status", "Card application submitted successfully.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))


    card_app_win = Tk()
    card_app_win.title("Card Application")

    head_label = Label(card_app_win, text="Apply for Card Services", font=("bold", 16))
    head_label.grid(row=0, column=1, padx=20, pady=10, columnspan=2)

    username_label = Label(card_app_win, text="Username:", font=("bold", 12))
    username_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")
    username_entry = Entry(card_app_win)
    username_entry.grid(row=1, column=1, padx=20, pady=10, columnspan=2)

    card_type_label = Label(card_app_win, text="Card Type:", font=("bold", 12))
    card_type_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")
    card_type_combo = ttk.Combobox(card_app_win, values=["Debit Card", "Credit Card"])
    card_type_combo.grid(row=2, column=1, padx=20, pady=10, columnspan=2)
    card_type_combo.set("Debit Card")

    submit_button = Button(card_app_win, text="Submit", bg="grey", fg="white", font=("bold", 12), command=submit_application)
    submit_button.grid(row=3, column=1, padx=20, pady=10)

    card_app_win.mainloop()

def modify_account_window():
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

    modify = Tk()
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

def forgot_password():
    global username,password

    def get_password():
        entered_email = email_entry.get()
        entered_contact = contact_entry.get()

        if not entered_email or not entered_contact:
            result_label.config(text="Please enter both email and contact.", fg="red")
            return

        connection = connect_to_database()
        if not connection:
            result_label.config(text="Database connection error.", fg="red")
            return

        cursor = connection.cursor()
        try:
            cursor.execute("SELECT username, password FROM registration WHERE email = ? AND phone = ?", (entered_email, entered_contact))
            user_data = cursor.fetchone()

            if user_data:
                username.set(user_data[0])
                password.set(user_data[1])
                result_label.config(text="Username and password found.", fg="green")
                username_entry.config(state='normal')
                username_entry.delete(0, 'end')
                username_entry.insert(0, username.get())
                username_entry.config(state='readonly')
                password_entry.config(state='normal')
                password_entry.delete(0, 'end')
                password_entry.insert(0, password.get())
                password_entry.config(state='readonly')
                
            else:
                result_label.config(text="No matching user found.", fg="red")
        except pyodbc.Error as e:
            print(f"Database error: {e}")
            result_label.config(text="Error retrieving data.", fg="red")
        finally:
            connection.close()

    forgot_password_window = Tk()
    forgot_password_window.title("Forgot Password")
    head=Label(forgot_password_window,text="FIND YOUR USERNAME AND PASSWORD",font=("bold",25),bg="SystemButtonFace").grid(row=0,padx=60,sticky="w")
    email_label = Label(forgot_password_window, text="Email:",font=("bold",16))
    email_label.grid(row=1,padx=60,sticky="w")

    email_entry = Entry(forgot_password_window)
    email_entry.grid(row=1,padx=200,sticky="w")

    contact_label = Label(forgot_password_window, text="Contact:",font=("bold",16))
    contact_label.grid(row=2,padx=60,sticky="w")

    contact_entry = Entry(forgot_password_window)
    contact_entry.grid(row=2,padx=200,sticky="w")

    retrieve_button = Button(forgot_password_window, text="Retrieve",command=get_password,fg="white",bg="grey",font=("bold",16))
    retrieve_button.grid(row=3,padx=60,sticky="w")

    result_label = Label(forgot_password_window, text="", fg="black",font=("bold",16))
    result_label.grid(row=4,padx=60,sticky="w")

    username = StringVar()
    password = StringVar()

    username_label = Label(forgot_password_window, text="Username:",font=("bold",16))
    username_label.grid(row=5,padx=60,sticky="w")

    username_entry = Entry(forgot_password_window, textvariable=username, state='readonly')
    username_entry.grid(row=5,padx=200,sticky="w")

    password_label = Label(forgot_password_window, text="Password:",font=("bold",16))
    password_label.grid(row=6,padx=60,sticky="w")

    password_entry = Entry(forgot_password_window, textvariable=password, state='readonly')
    password_entry.grid(row=6,padx=200,sticky="w")
    forgot_password_window.mainloop()

def inquire_user_details():
    global name,phone,email,gender,nationality,state,address,balance,card
    name = StringVar()
    phone = StringVar()
    email = StringVar()
    gender = StringVar()
    nationality = StringVar()
    state = StringVar()
    address = StringVar()
    balance = StringVar()
    card=StringVar()
    
    def get_user_details(): 
        
        entered_username = username_entry.get()
        print(f"Entered username: {entered_username}")  

        if not entered_username:
            messagebox.showerror('MISSING ',"ENTER USERNAME")
            return

        connection = connect_to_database()
        if not connection:
           messagebox.showerror('database error',"DATABASE ERROR")
           return

        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM registration WHERE username = ?", (entered_username,))
            user_data = cursor.fetchone()

            
            if user_data:
                name.set(user_data[0])
                phone.set(user_data[1])
                email.set(user_data[2])
                gender.set(user_data[3])
                nationality.set(user_data[4])
                state.set(user_data[5])
                address.set(user_data[6])
                balance.set(user_data[10])
                cursor.execute("SELECT card_type FROM card_application WHERE username = ?", (entered_username,))
                card_data = cursor.fetchone()
                if card_data:
                    card.set(card_data[0])
                else:
                    card.set("NO data found")  
                    messagebox.showinfo('FOUND', f"USER FOUND: {entered_username}")
                messagebox.showinfo('FOUND',f"USER FOUND: {entered_username}")  
                name_entry.config(state='normal')
                name_entry.delete(0, 'end')
                name_entry.insert(0, name.get())
                name_entry.config(state='readonly')
                phone_entry.config(state='normal')
                phone_entry.delete(0, 'end')
                phone_entry.insert(0, phone.get())
                phone_entry.config(state='readonly')
                email_entry.config(state='normal')
                email_entry.delete(0, 'end')
                email_entry.insert(0, email.get())
                email_entry.config(state='readonly')
                gender_entry.config(state='normal')
                gender_entry.delete(0, 'end')
                gender_entry.insert(0, gender.get())
                gender_entry.config(state='readonly')
                nationality_entry.config(state='normal')
                nationality_entry.delete(0, 'end')
                nationality_entry.insert(0, nationality.get())
                nationality_entry.config(state='readonly')
                state_entry.config(state='normal')
                state_entry.delete(0, 'end')
                state_entry.insert(0, state.get())
                state_entry.config(state='readonly')
                address_entry.config(state='normal')
                address_entry.delete(0, 'end')
                address_entry.insert(0, address.get())
                address_entry.config(state='readonly')
                balance_entry.config(state='normal')
                balance_entry.delete(0, 'end')
                balance_entry.insert(0, balance.get())
                balance_entry.config(state='readonly')
                card_entry.config(state='normal')
                card_entry.delete(0, 'end')
                card_entry.insert(0, card.get())
                card_entry.config(state='readonly')
            else:
                messagebox.showinfo('NOT FOUND...',f"NO MATCHING INFO FOUND FOR : {entered_username}")
        except pyodbc.Error as e:
            print(f"Database error: {e}")
            messagebox.showinfo('DATABASE ERROR',"DATABASE ERROR")
        finally:
            connection.close()
    
    inquire_details_window = Tk()
    inquire_details_window.title("Inquire User Details")
    head_lb=Label(inquire_details_window,text="ENQUIRY DATA.....",font=("bold",25))
    head_lb.grid(row=0,padx=60,sticky="w")
    username_label = Label(inquire_details_window, text="Username:",font=("Ariel",16))
    username_label.grid(row=1,padx=60,sticky="w")

    username_entry = Entry(inquire_details_window)
    username_entry.grid(row=1,padx=200,sticky="w")

    retrieve_button = Button(inquire_details_window, text="Retrieve", command=get_user_details,font=("Ariel",16,'bold'),bg="grey",fg="white")
    retrieve_button.grid(row=2,padx=100,sticky="w")
    

    name_label = Label(inquire_details_window, text="Name:",font=("Ariel",16))
    name_label.grid(row=3,padx=60,sticky="w")
    name_entry = Entry(inquire_details_window, textvariable=name, state='readonly')
    name_entry.grid(row=3,padx=200,sticky="w")
    phone_label = Label(inquire_details_window, text="Phone:",font=("Ariel",16))
    phone_label.grid(row=4,padx=60,sticky="w")
    phone_entry = Entry(inquire_details_window, textvariable=phone, state='readonly')
    phone_entry.grid(row=4,padx=200,sticky="w")
    email_label = Label(inquire_details_window, text="Email:",font=("Ariel",16))
    email_label.grid(row=5,padx=60,sticky="w")
    email_entry = Entry(inquire_details_window, textvariable=email, state='readonly')
    email_entry.grid(row=5,padx=200,sticky="w")
    gender_label = Label(inquire_details_window, text="Gender:",font=("Ariel",16))
    gender_label.grid(row=6,padx=60,sticky="w")
    gender_entry = Entry(inquire_details_window, textvariable=gender, state='readonly')
    gender_entry.grid(row=6,padx=200,sticky="w")
    nationality_label = Label(inquire_details_window, text="Nationality:",font=("Ariel",16))
    nationality_label.grid(row=7,padx=60,sticky="w")
    nationality_entry = Entry(inquire_details_window, textvariable=nationality, state='readonly')
    nationality_entry.grid(row=7,padx=200,sticky="w")
    state_label = Label(inquire_details_window, text="State:",font=("Ariel",16))
    state_label.grid(row=8,padx=60,sticky="w")
    state_entry = Entry(inquire_details_window, textvariable=state, state='readonly')
    state_entry.grid(row=8,padx=200,sticky="w")
    address_label = Label(inquire_details_window, text="Address:",font=("Ariel",16))
    address_label.grid(row=9,padx=60,sticky="w")
    address_entry = Entry(inquire_details_window, textvariable=address, state='readonly')
    address_entry.grid(row=9,padx=200,sticky="w")
    balance_label = Label(inquire_details_window, text="Balance:",font=("Ariel",16))
    balance_label.grid(row=11,padx=60,sticky="w")
    balance_entry = Entry(inquire_details_window, textvariable=balance, state='readonly')
    balance_entry.grid(row=11,padx=200,sticky="w")
    card_label = Label(inquire_details_window, text="Card:",font=("Ariel",16))
    card_label.grid(row=12,padx=60,sticky="w")
    card_entry = Entry(inquire_details_window, textvariable=card, state='readonly')
    card_entry.grid(row=12,padx=200,sticky="w")

    inquire_details_window.mainloop()

def expense_predictor():
    def linear_regression():
        age_val = int(age_entry.get())
        income_val = int(income_entry.get())
        gender_val = gender_var.get()

        dataset = pd.read_csv('Ecom Expense.csv')

        dataset = pd.get_dummies(dataset, columns=['Gender'], drop_first=True)

        X = dataset[['Age ', 'Monthly Income', 'Gender_Male']]
        y = dataset['Total Spend']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

        model = LinearRegression()
        model.fit(X_train, y_train)

        gender_mapping = {'Male': 1, 'Female': 0}
        gender_display = 'Male' if gender_val == 1 else 'Female'

        predicted_total_spent = model.predict([[age_val, income_val, gender_val]])
        spent.set(f"{int(predicted_total_spent[0])}")
        spend_entry.config(state='normal')
        spend_entry.delete(0, 'end')
        spend_entry.insert(0, spent.get())
        spend_entry.config(state='readonly')

        '''if(income_val==0):
            label=Label(expense_window,text=f"BHAI TERI INCOME  {income_val} itni h kamana shuru kar kab tak baap ke tukdo pe palega ",font=(16),fg='red').grid(row=6,sticky="w",padx=60,pady=10)'''
        

    expense_window = Tk()
    expense_window.title("Expense Predictor")
    spent = StringVar()
    age_var = StringVar()
    income_var = StringVar()
    gender_var = IntVar()

    label = Label(expense_window, text="Enter Your Details to Predict Total Spend:", font=("Arial", 16))
    label.grid(row=0, sticky="w", padx=10)

    age_lb = Label(expense_window, text="AGE", font=("Arial", 16))
    age_lb.grid(row=1, sticky="w", padx=10, pady=6)
    age_entry = Entry(expense_window, textvariable=age_var)
    age_entry.grid(row=1, sticky="w", padx=250)

    income_lb = Label(expense_window, text="MONTHLY INCOME", font=("Arial", 16))
    income_lb.grid(row=2, sticky="w", padx=10, pady=6)
    income_entry = Entry(expense_window, textvariable=income_var)
    income_entry.grid(row=2, sticky="w", padx=250)

    gender_lb = Label(expense_window, text="GENDER", font=("Arial", 16))
    gender_lb.grid(row=3, sticky="w", padx=10, pady=6)
    male_rb = Radiobutton(expense_window, text="Male", variable=gender_var, value=1)
    male_rb.grid(row=3, sticky="w", padx=250)
    female_rb = Radiobutton(expense_window, text="Female", variable=gender_var, value=0)
    female_rb.grid(row=3, sticky="w",padx=300)

    predict_button = Button(expense_window, text="Predict", bg="grey", fg="white", font=("Arial", 16), command=linear_regression)
    predict_button.grid(row=4, sticky="w", padx=50, ipadx=2, ipady=2)

    spent_lb = Label(expense_window, text="TOTAL SPEND", font=("Arial", 16))
    spent_lb.grid(row=5, sticky="w", padx=10)
    spend_entry = Entry(expense_window, textvariable=spent)
    spend_entry.grid(row=5, sticky="w", padx=250)

    expense_window.mainloop()

def services():
    services=Tk()
    services.title("SERVICES")
    heading=Label(services,text="SERVICES",font=("Arial",25),bg="SystemButtonFace").grid(row=0,padx=10,sticky="w")
    deposit_btn=Button(services,text="DEPOSIT",font=("Arial",16),bd=1,fg="white",bg="grey",command=deposit_page).grid(row=1,padx=10,sticky="w",pady=10)
    withraw_btn=Button(services,text="WITHDRAW",font=("Arial",16),bd=1,fg="white",bg="grey",command=withdraw_page).grid(row=1,padx=200,sticky="w",pady=10)
    transfer_btn=Button(services,text="TRANSFER",font=("Arial",16),bd=1,fg="white",bg="grey",command=transfer_page).grid(row=1,padx=450,sticky="w",pady=10)
    calculator_btn=Button(services,text="CALCULATOR",font=("Arial",16),bd=1,fg="white",bg="grey",command=calculator).grid(row=2,padx=10,sticky="w")
    enquiry_btn=Button(services,text="ENQUIRY",font=("Arial",16),bd=1,fg="white",bg="grey",command=inquire_user_details).grid(row=2,padx=200,sticky="w",pady=10)
    services.mainloop()

def navigate(label):
    if label == "SERVICES":
        services()
        print("Services function called")
    elif label == "EXPENSE PREDICTOR":
        expense_predictor()
        print("Expense Predictor function called")
    elif label == "CARD SERVICES":
        card_application_page()
        print("card application window opened")
    elif label == "MODIFY ACCOUNT":
        modify_account_window()
        print("Modify Account function called")
    elif label == "HISTORY":
        print("History function called")

def profile(username):
    profile = Tk()
    profile.title("PROFILE PAGE ")
    def update_time():
        current_time = datetime.now().strftime("%H:%M:%S %d %Y-%m")
        time_label.config(text=current_time)
        profile.after(1000, update_time)

    time_label = Label(profile, font=("Helvetica", 20), bg="SystemButtonFace")
    time_label.grid(row=0, pady=6, padx=6, sticky="w")
    update_time()


    head_lb = Label(profile, text="VISHNU LEGACY BANK", font=(
        "Helvetica", 35), bg="SystemButtonFace", bd=0)
    head_lb.grid(row=3, sticky="w", padx=100)

    nav_frame = Frame(profile, bg="gray")
    nav_frame.grid(row=4, pady=20, sticky="we")
    profile.columnconfigure(0, weight=1)
    nav_links = ["Services", "Expense Predictor", "card services", "Modify Account", "history"]
    nav_links = [link.upper() for link in nav_links]
    for i, link in enumerate(nav_links):
        link_button = Button(nav_frame, text=link, command=lambda l=link: navigate(l), font=("Helvetica", 16))
        link_button.grid(row=4, column=i, padx=60, pady=10)

    login_btn = Button(profile, text="LOGOFF", font=(
        "Helvetica", 20), bg="SystemButtonFace", bd=0)
    login_btn.grid(row=0, pady=6, padx=6, sticky="ne")
    user_data = fetch_user_data(username)
    user_name_label = Label(profile, text=f"Name: {user_data['Name']}", font=("Arial", 20))
    user_name_label.grid(row=5, padx=100, sticky="w",pady=50)

    dob_label = Label(profile, text=f"Date of Birth: {user_data['DOB']}", font=("Arial", 20))
    dob_label.grid(row=6, padx=100, sticky="w",pady=10)

    contact_no_label = Label(profile, text=f"Contact No.: {user_data['Phone']}", font=("Arial", 20))
    contact_no_label.grid(row=7, padx=100, sticky="w",pady=20)

    email_label = Label(profile, text=f"Email: {user_data['Email']}", font=("Arial", 20))
    email_label.grid(row=8, padx=100, sticky="w",pady=30)
    profile.mainloop()

def login_data(username, password):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            query = "SELECT * FROM registration WHERE username = ? AND password = ?"
            cursor.execute(query, (username, password))
            registration = cursor.fetchone()

            if registration:
                profile(username)
            else:
                messagebox.showinfo(
                    "Login Failed", "Login failed for username: " + username)
        except pyodbc.Error as e:
            print(f"Error executing SQL query: {e}")
        finally:
            connection.close()

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

        if login_data(entered_username, entered_password):
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
    
    forget_btn = Button(login_window, text="FORGET PASSWORD", bg="SystemButtonFace", bd=0, font=("Arial", 16),command=forgot_password)
    forget_btn.grid(row=4, padx=800, sticky="w")
    login_window.mainloop()
