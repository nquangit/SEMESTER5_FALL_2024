import sqlite3

# Create a database in RAM
db = sqlite3.connect(':memory:')

# Get a cursor object
cursor = db.cursor()
cursor.execute('''
    CREATE TABLE Ages ( 
    name VARCHAR(128), 
    age INTEGER
)
''')


cursor.execute('''DELETE FROM Ages;''')

'''
INSERT INTO Ages (name, age) VALUES ('Liberty', 31);
INSERT INTO Ages (name, age) VALUES ('Manahil', 28);
INSERT INTO Ages (name, age) VALUES ('Cori', 13);
INSERT INTO Ages (name, age) VALUES ('Bill', 19);
INSERT INTO Ages (name, age) VALUES ('Charly', 20);
'''
# Insert users
cursor.execute('''INSERT INTO Ages (name, age) VALUES ('Liberty', 31)''')
cursor.execute('''INSERT INTO Ages (name, age) VALUES ('Manahil', 28)''')
cursor.execute('''INSERT INTO Ages (name, age) VALUES ('Cori', 13)''')
cursor.execute('''INSERT INTO Ages (name, age) VALUES ('Bill', 19)''')
cursor.execute('''INSERT INTO Ages (name, age) VALUES ('Charly', 20)''')

#Select user
cursor.execute('''SELECT hex(name || age) AS X FROM Ages ORDER BY X''')

#retrieve the first row
user1 = cursor.fetchone()
#Print the first column retrieved(user's name)
print("The first row in the resulting record set : "+user1[0])

#Commit changes into database
db.commit()
#Close database
db.close()