import sqlite3
conn = sqlite3.connect("kbs.sqlite3")
# conn.commit
cursor = conn.cursor()

def student_info():
    cursor.execute("""CREATE TABLE IF NOT EXISTS st_info(
                   student_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   st_name VARCHAR(30) NOT NULL,
                   st_address VARCHAR(50) NOT NULL,
                   st_contact INTEGER NOT NULL)""")
    conn.commit()

student_info()

# def drop_table():
#     cursor.execute("""DROP TABLE IF EXISTS st_marks""")
# drop_table()
cursor.execute("""CREATE TABLE IF NOT EXISTS st_marks(
               st_id INTEGER NOT NULL,
               computer INTEGER NOT NULL,
               science INTEGER NOT NULL,
               math INTEGER NOT NULL,
               nepali INTEGER NOT NULL,
               english INTEGER NOT NULL,
               FOREIGN KEY(st_id) REFERENCES student_info(student_id))""")
conn.commit()

# function to insert data into students_info table
def insert_st_info(st_name,st_address,st_contact):
    cursor.execute("""INSERT INTO st_info(st_name,st_address,st_contact) VALUES (?,?,?)"""
                   ,(st_name,st_address,st_contact))
    conn.commit()
    print("Data inserted into student info table successfully!")

# function to insert data into st_marks table
def marks_data_insert(st_id,computer,science,math,nepali,english):
    # st_id = int(input("Student ID: "))
    # st_name = input("Name: ")
    cursor.execute("""INSERT INTO st_marks(st_id,computer,science,math,nepali,english) VALUES (?,?,?,?,?,?)"""
                   ,(st_id,computer,science,math,nepali,english))
    conn.commit()
    print("Data inserted succesfully into marks table")

# Function to update info into student info table!
def update_st_info(st_name,st_address,st_contact,student_id):
    cursor.execute("""UPDATE st_info SET st_name=?,st_address=?,st_contact=? WHERE student_id=?"""
                   ,(st_name,st_address,st_contact,student_id))
    conn.commit()
    print('Data successfully updated into student info table!')

# Function to update info into students marks table!
def update_st_marks(computer,science,math,nepali,english,st_id):
    cursor.execute("""UPDATE st_marks SET computer=?,science=?,math=?,nepali=?,english=? WHERE st_id=?"""
                   ,(computer,science,math,nepali,english,st_id))
    if cursor.rowcount == 0:
            print(f"No record found with st_id = {st_id}. Please verify the student ID.")
    else:
        conn.commit()
        print('Data successfully updated in the student marks table!')

# Function to clear student's info row
def clear_st_info(student_id):
    cursor.execute("DELETE FROM st_info WHERE student_id =?",(student_id,))
    conn.commit()
    print("Data Successfully deleted!")

# Function to clear student's marks row
def clear_st_mark(st_id):
    cursor.execute("DELETE FROM st_marks WHERE st_id =?",(st_id,))
    conn.commit()
    print("Data Successfully deleted!")

# Function to show the st_info table
def show_st_info():
    cursor.execute("SELECT* FROM st_info")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# Function to show the st_info table
def show_st_marks():
    cursor.execute("SELECT* FROM st_marks")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# Function to show the joint table!
# def merged_table():
#     cursor.execute("SELECT st_info.*,st_marks.* FROM st_info JOIN st_marks ON st_info.student_id=st_marks.st_id")
#     rows = cursor.fetchall()
#     for row in rows:
#         print(row)

def show_with_calculations():
    try:
        cursor.execute("""
            SELECT st_info.student_id, st_info.st_name, st_info.st_address, st_info.st_contact,
                   st_marks.computer, st_marks.science, st_marks.math, st_marks.nepali, st_marks.english,
                   (st_marks.computer + st_marks.science + st_marks.math + st_marks.nepali + st_marks.english) AS total_marks,
                   ROUND((st_marks.computer + st_marks.science + st_marks.math + st_marks.nepali + st_marks.english) / 5.0, 2) AS percentage
            FROM st_info
            INNER JOIN st_marks ON st_info.student_id = st_marks.st_id
        """)
        rows = cursor.fetchall()
        
        if rows:
            print("\nStudent Info with Calculations:")
            print("-" * 90)
            print("{:<5} {:<20} {:<20} {:<10} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5}".format(
                "ID", "Name", "Address", "Contact", "Comp", "Sci", "Math", "Nep", "Eng", "Total", "Percent"))
            print("-" * 100)
            
            for row in rows:
                print("{:<5} {:<20} {:<20} {:<10} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5.2f}".format(
                    row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]))
        else:
            print("No data found!")
    except Exception as e:
        print(f"Error fetching data: {e}")

