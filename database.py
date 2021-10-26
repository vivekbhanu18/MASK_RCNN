import sqlite3 
import datetime
import csv
import os
# connecting to the database  
connection = sqlite3.connect("info.db") 
  
# cursor  
crsr = connection.cursor() 
print("connection setup successfully!!")
# SQL command to create a table in the database 
# SQL command to create a table in the database 
sql_command = """CREATE TABLE project_info(  
    id INTEGER PRIMARY KEY ,  
    plastic VARCHAR(20),    
    non_plastic VARCHAR(50),
    location VARCHAR(50),  
    date_created TEXT DEFAULT CURRENT_TIMESTAMP);"""    
count_p=4
count_n=9
    # execute the statement 
    #crsr.execute(sql_command)    
#crsr.execute("select sum(plastic),sum(non_plastic) from project_info where location='vashi';")


crsr.execute("""INSERT INTO project_info (plastic, non_plastic, date_created) VALUES (?, ?, datetime())""",(count_p,count_n)
)
print("inserted successfully!!")

os.remove('output.csv')
csvWriter = csv.writer(open("output.csv", "w"))
headers = ['plastic','non_plastic','location','date_created']
csvWriter.writerow(headers)
rows=crsr.execute("select plastic,non_plastic,location,date() from project_info;")
for row in rows:
	csvWriter.writerow(row)
connection.commit()
crsr.close()
connection.close()