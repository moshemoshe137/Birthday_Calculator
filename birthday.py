import datetime as dt

import dateutil.parser
import dateutil.relativedelta

import tkinter as tk


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
            raise e
            return -1

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


