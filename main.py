import sqlite3

conn = sqlite3.connect('mydatabase.db')
cur = conn.cursor()

notices = "No new notices."


def login():
    while 1 == 1:
        val_user = input("Username: ")
        user_pass = input("Password: ")

        cur.execute("SELECT * FROM users WHERE username = ?", (val_user,))
        rows = cur.fetchall()

        if len(rows) != 1:
            print("bad username")
            retry = input("Would you like to try again? Y/N\n")
            if retry.lower() == 'Y':
                continue
            else:
                exit()

        if user_pass != rows[0][4]:
            print("bad pass")
            continue

        return rows[0][1], rows[0][2]


user_type, user_name = login()


def prompt():
    response = input("Do you want to go back to the main menu? Y/N\n")

    if response.lower() != "y":
        exit()


def student_menu():
    while 1 == 1:
        print("Main menu")
        print("1. Grades")
        print("2. Unpaid balance")
        print("3. Enrolled classes")
        print("4. Certificate requests")
        print("5. Exit")
        choice = input("Please select an option.\n")

        if choice == "1":
            cur.execute("SELECT class_name, grade FROM student_classes WHERE user_name = ?", (user_name,))
            rows = cur.fetchall()

            for student_class in rows:
                class_name, grade = student_class
                print("Class:", class_name)
                print("Grade:", grade)

            prompt()

        elif choice == "2":
            cur.execute("SELECT balance FROM users WHERE name = ?", (user_name,))
            row = cur.fetchone()

            if row is not None:
                balance = row[0]
                print("Pending balance:", balance)
            else:
                print("No pending balance.")

            prompt()

        elif choice == "3":
            cur.execute("SELECT class_name FROM student_classes WHERE user_name = ?", (user_name,))
            rows = cur.fetchall()

            print("Enrolled classes:")
            for row in rows:
                class_name = row[0]
                print(class_name)

            prompt()

        elif choice == "4":
            req = input("Would you like to request a certificate? Y/N\n")

            if req == "Y":
                print("Your certificate has been requested.")

            prompt()

        elif choice == "5":
            exit()


def teacher_menu():
    while 1 == 1:
        print("Main menu")
        print("1. Grades")
        print("2. Missed attendance")
        print("3. Notices")
        print("4. Exit")
        choice = input("Please select an option.\n")

        if choice == "1":
            update_grades()
            prompt()

        elif choice == "2":
            print("Please provide the following information:")
            class_name = input("Class name:\n")
            group_id = input("Group id:\n")
            student_name = input("Student name:\n")
            date = input("Date: YYYY/MM/DD\n")

            cur.execute("INSERT INTO missed_attendance (user_name, class_name, group_id, date) VALUES (?, ?, ?, ?)", (student_name, class_name, group_id, date,))
            conn.commit()

            print("Missed attendance recorded successfully.")

            prompt()

        elif choice == "3":
            print(notices)
            prompt()

        elif choice == "4":
            exit()


def coordinator_menu():
    while 1 == 1:
        print("Main menu")
        print("1. Create new group")
        print("2. Assign classes")
        print("3. Register student")
        print("4. Change grades")
        print("5. Student status")
        print("6. Exit")
        choice = input("Please select an option.\n")

        if choice == "1":
            name = input("Student name:\n")
            group_id = input("Group id:\n")

            cur.execute("UPDATE users SET group_id = ? WHERE name = ?", (group_id, name,))
            conn.commit()

            if cur.rowcount > 0:
                print("Group assignment was successful.")
            else:
                print("No matching records found.")

            prompt()

        elif choice == "2":
            print("Please provide the following information:")
            class_name = input("Class name:\n")
            group_id = input("Group id:\n")
            teacher_name = input("Teacher name:\n")

            cur.execute("UPDATE classes SET teacher_name = ? WHERE class_name = ? AND group_id = ?", (teacher_name, class_name, group_id,))
            conn.commit()

            if cur.rowcount > 0:
                print("Class assignment was successful.")
            else:
                print("No matching records found.")

            prompt()

        elif choice == "3":
            print("Please provide the following information:")
            new_user_type = input("User type:\n")
            new_name = input("Name:\n")
            new_username = input("Username:\n")
            new_password = input("Password:\n")
            user_status = input("Status:\n")
            group_id = input("Group ID:\n")
            user_balance = input("Pending balance:\n")

            if new_user_type.lower() != "student":
                print("User type must be 'student'.")
            else:
                cur.execute("INSERT INTO users (type, name, username, pass, status, group_id, balance) VALUES (?, ?, ?, ?, ?, ?, ?)", (new_user_type, new_name, new_username, new_password, user_status, group_id, user_balance,))
                conn.commit()
                print("New student has been added successfully.")
                prompt()

        elif choice == "4":
            update_grades()
            prompt()

        elif choice == "5":
            name = input("Student name:\n")

            cur.execute("SELECT status FROM users WHERE name = ?", (name,))
            row = cur.fetchone()

            if row is not None:
                status = row[0]
                print("Status:", status)

            prompt()

        elif choice == "6":
            exit()


def update_grades():
    print("Please provide the following information:")
    class_name = input("Class name:\n")
    group_id = input("Group id:\n")
    student_name = input("Student name:\n")
    new_grade = input("Grade:\n")

    cur.execute("UPDATE student_classes SET grade = ? WHERE user_name = ? AND class_name = ? AND group_id = ?",
                (new_grade, student_name, class_name, group_id,))
    conn.commit()

    if cur.rowcount > 0:
        print("Grade updated successfully.")
    else:
        print("No matching records found.")


print("Welcome!")

if user_type == 'student':
    student_menu()

elif user_type == 'teacher':
    teacher_menu()

elif user_type == 'coordinator':
    coordinator_menu()

conn.close()
