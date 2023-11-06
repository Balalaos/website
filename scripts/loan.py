import os, re
import sqlite3
import ast
import datetime
import time

# This is database class. There is all operations connected with Database
class LoanDatabase():
    def __init__(self) -> None:
        cwd = os.path.dirname(os.path.realpath(__file__))
        cwd = cwd.replace("scripts", "database\\loan_app.db")
        self.conn = sqlite3.connect(cwd)
        self.cursor = self.conn.cursor()
        
    
    # This function searchs user in database
    # Input: user ID number
    # Return: user data
    def search(self, search_data):
        self.cursor.execute("SELECT * FROM users WHERE id = ?", (search_data,))
        rows = self.cursor.fetchall()
        return rows
    
    
    # This function deletes user in database
    # Input: user row number in database
    def delete_row(self, row_num):
        self.cursor.execute("DELETE FROM users WHERE row = ?", (row_num,))
        self.conn.commit()
        
        
    # This function adds user in database
    # Input: user ID data
    def add_data(self, row):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            row INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            id INTEGER,
            black_listed BIT DEFAULT 0,
            loan_number INTEGER,
            money TEXT,
            start_date TEXT,
            end_date TEXT,
            current_time DATETIME
        )
        """)
        
        self.cursor.execute("""
        INSERT INTO users (username, id, black_listed, loan_number, money, start_date, end_date, current_time)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
        
        self.conn.commit()
        self.conn_close()
        
        
    # This function closes connection with database
    def conn_close(self):
        self.conn.close()



# This class taking data from main page fields and controls if data correct and finds user in database.
# It shows borrower data if user was found
class MainPage():  
    def __init__(self):
        pass
    
    
    class Error(Exception):
        def __init__(self, message="Unexpected error"):
            super().__init__(message)
    
    
    # This function searchs user in database
    # Input: username from main page field
    # Return: string, if there is not this borrower
    #         or user data
    def search(self, id):

        database = LoanDatabase()
        rows = database.search(id)
        database.conn_close()
        if not rows:
            raise self.Error("We did not find anything")
        else:
            #reformat data from database format to show data format
            row = self.rewrite(rows[0])
            return row
     
            
    # This function preparing data from database to be shown
    # Input: database data
    # Return: data is ready for showing
    def rewrite(self, row):
        message = []
        for i in range(5):
            message.append(row[i])
        
        money = re.findall(r'\b\w+\b|\d+', row[5])
        start_date = ast.literal_eval(row[6])
        end_date =  ast.literal_eval(row[7])
        amount = 0 
        total_money = 0
        
        for i in range(message[4]):
            money[i] = int(money[i])
            start = datetime.datetime.strptime(start_date[i], "%Y-%m-%d").date()
            end = datetime.datetime.strptime(end_date[i], "%Y-%m-%d").date()
            months = (end.year - start.year) * 12 + (end.month - start.month)
            total_money += money[i]
            amount += money[i] * (1 + 0.05) ** months
            
        amount = round(amount, 2)
        message.append(money)
        message.append(start_date)
        message.append(end_date)

        message.append(total_money)
        message.append(amount)
        data = self.change_for_session(message)
        return data


    # This function reformat data from database format to show data format
    # Input: database data
    # Return: data is ready for showing
    def change_for_session(self, row):
        data = {}
        data['username'] = row[1]
        data['id'] = row[2]
        data['blacklisted'] = row[3]
        data['array_size'] = row[4]
        data['money']  = row[5]
        data['date_start'] = row[6]
        data['date_end'] = row[7]
        data['total_money']  = row[8]
        data['amount'] = row[9]
        return data



# This class taking data from register page fields and controlls if data correct
# and if a borrower is blacklisted or there was loan request in 24 hours.
# If everything is correct it saves borrower data to database
class RegistrationForm():
    def __init__(self):
        pass
    
    
    class Error(Exception):
        def __init__(self, message="Unexpected error"):
            super().__init__(message)
    
    
    # This function reads data, checks it and saves it to database
    # Input: data from register page fields
    # Return: error message 
    #         or array with borrower information
    def submit_registration(self, data):
        username = data['username']
        id = int(data['id'])
        money = data['money']
        date = data['date']
    
        # Check if date is minimum 90 days after todays date
        try:
            time_tuple = time.strptime(date, '%Y-%m-%d')
            date = datetime.date(*time_tuple[:3])
        except ValueError:
            raise self.Error("Date is incorrect")
        
        today = datetime.date.today()
        difference = date - today
        if difference.days < 90:
            raise self.Error("Date should be 90 days after this date")
            
        # Open data base
        database = LoanDatabase()
        rows = database.search(id)
        
        # Check if user is blacklist
        try:
            borrower_data = self.check_black_listed(rows)
        except:
            database.conn_close()
            raise self.Error("The borrower is blacklisted")
        
        # If user is in data base a new loan will be added to the old ones
        if borrower_data:
            # Add new loan if borrower exists already
            if username == borrower_data[1] and id == borrower_data[2]:
                # Check if there was loan in the previous 24 hours
                if not self.check_time(borrower_data):
                    database.conn_close()
                    raise self.Error("You asked for too many loans in 24 hours")
                # If everything is correct takes all user data to be owerwrite in future
                loan_number = borrower_data[4] + 1
                money_array= re.findall(r'\b\w+\b|\d+', borrower_data[5])
                today_array = ast.literal_eval(borrower_data[6])
                date_array =  ast.literal_eval(borrower_data[7])
                money_array.append(money)
                today_array.append(today.strftime("%Y-%m-%d"))
                date_array.append(date.strftime("%Y-%m-%d"))
                # Delete all data
                database.delete_row(borrower_data[0])
            # If there is another user using this ID sends error message
            else:
                string = "There is another borrower using " + str(borrower_data[2]) + " ID."
                raise self.Error(string)
            
        # If there is no anyone whos use this ID, new user will be added
        else:
            current_time = datetime.datetime.now().replace(microsecond=0)
            loan_number = 1
            money_array = []
            today_array = []
            date_array = []
            money_array.append(money)
            today_array.append(today.strftime("%Y-%m-%d"))
            date_array.append(date.strftime("%Y-%m-%d"))
            
        black_listed = False
        row = (0, username, id, black_listed, loan_number, str(money_array), str(today_array), str(date_array), current_time)
        database.add_data(row)   
        
        # Return user data
        return row
            
    
    # This function checks if user blacklisted
    # Input: username
    # Return: error if user blacklisted
    #         or False bool, if there is not user with this id
    #         or array, if there is user with this id
    def check_black_listed(self, rows):
        if len(rows) == 0:
            return False
        for row in rows:
            if row[3] == 1:
                raise Exception()
        
        return rows[0]
       

    # This function checks if there was loan in the previous 24 hours
    # Input: username
    # Return: True or False bool depending if time is correct
    def check_time(self, message):
        current_time = datetime.datetime.now().replace(microsecond=0)
        twenty_four_hours_ago = current_time - datetime.timedelta(hours=24)
                
        format_string = '%Y-%m-%d %H:%M:%S'
        datetime_object = datetime.datetime.strptime(message[8], format_string)
        if twenty_four_hours_ago < datetime_object:
            return False
        return True