import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk 
import random

# Define a dictionary of rules and responses
rules = {
    "hello": ["Namaste!", "Hello!", "Hey!"],
    "hi": ["hi", "Hello!", "Hey!"],
    "jai jai shree ram": ["jai shree ram!", "ram ram!", "Hare ram!"],
    "how are you": ["I'm doing well, thanks!", "I'm just a bot, so I don't have feelings, but I'm here to help!"],
    "what's your name": ["I'm a chatbot.", "I don't have a name, but you can call me ChatBot."],
    "bye": ["Goodbye!", "See you later!", "Have a great day!"],
    "how old are you": ["I don't have an age. I'm just a computer program.", "I exist in the digital realm, so I don't age."],
    "what is your purpose": ["My purpose is to assist you with information and answer your questions to the best of my knowledge."],
    "eligibility for insurance": ["Insurance eligibility depends on various factors such as your age, health, and the type of insurance you are interested in. It's best to contact our customer support for detailed information."],
    "apply for card services": ["You can apply for card services by visiting our nearest branch or by filling out an online application form on our website. Make sure to provide all the necessary documents."],
    "convert normal account to fixed account": ["To convert a normal account to a fixed account, you need to visit our branch and speak to our customer service representative. They will guide you through the process."],
    "available schemes": ["We offer a variety of schemes, including savings accounts, fixed deposits, and investment plans. Please visit our website or contact our customer support for more details."],
    "check profile": ["You can check your profile by logging into your online account on our website or by visiting our nearest branch and asking our staff for assistance."],
    "reset password": ["To reset your password, visit our website and click on the 'Forgot Password' link on the login page. Follow the instructions to reset your password."],
}


entry = None
chatbox = None

# Function to generate a response
def generate_response(user_input):
    for key in rules:
        if key in user_input:
            return random.choice(rules[key])
    return "I'm sorry, I don't understand that."

# Function to handle user input
def send_message():
    global entry, chatbox
    user_input = entry.get().lower()
    if user_input == "exit":
        chatbox.config(state=tk.NORMAL)
        chatbox.insert(tk.END, "You: " + user_input + "\n")
        chatbox.insert(tk.END, "ChatBot: Goodbye!\n")
        chatbox.config(state=tk.DISABLED)
        entry.config(state=tk.DISABLED)
    else:
        response = generate_response(user_input)
        chatbox.config(state=tk.NORMAL)
        chatbox.insert(tk.END, "You: " + user_input + "\n")
        chatbox.insert(tk.END, "ChatBot: " + response + "\n")
        chatbox.config(state=tk.DISABLED)
        entry.delete(0, tk.END)

# Create the main window
root = tk.Tk()
root.title("ChatBot")
root.geometry("400x500")

# Resize the chatbot image
original_image = Image.open("chatbot.png")
resized_image = original_image.resize((100, 100), Image.ANTIALIAS)  # Adjust the size as needed

# Convert the resized image to PhotoImage format
chatbot_image = ImageTk.PhotoImage(resized_image)

# Function to open chatbot window
def open_chatbot_window():
    global entry, chatbox
    chatbot_window = tk.Toplevel(root)
    chatbot_window.title("ChatBot")
    chatbot_window.geometry("400x500")

    chatbot_label = tk.Label(chatbot_window, image=chatbot_image)
    chatbot_label.pack()

    greeting_label = tk.Label(chatbot_window, text="Namaste!", fg="black", font=("Arial", 12))
    greeting_label.pack()

    chatbox = tk.Text(chatbot_window, state=tk.DISABLED)
    chatbox.pack()

    entry = tk.Entry(chatbot_window)
    entry.pack()

    send_button = tk.Button(chatbot_window, text="Send", command=send_message)
    send_button.pack()


chatbot_button = tk.Button(root, image=chatbot_image, command=open_chatbot_window)
chatbot_button.pack()

root.mainloop()
