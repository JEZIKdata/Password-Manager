from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]

    password_list = password_symbols + password_numbers + password_letters
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty.")
    else:
        is_ok = messagebox.askokcancel(title=website,
                                       message=f"These are entered details:\n email: {email}\n password: {password}\n "
                                               f"Do you want to save it?")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- FINDING PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="error", message="No data file found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"email: {email}\npassword: {password}")
        else:
            messagebox.showinfo(title="error", message="No details for the website exists.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=30, pady=30)

canvas = Canvas(width=200, height=200)
lock = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

website_entry = Entry(width=23)
website_entry.focus()
website_entry.grid(column=1, row=1)

email_entry = Entry(width=43)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "miroslava.jezikovahk@gmail.com")

password_entry = Entry(width=23)
password_entry.grid(column=1, row=3)

password_button = Button(text="Generate Password", width=15, command=generate_password)
password_button.grid(column=2, row=3)

add_button = Button(text="Add", width=38, command=save)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", width=10, command=find_password)
search_button.grid(column=2, row=1)

window.mainloop()
