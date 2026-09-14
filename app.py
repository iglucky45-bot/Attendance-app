import json
import os
from datetime import datetime

ATTENDANCE_FILE = "attendance.json"
PROFILE_FILE = "profile.json"


def load_json(filename, default):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return default


def save_json(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def attendance_percentage(present, absent):
    total = present + absent
    if total == 0:
        return 0
    return (present / total) * 100


attendance = load_json(ATTENDANCE_FILE, {})
profile = load_json(PROFILE_FILE, None)


# FIRST TIME SETUP
if profile is None:

    print("==============================")
    print("     STUDENT ATTENDANCE")
    print("==============================")

    name = input("Enter your name: ")
    college = input("Enter your college: ")
    branch = input("Enter your branch: ")

    profile = {
        "name": name,
        "college": college,
        "branch": branch
    }

    save_json(PROFILE_FILE, profile)

    print("\nProfile saved successfully! ✅")

else:

    name = profile["name"]
    college = profile["college"]
    branch = profile["branch"]

    print("==============================")
    print("     WELCOME BACK! 👋")
    print("==============================")
    print("Name   :", name)
    print("College:", college)
    print("Branch :", branch)


while True:

    print("\n==============================")
    print("            MENU")
    print("==============================")
    print("1. 📊 Student Dashboard")
    print("2. ✅ Mark Attendance")
    print("3. 📋 View Attendance")
    print("4. 📈 75% Attendance Calculator")
    print("5. ✏️ Edit Attendance")
    print("6. 📅 Attendance Calendar")
    print("7. 👤 Profile")
    print("8. 🚪 Exit")

    choice = input("\nChoose an option: ")


    # DASHBOARD
    if choice == "1":

        print("\n==============================")
        print("       STUDENT DASHBOARD")
        print("==============================")

        print("Name   :", name)
        print("College:", college)
        print("Branch :", branch)

        if not attendance:
            print("\nNo attendance recorded yet.")
        else:

            total_present = 0
            total_absent = 0

            print("\nSubject-wise Attendance")
            print("-" * 35)

            for subject, records in attendance.items():

                present = 0
                absent = 0

                for status in records.values():

                    if status == "P":
                        present += 1

                    elif status == "A":
                        absent += 1

                total = present + absent

                if total > 0:

                    percent = attendance_percentage(
                        present, absent
                    )

                    print(
                        f"{subject:<20} {percent:.2f}%"
                    )

                    total_present += present
                    total_absent += absent

            overall = attendance_percentage(
                total_present,
                total_absent
            )

            print("-" * 35)
            print(f"Overall Attendance: {overall:.2f}%")

        input("\nPress Enter to continue...")


    # MARK ATTENDANCE
    elif choice == "2":

        subject = input("\nEnter subject: ")

        today = datetime.now().strftime("%d-%m-%Y")

        print("Today's date:", today)

        if subject not in attendance:
            attendance[subject] = {}

        if today in attendance[subject]:

            print("\n⚠️ Attendance already recorded today!")
            print(
                "Current status:",
                attendance[subject][today]
            )

            continue

        print("\nP = ✅ Present")
        print("A = ❌ Absent")
        print("H = 🏖️ Holiday")

        status = input(
            "Enter status (P/A/H): "
        ).upper()

        if status not in ["P", "A", "H"]:

            print("❌ Invalid choice!")
            continue

        attendance[subject][today] = status

        save_json(
            ATTENDANCE_FILE,
            attendance
        )

        print("\nAttendance saved! ✅")


    # VIEW ATTENDANCE
    elif choice == "3":

        if not attendance:

            print("\nNo attendance recorded yet.")
            continue

        print("\n==============================")
        print("       ATTENDANCE HISTORY")
        print("==============================")

        for subject, records in attendance.items():

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

            print("\nPresent:", present)
            print("Absent :", absent)
            print("Holiday:", holiday)

            if total > 0:

                percent = attendance_percentage(
                    present,
                    absent
                )

                print(
                    "Attendance:",
                    f"{percent:.2f}%"
                )


        input("\nPress Enter to continue...")


    # 75% CALCULATOR
    elif choice == "4":

        if not attendance:

            print("\nNo attendance recorded yet.")
            continue

        print("\n==============================")
        print("       75% CHECK")
        print("==============================")

        for subject, records in attendance.items():

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

            percent = attendance_percentage(
                present,
                absent
            )

            print(
                "Attendance:",
                f"{percent:.2f}%"
            )

            if percent >= 75:

                can_miss = int(
                    present / 0.75 - total
                )

                print("✅ Above 75%")

                if can_miss > 0:

                    print(
                        "You can miss:",
                        can_miss,
                        "class(es)"
                    )

            else:

                needed = 0

                while attendance_percentage(
                    present + needed,
                    absent
                ) < 75:

                    needed += 1

                print("⚠️ Below 75%")

                print(
                    "Need to attend:",
                    needed,
                    "more class(es)"
                )

        input("\nPress Enter to continue...")


    # EDIT ATTENDANCE
    elif choice == "5":

        subject = input("\nEnter subject: ")

        if subject not in attendance:

            print("❌ Subject not found!")
            continue

        date = input(
            "Enter date (DD-MM-YYYY): "
        )

        if date not in attendance[subject]:

            print("❌ Date not found!")
            continue

        print(
            "Current status:",
            attendance[subject][date]
        )

        print("\nP = Present")
        print("A = Absent")
        print("H = Holiday")

        status = input(
            "Enter new status: "
        ).upper()

        if status not in ["P", "A", "H"]:

            print("❌ Invalid choice!")
            continue

        attendance[subject][date] = status

        save_json(
            ATTENDANCE_FILE,
            attendance
        )

        print(
            "\nAttendance updated! ✅"
        )


    # CALENDAR
    elif choice == "6":

        print(
            "\nOpening calendar... 📅"
        )

        if os.path.exists("calendar_view.py"):

            exec(
                open(
                    "calendar_view.py"
                ).read()
            )

        else:

            print(
                "Calendar file not found."
            )

        input(
            "\nPress Enter to return..."
        )


    # PROFILE
    elif choice == "7":

        print("\n==============================")
        print("           PROFILE")
        print("==============================")

        print("Name   :", name)
        print("College:", college)
        print("Branch :", branch)

        change = input(
            "\nChange profile? (Y/N): "
        ).upper()

        if change == "Y":

            name = input(
                "Enter new name: "
            )

            college = input(
                "Enter new college: "
            )

            branch = input(
                "Enter new branch: "
            )

            profile = {
                "name": name,
                "college": college,
                "branch": branch
            }

            save_json(
                PROFILE_FILE,
                profile
            )

            print(
                "\nProfile updated! ✅"
            )


    # EXIT
    elif choice == "8":

        print(
            "\nGoodbye",
            name,
            "! 👋"
        )

        break


    else:

        print(
            "\n❌ Invalid option!"
        )
