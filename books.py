from tabulate import tabulate
import sqlite3
db = sqlite3.connect('books_db')
cursor = db.cursor()

# checking if table books exists in the books_db
cursor.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='books' ''')
# if .fetchone()[0] is one that means that table already exists and there is no need to create it
if cursor.fetchone()[0] != 1:
    cursor.execute('''CREATE TABLE books(id INTEGER PRIMARY KEY, title TEXT, author TEXT, qty INTEGER)''')
    # populating books table
    cursor.execute('''INSERT INTO books (id, title, author, qty)
                    VALUES(?, ?, ?, ?)''', (3001, 'A Tale of Two Cities', 'Charles Dickens', 30))
    cursor.execute('''INSERT INTO books (id, title, author, qty)
                    VALUES(?, ?, ?, ?)''', (3002, 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 40))
    cursor.execute('''INSERT INTO books (id, title, author, qty)
                    VALUES(?, ?, ?, ?)''', (3003, 'The Lion, the Witch and the Wardrobe', 'C. S. Lewis', 25))
    cursor.execute('''INSERT INTO books (id, title, author, qty)
                    VALUES(?, ?, ?, ?)''', (3004, 'The Lord of the Rings', 'J.R.R Tolkien', 37))
    cursor.execute('''INSERT INTO books (id, title, author, qty)
                    VALUES(?, ?, ?, ?)''', (3005, 'Alice in Wonderland', 'Lewis Carroll', 12))
    db.commit()
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
# defining enter_book function
def enter_book():
    # sorting rows by id in descending order in order to find latest id number
    cursor.execute("SELECT * FROM books ORDER BY id DESC LIMIT 1")
    # retrieving latest id number and adding one to it 
    book_id = cursor.fetchone()[0] + 1 
    book_title = input("Please enter title of the book: ")
    book_author = input("Please enter author of the book: ")
    while True:
        try:
            book_qty = int(input("Please enter quantity: "))
            break
        except ValueError:
            print("Not a number. Please enter a number.")  
    # adding book to the table
    cursor.execute('''INSERT INTO books (id, title, author, qty)
                    VALUES(?, ?, ?, ?)''', (book_id, book_title, book_author, book_qty))
    db.commit()
#----------------------------------------------------------------------------------------
# function checking if given id is not in the table in database
# if it is not the function returns True
def not_in(num):
    cursor.execute("SELECT * FROM books")
    # storing the whole books table in c variable
    c = cursor.fetchall()
    # iterating trough all of the rows and checking first value in the row 
    # which is id and comparing it to id entered by the user
    for row in c:
        if num != row[0] :
            b = 0
        else:
            b = 1
            break
    if b == 0:
        return True
#-----------------------------------------------------------------------------------------
# defining update_book function
def update_book():
    while True:
        try:
            # getting input from the user
            id_num = int(input("Please type in id of the book you would like to update: "))
            # checking if given id is in the database
            if not_in(id_num) == True:
                print("There is no book with that id in the database. Please try again.")
                continue
            else:
                break
        except ValueError:
            print("Your input was incorrect. Please try again.")           
    while True:    
        # giving user choice what to update
        update = input('''
            Please choose what information you would like to update:
            1. Title
            2. Author
            3. Quantity
            4. Go back
        ''')
        if update == '1':
            title_update = input("Please enter new title: ")
            cursor.execute('''UPDATE books SET title = ? WHERE id = ? ''', (title_update, id_num))
            db.commit()
        elif update == '2':
            author_update = input("Please enter authors name: ")
            cursor.execute('''UPDATE books SET author = ? WHERE id = ? ''', (author_update, id_num))
            db.commit()
        elif update == '3':
            while True:
                try:
                    qty_update = int(input("Please enter quantity: "))
                    break
                except ValueError:
                    print("Please enter a number.")
            cursor.execute('''UPDATE books SET qty = ? WHERE id = ? ''', (qty_update, id_num))
            db.commit()
        elif update == '4':
            break
        else:
            print("You choice doesn't match any of the options. Please try again")
#---------------------------------------------------------------------------------------
# defining delete function
def delete():
    while True:
        try:        
            # asking user to input id of the book they want to be deleted
            id_num = int(input("Please type in id of the book you would like to delete: "))
            # checking if given id is in the database
            if not_in(id_num) == True:
                print("There is no book with that id in the database. Please try again.")
                continue
            else:
                break
        except ValueError:
            print("Your input was incorrect. Please try again.")
    # deleting the row with given id 
    cursor.execute('''DELETE FROM books WHERE id = ?''', (id_num,))
    db.commit()
#--------------------------------------------------------------------------------------
# defining searching function
def search():
    while True:
        # asking user to choose an option 
        choice = input('''
            PLease choose one of the options:
            1. Search by book ID
            2. Go back
        ''')
        if choice == '1':
            # if the option to search has been selected 
            while True:
                try:        
                    # asking user to input id of the book they want to look for
                    id_num = int(input("Please type in id of the book you are looking for: "))
                    # checking if given id is in the database
                    if not_in(id_num) == True:
                        y_or_n =  input("There is no book with that id in the database. Please pres Y to try again or N to go back. ").lower()
                        # if the book is not in database user has an option to go back to main menu
                        if y_or_n == 'y':
                            continue
                        elif y_or_n == 'n':
                            break
                        else:
                            print("Please enter Y or N.")
                            continue
                except ValueError:
                    print("Your input was incorrect. Please try again.")
                cursor.execute('''SELECT id, title, author, qty FROM books WHERE id = ?''', (id_num,))
                book = cursor.fetchone()
                # printing out search result in table form
                tab = tabulate([[book[0], book[1], book[2], book[3]]],headers = ["Id","Title","Author","Quantity"],tablefmt="simple_grid" )
                print(tab)
                break
        if choice == '2':
            break
#--------------------------------------------------------------------------------------------
# function displaying all of the books in the inventory
def dis_all():
    cursor.execute('''SELECT * FROM books''')
    rows = cursor.fetchall()
    # printing out the result in table form
    tab = tabulate(rows, headers = ["Id","Title","Author","Quantity"],tablefmt="simple_grid")
    print(tab)
#--------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------
# main menu of the program 
while True:
    # asking user to choose one of the options
    choice = input('''
    ------------------------------------------
            WELCOME TO BOOK INVENTORY
    PLEASE CHOOSE FROM THE FOLLOWING OPTIONS

    1. Enter book
    2. Update book
    3. Delete book
    4. Search book
    5. Display all
    0. exit
    ------------------------------------------
    ''')

    if choice == '1':
        enter_book()
    elif choice == '2':
        update_book()
    elif choice == '3':
        delete()
    elif choice == '4':
        search()
    elif choice == '5':
        dis_all()
    elif choice == '0':
        db.close()
        exit()
    else:
        print("You have entered incorrect option. Please try again.")