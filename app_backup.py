import json
import os
from datetime import datetime

FILE = "attendance.json"


def load_data():
    if os.path.exists(FILE):
        with open(FILE, "r") as file:
            return json.load(file)
    return {}


def save_data(data):
    with open(FILE, "w") as file:
        json.dump(data, file, indent=4)


def percentage(present, absent):
    total = present + absent
    if total == 0:
        return 0
    return (present / total) * 100


def dashboard():
    print("\n" + "=" * 42)
    print("           STUDENT DASHBOARD")
    print("=" * 42)

    print("Name    :", name)
    print("College :", college)
    print("Branch  :", branch)

    if not data:
        print("\nNo attendance recorded yet.")
        return

    total_present = 0
    total_absent = 0

    print("\n" + "-" * 42)
    print("SUBJECT                ATTENDANCE")
    print("-" * 42)

    for subject, records in data.items():

        present = 0
        absent = 0

        for status in records.values():
            if status == "P":
                present += 1
            elif status == "A":
                absent += 1

        total = present + absent

        if total > 0:
            percent = percentage(present, absent)
            print(f"{subject:<22} {percent:.2f}%")
            total_present += present
            total_absent += absent
        else:
            print(f"{subject:<22} No classes")

    overall = percentage(total_present, total_absent)

    print("-" * 42)
    print(f"OVERALL ATTENDANCE:     {overall:.2f}%")

    if overall >= 75:
        print("STATUS:                 ✅ 75% or above")
    else:
        print("STATUS:                 ⚠️ Below 75%")


data = load_data()

print("=" * 42)
print("        STUDENT ATTENDANCE APP")
print("=" * 42)

name = input("Enter your name: ")
college = input("Enter your college: ")
branch = input("Enter your branch: ")

while True:

    print("\n" + "=" * 42)
    print("                  MENU")
    print("=" * 42)

    print("1. 📊 Student Dashboard")
    print("2. ✅ Mark Attendance")
    print("3. 📅 View Attendance")
    print("4. 📈 75% Attendance Calculator")
    print("5. ✏️ Edit Attendance")
    print("6. 🚪 Exit")
    print("7. 📅 Attendance Calendar")

    choice = input("\nChoose an option: ")

    # DASHBOARD
    if choice == "1":

        dashboard()

        input("\nPress Enter to continue...")

    # MARK ATTENDANCE
    elif choice == "2":

        subject = input("\nEnter subject: ")
        today = datetime.now().strftime("%d-%m-%Y")

        print("Today's date:", today)

        if subject not in data:
            data[subject] = {}

        if today in data[subject]:
            print("\n⚠️ Attendance already recorded today!")
            print("Current status:", data[subject][today])
            continue

        print("\nP = ✅ Present")
        print("A = ❌ Absent")
        print("H = 🏖️ Holiday")

        status = input("Enter status (P/A/H): ").upper()

        if status not in ["P", "A", "H"]:
            print("❌ Invalid choice!")
            continue

        data[subject][today] = status
        save_data(data)

        print("\nAttendance saved successfully! ✅")

    # VIEW ATTENDANCE
    elif choice == "3":

        if not data:
            print("\nNo attendance recorded yet.")
            continue

        print("\n" + "=" * 42)
        print("             ATTENDANCE HISTORY")
        print("=" * 42)

        for subject, records in data.items():

            print("\n📚", subject)
            print("-" * 30)

            present = 0
            absent = 0
            holiday = 0

            for date, status in sorted(records.items()):

                if status == "P":
                    print(date, "✅ Present")
                    present += 1

                elif status == "A":
                    print(date, "❌ Absent")
                    absent += 1

                elif status == "H":
                    print(date, "🏖️ Holiday")
                    holiday += 1

            total = present + absent

            print("\nPresent :", present)
            print("Absent  :", absent)
            print("Holiday :", holiday)

            if total > 0:
                print("Attendance:", f"{percentage(present, absent):.2f}%")
            else:
                print("Attendance: No classes")

        input("\nPress Enter to continue...")

    # 75% CALCULATOR
    elif choice == "4":

        if not data:
            print("\nNo attendance recorded yet.")
            continue

        print("\n" + "=" * 42)
        print("          75% ATTENDANCE CHECK")
        print("=" * 42)

        for subject, records in data.items():

            present = 0
            absent = 0

            for status in records.values():
                if status == "P":
                    present += 1
                elif status == "A":
                    absent += 1

            total = present + absent

            print("\n📚", subject)

            if total == 0:
                print("No classes recorded.")
                continue

            percent = percentage(present, absent)

            print("Classes    :", total)
            print("Present    :", present)
            print("Absent     :", absent)
            print("Attendance :", f"{percent:.2f}%")

            if percent >= 75:

                can_miss = int(present / 0.75 - total)

                if can_miss > 0:
                    print("✅ You can miss", can_miss, "more class(es).")
                else:
                    print("⚠️ Don't miss the next class!")

            else:

                needed = 0

                while percentage(
                    present + needed,
                    absent
                ) < 75:

                    needed += 1

                print("⚠️ Below 75%.")
                print("Need to attend", needed,
                      "more consecutive class(es).")

        input("\nPress Enter to continue...")

    # EDIT
    elif choice == "5":

        if not data:
            print("\nNo attendance recorded yet.")
            continue

        subject = input("\nEnter subject: ")

        if subject not in data:
            print("❌ Subject not found!")
            continue

        date = input("Enter date (DD-MM-YYYY): ")

        if date not in data[subject]:
            print("❌ No record found for this date!")
            continue

        print("\nCurrent status:", data[subject][date])

        print("\nP = Present")
        print("A = Absent")
        print("H = Holiday")

        new_status = input("Enter new status: ").upper()

        if new_status not in ["P", "A", "H"]:
            print("❌ Invalid choice!")
            continue

        data[subject][date] = new_status
        save_data(data)

        print("\nAttendance updated successfully! ✅")

    # CALENDAR
    elif choice == "7":
        print("\nOpening attendance calendar... 📅")
        exec(open("calendar_view.py").read())
        input("\nPress Enter to return to main menu...")

    # EXIT
    elif choice == "6":

        print("\nGoodbye", name, "! 👋")
        break

    else:

        print("\n❌ Invalid option!")
