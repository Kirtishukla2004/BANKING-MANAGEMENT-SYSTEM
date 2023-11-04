from datetime import datetime
from tkinter import *
from PIL import Image, ImageTk
'''import databaseconnet as db
import otherfunctions as ot'''
import pyodbc
from tkinter import messagebox
from tkinter import Label ,Button
import mainpage as mp


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


def insert_data(name, phone, email, gender, nationality, state, address, password,username, dob):
    connection = connect_to_database()
    if connection:
        try:
            cursor = connection.cursor()
            sql_insert = """
            INSERT INTO registration(Name, Phone, Email, Gender, Nationality, State, Address, Password,Username, DOB)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            values = (name, phone, email, gender, nationality,
                      state, address, password, username,dob)

            cursor.execute(sql_insert, values)
            connection.commit()
            cursor.close()
            print("Data inserted successfully")  # Add this line

            messagebox.showinfo(
                "welcome ", "vishnu legacy bank : " + username)

        except pyodbc.Error as e:
            print(f"Error inserting data: {e}")
        finally:
            connection.close()

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
        'Contact_no': '',
        'Email': '',
    }


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
        link_button = Button(nav_frame, text=link, command=lambda l=link: mp.navigate(l), font=("Helvetica", 16))
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