# Search Result function
def search_result():
    print('1. Search by student_id\n2. Search by student_name')
    search_input = int(input("Enter option: "))
    if search_input == 1:
        student_id = int(input("Student's ID: "))
        cursor.execute("""SELECT st_info.student_id,st_info.st_name,st_info.st_address,st_info.st_contact,
        st_marks.computer,st_marks.science,st_marks.math,st_marks.nepali,st_marks.english,st_info.student_id,
        (st_marks.computer+st_marks.science+st_marks.math+st_marks.nepali+st_marks.english)AS Total_Marks,
        ROUND((st_marks.computer+st_marks.science+st_marks.math+st_marks.nepali+st_marks.english)/5.0,2)AS Percentage
        FROM st_info INNER JOIN st_marks ON st_info.student_id = st_marks.st_id WHERE student_id=?"""
        ,(student_id,)
        )
    elif search_input ==2:
        st_name = input("Student's Name: ")
        cursor.execute("""SELECT st_info.student_id,st_info.st_name,st_info.st_address,st_info.st_contact,
        st_marks.computer,st_marks.science,st_marks.math,st_marks.nepali,st_marks.english,st_info.student_id,
        (st_marks.computer+st_marks.science+st_marks.math+st_marks.nepali+st_marks.english)AS Total_Marks,
        ROUND((st_marks.computer+st_marks.science+st_marks.math+st_marks.nepali+st_marks.english)/5.0,2)AS Percentage
        FROM st_info INNER JOIN st_marks ON st_info.student_id = st_marks.st_id WHERE st_name LIKE?"""
        ,(st_name,)
        )
    else:
        print("Enter valid option")
        return

    rows = cursor.fetchall()
    if rows:
        print("\nStudent Search Results:")
        print("-" * 110)
        print("{:<5} {:<20} {:<20} {:<15} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5}".format(
            "ID", "Name", "Address", "Contact", "Comp", "Sci", "Math", "Nep", "Eng", "Total", "Percent"))
        print("-" * 110)
        for row in rows:
            print("{:<5} {:<20} {:<20} {:<15} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5.2f}".format(
                row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[10], row[11]))
    else:
        print("No record found matching the search criteria.")
    
# MAin function
def main():
    while True:
        try:
            print("""
    Select the option below:
    .........................
    1. Insert Student's Info    2. Insert into Marks Table         3. Update Student's Info
    4. Update Student's Marks   5. Delete Data from Student Info   6. Delete Data from Student Marks
    7. Show Student Info Table  8. Show Student's Marks Table      9. Show Entire Table
    10. Search Result           11. Exit
    .........................
    """)

            user_input = int(input("Enter the option: "))

            if user_input == 1:
                st_name = input("Name: ")
                st_address = input("Address: ")
                st_contact = int(input("Phone No: "))
                insert_st_info(st_name,st_address,st_contact)

            elif user_input == 2:
                st_id = int(input("St_id: "))
                computer = int(input("Computer: "))
                science = int(input("Science: "))
                math = int(input("Math: "))
                nepali = int(input("Nepali: "))
                english = int(input("English: "))
                marks_data_insert(st_id,computer,science,math,nepali,english)

            elif user_input == 3:
                student_id = int(input("St_id: "))
                st_name = input("Namer: ")
                st_address = input("Address: ")
                st_contact = int(input("Contact: "))
                update_st_info(st_name,st_address,st_contact,student_id)

            elif user_input == 4:
                computer = int(input("Computer: "))
                science = int(input("Science: "))
                math = int(input("Math: "))
                nepali = int(input("Nepali: "))
                english = int(input("English: "))
                st_id = int(input("St_id: "))
                update_st_marks(computer,science,math,nepali,english,st_id)

            elif user_input == 5:
                student_id = int(input("St_id: "))
                clear_st_info(student_id)
            elif user_input == 6:
                st_id = int(input("St_id: "))
                clear_st_mark(st_id)
            elif user_input == 7:
                show_st_info()
            elif user_input == 8:
                show_st_marks()
            elif user_input == 9:
                show_with_calculations()
            elif user_input==11:
                print("Good Bye!")
                exit()
            elif user_input == 10:
                search_result()
            else:
                print("Please enter valid option from above!")

        except ValueError: 
            print("Invalid option selected!")

main()
conn.close()

