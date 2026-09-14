import calendar
import json
import os
from datetime import datetime

FILE = "attendance.json"

if os.path.exists(FILE):
    with open(FILE, "r") as file:
        data = json.load(file)
else:
    data = {}

if not data:
    print("No attendance data found.")
    exit()

subjects = list(data.keys())

print("==============================")
print("      ATTENDANCE CALENDAR")
print("==============================")

for i, subject in enumerate(subjects, 1):
    print(f"{i}. {subject}")

choice = input("\nChoose subject: ")

if not choice.isdigit() or not 1 <= int(choice) <= len(subjects):
    print("Invalid choice!")
    exit()

subject = subjects[int(choice) - 1]
records = data[subject]

today = datetime.now()
year = today.year
month = today.month

while True:

    print("\033[2J\033[H", end="")

    print("==============================")
    print("      ATTENDANCE CALENDAR")
    print("==============================")
    print("Subject:", subject)
    print()

    print(calendar.month(year, month))

    print("Attendance records:")

    found = False

    for date, status in sorted(records.items()):

        day = datetime.strptime(date, "%d-%m-%Y")

        if day.year == year and day.month == month:

            found = True

            if status == "P":
                print(f"{date}: ✅ Present")

            elif status == "A":
                print(f"{date}: ❌ Absent")

            elif status == "H":
                print(f"{date}: 🏖️ Holiday")

    if not found:
        print("No records this month.")

    print("\n------------------------------")
    print("1. Previous month")
    print("2. Next month")
    print("3. Today")
    print("4. Change subject")
    print("5. Exit")

    option = input("\nChoose: ")

    if option == "1":

        month -= 1

        if month == 0:
            month = 12
            year -= 1

    elif option == "2":

        month += 1

        if month == 13:
            month = 1
            year += 1

    elif option == "3":

        year = today.year
        month = today.month

    elif option == "4":

        for i, sub in enumerate(subjects, 1):
            print(f"{i}. {sub}")

        new_choice = input("\nChoose subject: ")

        if new_choice.isdigit() and 1 <= int(new_choice) <= len(subjects):
            subject = subjects[int(new_choice) - 1]
            records = data[subject]

    elif option == "5":

        print("Goodbye! 👋")
        break

    else:

        input("Invalid option. Press Enter...")
