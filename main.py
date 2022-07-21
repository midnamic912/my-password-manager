from tkinter import *
from tkinter import messagebox
from random import choice, shuffle, randint
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project

def generate_pw():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letter_list = [choice(letters) for _ in range(randint(8, 10))]
    symbol_list = [choice(symbols) for _ in range(randint(2, 4))]
    number_list = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = letter_list + symbol_list + number_list
    # todo: Lists can plus each other and become a new list directly
    shuffle(password_list)

    password = "".join(password_list)

    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website_input = website_entry.get()
    username_input = username_entry.get()
    password_input = password_entry.get()
    new_data = {
        website_input: {
            "username": username_input,
            "password": password_input
        }
    }

    if len(website_input) == 0 or len(username_input) == 0 or len(password_input) == 0:
        messagebox.showinfo(title="Warning", message="Please don't leave any fields empty!")
        window.focus()
        website_entry.focus()

    else:
        try:
            with open("data.json", "r") as data_file:
                data_dict = json.load(data_file)  # todo: convert a existing json file to a dict
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            if website_input in data_dict:
                messagebox.showinfo(title="Notice", message="Data of the website is already exist.\n"
                                                            "Password has been updated.")
            data_dict.update(new_data)  # todo: update the dict

            with open("data.json", "w") as data_file:
                json.dump(data_dict, data_file, indent=4)  # todo: convert the dict to json
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            website_entry.focus()


# --------------------------- SEARCH PASSWORD ------------------------- #
def find_password():
    website_input = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data_dict = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Oops!", message="No Data File Found.")
    else:
        if website_input in data_dict:
            username = data_dict[website_input]["username"]
            password = data_dict[website_input]["password"]
            messagebox.showinfo(title="Result", message=f"Username:\n{username}\nPassword:\n{password}")
        else:
            messagebox.showinfo(title="Oops!", message=f"No details for {website_input} exists.")
    finally:
        window.focus()
        website_entry.focus()


# ---------------------------- UI SETUP ------------------------------- #

# window

window = Tk()
window.config(padx=50, pady=50)
window.title("Password Manager by Midna")

# canvas
canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="cat_lock.png", width=200, height=189)
canvas.create_image(138, 95, image=logo_img)
canvas.grid(column=1, row=0)

# labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
username_label = Label(text="Username/Email:")
username_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# entries
website_entry = Entry(width=21)
website_entry.focus()
website_entry.grid(column=1, row=1)

username_entry = Entry(width=38)
username_entry.insert(0, "midnamic912@gmail.com")
username_entry.grid(column=1, row=2, columnspan=2)
password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)

# buttons
generate_pw_button = Button(text="Generate Password", command=generate_pw)
generate_pw_button.grid(column=2, row=3)
add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)
search_button = Button(text="Search", width=13, command=find_password)
search_button.grid(column=2, row=1)

window.mainloop()
