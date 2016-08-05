"""PROBLEM DESCRIPTION:
COUNTING ORGANIZATIONS

This application will read the mailbox data (mbox.txt) count up the number email
messages per organization (i.e. domain name of the email address) using a database
with the following schema to maintain the counts:

CREATE TABLE Counts (org TEXT, count INTEGER)

When you have run the program on mbox.txt upload the resulting database file 
above for grading. If you run the program multiple times in testing or with dfferent files, make
sure to empty out the data before each run.

You can use this code as a starting point for your application: 
http://www.pythonlearn.com/code/emaildb.py.

The data file for this application is the same as in previous assignments:
http://www.pythonlearn.com/code/mbox.txt.

Because the sample code is using an UPDATE statement and committing the results
to the database as each record is read in the loop, it might take as long as a 
Few minutes to process all the data. The commit insists on completely writing 
all the data to disk every time it is called.

The program can be speeded up greatly by moving the commit operation outside of
the loop. In any database program, there is a balance between the number of 
operations you execute between commits and the importance of not losing the 
results of operations that have not yet been committed. 
"""

"""PERSONAL COMMENTS:
As we can see, this exercise is identical as the email-counting database 
example that we've just seen, with the only difference that we have to count the
organizations and not the individual email adresses. However, we can use the 
code provided as example and only add a few modifications.

What we're going to do is, after getting the email, separate it using the .split()
method and taking into account that in an email address the separator is the "@"
symbol.

Besides, instead of reading directly a previously-downloaded mbox.txt file, we'll
obtain its information directly from internet, using urllib and the knowledge we 
got from the previous course. 
"""

import sqlite3
import urllib

#Connecting to the file in which we want to store our db
conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

#Deleting any possible table that may affect this assignment
cur.execute('''
DROP TABLE IF EXISTS Counts''')

#Creating the table we're going to use
cur.execute('''
CREATE TABLE Counts (org TEXT, count INTEGER)''')

#Indicating the file (URL in this case) from where we'll read the data
fname = "http://www.pythonlearn.com/code/mbox.txt"
fh = urllib.urlopen(fname)

#Reading each line of the file
for line in fh:

    #Finding an email address and splitting it into name and organization
    if not line.startswith('From: ') : continue
    pieces = line.split()
    email = pieces[1]
    (emailname, organization) = email.split("@")
    print email

    #Updating the table with the correspondent information
    cur.execute('SELECT count FROM Counts WHERE org = ? ', (organization, ))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO Counts (org, count) 
                VALUES ( ?, 1 )''', ( organization, ) )
    else : 
        cur.execute('UPDATE Counts SET count=count+1 WHERE org = ?', 
            (organization, ))

# We commit the changes after they've finished because this speeds up the 
# execution and, since our operations are not critical, a loss wouldn't suppose
# any problem
conn.commit()

# Getting the top 10 results and showing them
sqlstr = 'SELECT org, count FROM Counts ORDER BY count DESC LIMIT 10'
print
print "Counts:"
for row in cur.execute(sqlstr) :
    print str(row[0]), row[1]

#Closing the DB
cur.close()

