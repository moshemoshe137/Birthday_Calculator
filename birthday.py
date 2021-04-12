import datetime as dt
import tkinter as tk

import dateutil.parser
import dateutil.relativedelta


def pretty_date(date):
    # determine the suffix for pretty date printing
    # https://stackoverflow.com/questions/5891555/display-the-date-like-may-5th-using-pythons-strftime
    suffix = "th" if 11 <= date.day <= 13 else {1: "st", 2: "nd", 3: "rd"}.get(date.day % 10, "th")
    return f"{date:%A, %B {date.day}{suffix}, %Y}"


def calculate_age(birthday_string, on_date=dt.date.today()):
    if isinstance(birthday_string, dt.date) or isinstance(birthday_string, dt.datetime):
        # if we are already passed a date or datetime object, leave it be
        birthday = birthday_string
    else:
        # otherwise, try to parse the string
        try:
            birthday = dateutil.parser.parse(birthday_string).date()
        except dateutil.parser.ParserError as e:
            print("Error: Invalid Date")
            return e

    output_string = ""

    age = dateutil.relativedelta.relativedelta(on_date, birthday)
    age_days = (on_date - birthday).days

    output_string += f"I understood your birthday as {pretty_date(birthday)}.\n" + "\n"

    output_string += f"You are {age.years} years old" + "\n"
    output_string += f"     or {age.years} years, {age.months} months, and {age.days} days old" + "\n"
    output_string += f"     or {age.years * 12 + age.months:,} months and {age.days} days old" + "\n"
    output_string += f"     or {age_days // 7:,} weeks and {age.days % 7} days old" + "\n"
    output_string += f"     or {age_days:,} days old." + "\n"

    offset = " " * (len(f"At midnight on {pretty_date(on_date)} you were ") - len("or "))
    output_string += f"At midnight on {pretty_date(on_date)} you were {age_days * 24:,} hours old" + "\n"
    output_string += f"{offset}or {age_days * 24 * 60:,} minutes old" + "\n"
    output_string += f"{offset}or {age_days * 24 * 60 * 60:,} seconds old." + "\n"

    if dt.date(on_date.year, birthday.month, birthday.day) <= on_date:
        # if their birthday is before the on_date
        # then they have already had a birthday this year
        next_birthday = dt.date(on_date.year + 1, birthday.month, birthday.day)
    else:
        next_birthday = dt.date(on_date.year, birthday.month, birthday.day)
    output_string += f"Your next birthday is on {pretty_date(next_birthday)}, in {(next_birthday - on_date).days} days.\n" + "\n"

    return output_string


def birthday_calculator():
    def handle_submit(event=None):
        birthday = ent_birthday.get()
        string = calculate_age(birthday)
        lbl_result['text'] = string

    window = tk.Tk()
    window.title("Birthday Calculator")

    frm_input = tk.Frame(
        master=window,
        relief=tk.SUNKEN,
        borderwidth=3
    )

    lbl_birthday = tk.Label(master=frm_input, text="Please enter your birthday: ")
    lbl_birthday.grid(row=0, column=0, sticky="nsew")

    ent_birthday = tk.Entry(master=frm_input, width=20)
    ent_birthday.grid(row=0, column=1, sticky="nsew")

    btn_submit = tk.Button(master=frm_input, text="Submit", command=handle_submit)
    btn_submit.grid(row=0, column=2, sticky="nsew")

    lbl_result = tk.Label(master=window, text="", justify=tk.LEFT)

    frm_input.grid(row=0, column=0, padx=5, pady=5, sticky="nsew", ipadx=2, ipady=2)
    lbl_result.grid(row=1, column=0, sticky="nsew")

    # make everything resizable
    print(frm_input.grid_size())
    print(window.grid_size())
    for row in range(frm_input.grid_size()[1]):
        frm_input.rowconfigure(row, weight=1)
    for row in range(window.grid_size()[1]):
        window.rowconfigure(row, weight=(1 if row == 0 else 3))
    for col in range(frm_input.grid_size()[0]):
        frm_input.columnconfigure(col, weight=1)
    for col in range(window.grid_size()[0]):
        window.columnconfigure(col, weight=1)

    window.bind("<Return>", handle_submit)

    tk.mainloop()
