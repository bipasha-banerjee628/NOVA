import csv
import sqlite3
conn = sqlite3.connect("nova.db")

cursor = conn.cursor()

query= "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key,name VAECHAR(100),path VARCHAR(1000))"
cursor.execute(query)

query= "CREATE TABLE IF NOT EXISTS web_command(id integer primary key,name VAECHAR(100),url VARCHAR(1000))"
cursor.execute(query)

# query = "INSERT INTO sys_command VALUES(null,'microsoft edge','C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')"
# cursor.execute(query)
# conn.commit()
# query = "INSERT INTO  web_command VALUES(null,'github','https://github.com/')"
# cursor.execute(query)
# conn.commit()
query = "INSERT INTO web_command VALUES(null,'whatsapp','https://web.whatsapp.com/')"
cursor.execute(query)
conn.commit()
# query = "DELETE FROM web_command WHERE name='whatsapp'"
# cursor.execute(query)
# conn.commit()

# cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id INTEGER PRIMARY KEY, name VARCHAR(300), phone VARCHAR(255), email VARCHAR(255) NULL)''')

# desired_columns_indices = [0,19]

# with open ('contacts(1).csv','r',encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute('''INSERT INTO contacts (id,'name','phone') VALUES (null, ?,? );''',tuple(selected_data))
        
# conn.commit()
# conn.close()

# print("data inserted successfully")

# query = "INSERT INTO contacts VALUES(null,'baba','9709126287','null')"
# cursor.execute(query)
# conn.commit()


# query= 'Baba'
# query = query

# cursor.execute("SELECT phone FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
# results =cursor.fetchall()
# print(results[0][0])


# ------------------------to fetch a query
# query = 'mallika'
# query=query.lower()
# cursor.execute("SELECT phone FROM contacts WHERE LOWER(name) = ?", (query,))
# results = cursor.fetchall()                                                                        

# if results:
#     print(results[0][0])
# else:
#     print("No match found.")

# -----------------------to delete a query
# name_to_delete = 'Baba'.lower()

# cursor.execute("DELETE FROM contacts WHERE LOWER(name) = ?", (name_to_delete,))
# conn.commit()
# conn.close()

# print("Contact 'Baba' deleted successfully.")































































# import csv
# import sqlite3

# # Connect to database
# conn = sqlite3.connect("nova.db")
# cursor = conn.cursor()

# # Create tables if they don't exist
# cursor.execute("CREATE TABLE IF NOT EXISTS sys_command (id INTEGER PRIMARY KEY, name VARCHAR(100), path VARCHAR(1000))")
# cursor.execute("CREATE TABLE IF NOT EXISTS web_command (id INTEGER PRIMARY KEY, name VARCHAR(100), url VARCHAR(1000))")
# cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
#     id INTEGER PRIMARY KEY, 
#     name VARCHAR(300), 
#     phone VARCHAR(255), 
#     email VARCHAR(255) NULL
# )''')

# # Delete previous contact data (optional)
# cursor.execute("DELETE FROM contacts")
# print("Old contacts deleted.")

# # Set desired column indices
# desired_columns_indices = [0,18]

# # Load contacts from CSV
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     next(csvreader)  # Skip header row
#     for row in csvreader:
#         try:
#             selected_data = [row[i] for i in desired_columns_indices]
#             cursor.execute('''INSERT INTO contacts (id, name, phone) VALUES (null, ?, ?)''', tuple(selected_data))
#         except IndexError:
#             print(f"Skipped row (not enough columns): {row}")

# # Finalize
# conn.commit()
# conn.close()

# print("Data inserted successfully.")
