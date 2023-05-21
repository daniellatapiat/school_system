import os
import sqlite3

if os.path.isfile("mydatabase.db"):
    os.remove('mydatabase.db')

conn = sqlite3.connect('mydatabase.db')

cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS users
    (id INTEGER PRIMARY KEY, type TEXT, name TEXT, username TEXT, pass TEXT, status TEXT, group_id TEXT, balance FLOAT)''')

cur.execute("INSERT INTO users (type,name,username,pass,status,group_id,balance) VALUES ('student', 'Alicia', 'student', 'Sstudent', 'ACTIVE', 'A', '850.50')")
cur.execute("INSERT INTO users (type,name,username,pass) VALUES ('teacher', 'Juan', 'teacher', 'Tteacher')")
cur.execute("INSERT INTO users (type,name,username,pass) VALUES ('teacher', 'Charlie', 'charlie', 'Ccharlie')")
cur.execute("INSERT INTO users (type,name,username,pass,status,group_id) VALUES ('student', 'David', 'david', 'Ddavid', 'ACTIVE', 'B')")
cur.execute("INSERT INTO users (type,name,username,pass) VALUES ('coordinator', 'Emma', 'coordinator', 'Ccoordinator')")

cur.execute('''CREATE TABLE IF NOT EXISTS classes 
    (class_name TEXT, group_id TEXT, teacher_name TEXT)''')

cur.execute("INSERT INTO classes (class_name,group_id,teacher_name) VALUES ('Math', 'A', 'Juan')")
cur.execute("INSERT INTO classes (class_name,group_id,teacher_name) VALUES ('Math', 'B', 'Charlie')")
cur.execute("INSERT INTO classes (class_name,group_id,teacher_name) VALUES ('Spanish', 'A', 'Charlie')")
cur.execute("INSERT INTO classes (class_name,group_id,teacher_name) VALUES ('Spanish', 'B', 'Juan')")

cur.execute('''CREATE TABLE IF NOT EXISTS student_classes
    (user_name TEXT, class_name TEXT, group_id TEXT, grade FLOAT)''')

cur.execute("INSERT INTO student_classes (user_name,class_name,group_id,grade) VALUES ('Alicia', 'Math', 'A', '9.5')")
cur.execute("INSERT INTO student_classes (user_name,class_name,group_id) VALUES ('David', 'Math', 'B')")
cur.execute("INSERT INTO student_classes (user_name,class_name,group_id,grade) VALUES ('Alicia', 'Spanish', 'B', '8')")
cur.execute("INSERT INTO student_classes (user_name,class_name,group_id,grade) VALUES ('David', 'Spanish', 'A', '10')")

cur.execute('''CREATE TABLE IF NOT EXISTS missed_attendance
    (user_name TEXT, class_name TEXT, group_id TEXT, date DATE)''')

cur.execute("INSERT INTO missed_attendance (user_name,class_name,group_id,date) VALUES ('Alicia', 'Math', 'A', '2023-05-18')")

conn.commit()
conn.close()
