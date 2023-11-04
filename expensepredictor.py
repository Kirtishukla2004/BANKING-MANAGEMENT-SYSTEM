from tkinter import *
import pandas as pd
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def expense_predictor():
    def linear_regression():
        age_val = int(age_entry.get())
        income_val = int(income_entry.get())
        gender_val = gender_var.get()

        dataset = pd.read_csv('Ecom Expense.csv')

        dataset = pd.get_dummies(dataset, columns=['Gender'], drop_first=True)

        X = dataset[['Age ', 'Monthly Income', 'Gender']]
        y = dataset['Total Spend']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

        model = LinearRegression()
        model.fit(X_train, y_train)

        gender_mapping = {'Male': 1, 'Female': 0}
        gender_display = 'Male' if gender_val == 1 else 'Female'

        predicted_total_spent = model.predict([[age_val, income_val, gender_val]])
        spent.set(f"{int(predicted_total_spent[0])}")

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
    age_entry.grid(row=1, sticky="w", padx=200)

    income_lb = Label(expense_window, text="MONTHLY INCOME", font=("Arial", 16))
    income_lb.grid(row=2, sticky="w", padx=10, pady=6)
    income_entry = Entry(expense_window, textvariable=income_var)
    income_entry.grid(row=2, sticky="w", padx=250)

    gender_lb = Label(expense_window, text="GENDER", font=("Arial", 16))
    gender_lb.grid(row=3, sticky="w", padx=10, pady=6)
    male_rb = Radiobutton(expense_window, text="Male", variable=gender_var, value=1)
    male_rb.grid(row=3, sticky="w", padx=200)
    female_rb = Radiobutton(expense_window, text="Female", variable=gender_var, value=0)
    female_rb.grid(row=3, sticky="w",padx=250)

    predict_button = Button(expense_window, text="Predict", bg="grey", fg="white", font=("Arial", 16), command=linear_regression)
    predict_button.grid(row=4, sticky="w", padx=50, ipadx=2, ipady=2)

    spent_lb = Label(expense_window, text="TOTAL SPEND", font=("Arial", 16))
    spent_lb.grid(row=5, sticky="w", padx=10)
    spend_entry = Entry(expense_window, textvariable=spent)
    spend_entry.grid(row=5, sticky="w", padx=200)

    expense_window.mainloop()

