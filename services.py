
import pyodbc
from tkinter import*
from tkinter import ttk
from tkinter import messagebox
import databaseconnet as db


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
                cursor.execute("UPDATE registration SET balance=balance+? WHERE username=?", (amount, username))
                connection.commit()
                connection.close()
                message_label.config(text=f"Deposited {amount} successfully for {username}")
            else:
                connection.close()
                message_label.config(text="Invalid username or password")
        except Exception as e:
            message_label.config(text="Database error: " + str(e))

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

    find_button = Button(depo_win, text="Find", bg="grey", fg="white",font=("bold",16) , command=authenticate_and_deposit)
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

            cursor.execute("SELECT username, password, balance FROM registration WHERE username=? AND password=?", (username, password))
            user_data = cursor.fetchone()

            if user_data:
                current_balance = user_data[2]
                if current_balance >= float(amount):
                    new_balance = current_balance - float(amount)
                    cursor.execute("UPDATE registration SET balance=? WHERE username=?", (new_balance, username))
                    connection.commit()
                    connection.close()
                    message_label.config(text=f"Withdrawn {amount} successfully for {username}")
                else:
                    connection.close()
                    message_label.config(text="Insufficient balance")
            else:
                connection.close()
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
        # Get data from the entry widgets
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
                if sender_balance >= float(amount):
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
                    message_label.config(text="Insufficient balance")
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
        # Get data from the entry widgets
        username = username_entry.get()
        card_type = card_type_combo.get()

        try:
            server = 'localhost\SQLEXPRESS'
            database = 'bank'
            connection_string = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
        
            connection = pyodbc.connect(connection_string)
            cursor = connection.cursor()

            # Check if the user already applied for a card
            cursor.execute("SELECT username FROM registration WHERE username=?", (username,))
            existing_application = cursor.fetchone()

            if existing_application:
                connection.close()
                messagebox.showinfo("Application Status", "You already applied for a card.")
            else:
                # Insert the card application into the database
                cursor.execute("INSERT INTO registration (username, card_type) VALUES (?, ?)", (username, card_type))
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

    def update_user_info(username, field, new_value):
        connection = connect_to_database()
        if not connection:
            return
        
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT username FROM registration WHERE username = ?", (username,))
            existing_username = cursor.fetchone()

            if existing_username:
            
                cursor.execute(f"UPDATE registration SET {field} = ? WHERE username = ?", (new_value, username))
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
    
        if not username or not field or not new_value:
            status_label.config(text="Please fill in all fields.", fg="red")
            return
    
        update_user_info(username, field, new_value)

    modify = Tk()
    modify.title("Modify Account Information")
    head_lb = Label(modify, text="MODIFY YOUR ACCOUNT", font=("Helvetica", 25), bg="SystemButtonFace")
    head_lb.grid(row=0, sticky="w", padx=40, pady=10)
    frame = Frame(modify, padx=20, pady=20)
    frame.grid()
    username_label = Label(frame, text="Username:", font=("Helvetica", 16), bg="SystemButtonFace")
    username_label.grid(row=0, sticky="w", padx=60)

    global username_var
    username_var = StringVar()
    username_entry = Entry(frame, textvariable=username_var)
    username_entry.grid(row=0, sticky="w", padx=250)

    field_label = Label(frame, text="Modify", font=("bold", 16), bg="SystemButtonFace")
    field_label.grid(row=1, sticky="w", padx=60)

    fields = ["name", "phone", "email", "gender", "nationality", "state", "address"]
    global field_var
    field_var = StringVar()
    field_dropdown = OptionMenu(frame, field_var, *fields)
    field_dropdown.grid(row=1, sticky="w", padx=250)

    entry_label = Label(frame, text="New Value:", font=("Helvetica", 16), bg="SystemButtonFace")
    entry_label.grid(row=3, sticky="w", padx=60)

    global entry_var
    entry_var = StringVar()
    entry = Entry(frame, textvariable=entry_var)
    entry.grid(row=3, sticky="w", padx=250)
    modify_button = Button(frame, text="Modify", command=modify_account, font=("Helvetica", 16, "bold"), bg="grey", fg="white")
    modify_button.grid(row=5, sticky="w", padx=60)

    global status_label
    status_label = Label(frame, text="", fg="green", font=("Helvetica", 16), bg="SystemButtonFace")
    status_label.grid(row=6, columnspan=2)

    modify.mainloop()

