import sqlite3

connection=sqlite3.connect("student.db")

#create a cursur object to insert record, create table, retrieve data
cursor=connection.cursor()

#create table
table_info="""
CREATE TABLE Student(name VARCHAR(100), class VARCHAR(100),
section VARCHAR(100), marks INT);   
"""
cursor.execute("DROP TABLE IF EXISTS Student")
cursor.execute(table_info)

#insert some records

cursor.execute("INSERT INTO Student VALUES ('Aditya', 'AI', 'A', 90)")
cursor.execute("INSERT INTO Student VALUES ('Prithvi', 'AI', 'A',92)")
cursor.execute("INSERT INTO Student VALUES ('Aneesh', 'Data Science', 'A', 84)")
cursor.execute("INSERT INTO Student VALUES ('Siddharth', 'CSE', 'C', 56)")
cursor.execute("INSERT INTO Student VALUES ('Harsha', 'MG', 'F', 0)")

#Display all the records

print("The inserted records are: ")

data = cursor.execute("SELECT * FROM Student")

for row in data:
    print(row)

connection.commit()
connection.close()

