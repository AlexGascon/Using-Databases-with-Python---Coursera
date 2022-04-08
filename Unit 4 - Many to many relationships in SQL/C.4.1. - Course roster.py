"""
INSTRUCTIONS

This application will read roster data in JSON format, parse the file, and 
then produce an SQLite database that contains a User, Course, and Member 
table and populate the tables from the data file.

You can base your solution on this code: 
http://www.pythonlearn.com/code/roster.py - this code is incomplete as you
need to modify the program to store the role column in the Member table to
complete the assignment.

Each student gets their own file for the assignment. Download this file 
(https://pr4e.dr-chuck.com/tsugi/mod/sql-intro/roster_data.php?PHPSESSID=ac66d3b8dbd59e2dcfee8c24b15c25b9)
and save it as roster_data.json. Move the downloaded file into the same 
folder as your roster.py program.

Once you have made the necessary changes to the program and it has been run 
successfully reading the above JSON data, run the following SQL command:

SELECT hex(User.name || Course.title || Member.role ) AS X FROM 
    User JOIN Member JOIN Course 
    ON User.id = Member.user_id AND Member.course_id = Course.id
    ORDER BY X

Find the first row in the resulting record set and enter the long string that
looks like 53656C696E613333. 
"""

import json
import sqlite3
 
conn = sqlite3.connect('rosterdb.sqlite') 
cur = conn.cursor()
 
# Do some setup
cur.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;
 
 
CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);
 
CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);
 
CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')
 
fname = input('Enter file name: ')
if len(fname) < 1:
    fname = 'roster_data.json'
 
# [
#   [ "Charley", "si110", 1 ],
#   [ "Mea", "si110", 0 ],
 
str_data = open(fname).read()
json_data = json.loads(str_data)
 
for entry in json_data:
 
    name = entry[0]
    title = entry[1]
    role= entry[2]
 
    print((name, title, role))
 
    cur.execute('''INSERT OR IGNORE INTO User (name)
        VALUES ( ? )''', ( name, ) )
    cur.execute('SELECT id FROM User WHERE name = ? ', (name, ))
    user_id = cur.fetchone()[0]
 
    cur.execute('''INSERT OR IGNORE INTO Course (title)
        VALUES ( ? )''', ( title, ) )
    cur.execute('SELECT id FROM Course WHERE title = ? ', (title, ))
    course_id = cur.fetchone()[0]
 
    cur.execute('''INSERT OR IGNORE INTO Member (role)
        VALUES ( ? )''', ( role, ) )
     
     
 
    cur.execute('''INSERT OR REPLACE INTO Member
        (user_id, course_id) VALUES ( ?, ?)''',
        ( user_id, course_id ) )
 
    conn.commit()

#PART 4: Testing and obtaining the results
test_statement = """
SELECT hex(User.name || Course.title || Member.role ) AS X FROM 
    User JOIN Member JOIN Course 
    ON User.id = Member.user_id AND Member.course_id = Course.id
    ORDER BY X
"""
cur.execute(test_statement)
result = cur.fetchone()
print("RESULT: " + str(result))

#Closing the connection
cur.close()
conn.close()