def forgot_password():
    def get_password():
        entered_email = email_entry.get()
        entered_contact = contact_entry.get()

        if not entered_email or not entered_contact:
            result_label.config(text="Please enter both email and contact.", fg="red")
            return

        connection = db.connect_to_database()
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
    def get_user_details():
        entered_username = username_entry.get()
        print(f"Entered username: {entered_username}")  # Debugging

        if not entered_username:
            result_label.config(text="Please enter a username.", fg="red")
            return

        connection = db.connect_to_database()
        if not connection:
            result_label.config(text="Database connection error.", fg="red")
            return

        cursor = connection.cursor()
        try:
            cursor.execute("SELECT * FROM registration WHERE username = ?", (entered_username,))
            user_data = cursor.fetchone()
            print(f"Retrieved user data: {user_data}")  
            if user_data:
                name.set(user_data[0])
                phone.set(user_data[1])
                email.set(user_data[2])
                gender.set(user_data[3])
                nationality.set(user_data[4])
                state.set(user_data[5])
                address.set(user_data[6])
                balance.set(user_data[7])
                result_label.config(text="User details retrieved successfully.", fg="green")
            else:
                result_label.config(text="No matching user found.", fg="red")
        except pyodbc.Error as e:
            print(f"Database error: {e}")
            result_label.config(text="Error retrieving data.", fg="red")
        finally:
            connection.close()
    
    inquire_details_window = Tk()
    inquire_details_window.title("Inquire User Details")

    username_label = Label(inquire_details_window, text="Username:")
    username_label.grid()

    username_entry = Entry(inquire_details_window)
    username_entry.grid()

    retrieve_button = Button(inquire_details_window, text="Retrieve", command=get_user_details)
    retrieve_button.grid()

    result_label = Label(inquire_details_window, text="", fg="black")
    result_label.grid()

    name = StringVar()
    phone = StringVar()
    email = StringVar()
    gender = StringVar()
    nationality = StringVar()
    state = StringVar()
    address = StringVar()
    balance = StringVar()

    name_label = Label(inquire_details_window, text="Name:")
    name_label.grid()

    name_entry = Entry(inquire_details_window, textvariable=name, state='readonly')
    name_entry.grid()

    phone_label = Label(inquire_details_window, text="Phone:")
    phone_label.grid()

    phone_entry = Entry(inquire_details_window, textvariable=phone, state='readonly')
    phone_entry.grid()

    email_label = Label(inquire_details_window, text="Email:")
    email_label.grid()

    email_entry = Entry(inquire_details_window, textvariable=email, state='readonly')
    email_entry.grid()

    gender_label = Label(inquire_details_window, text="Gender:")
    gender_label.grid()

    gender_entry = Entry(inquire_details_window, textvariable=gender, state='readonly')
    gender_entry.grid()

    nationality_label = Label(inquire_details_window, text="Nationality:")
    nationality_label.grid()

    nationality_entry = Entry(inquire_details_window, textvariable=nationality, state='readonly')
    nationality_entry.grid()

    state_label = Label(inquire_details_window, text="State:")
    state_label.grid()

    state_entry = Entry(inquire_details_window, textvariable=state, state='readonly')
    state_entry.grid()

    address_label = Label(inquire_details_window, text="Address:")
    address_label.grid()

    address_entry = Entry(inquire_details_window, textvariable=address, state='readonly')
    address_entry.grid()

    balance_label = Label(inquire_details_window, text="Balance:")
    balance_label.grid()

    balance_entry = Entry(inquire_details_window, textvariable=balance, state='readonly')
    balance_entry.grid()





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


modify_account_window()