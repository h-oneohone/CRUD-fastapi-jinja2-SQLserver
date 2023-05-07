import pyodbc

# conn = pyodbc.connect('Driver={SQL Server};'
#                       'Server=TLE;'
#                       'Database=shopee;'
#                       'Trusted_Connection=yes;')
# cursor = conn.cursor()
# print("Connected to database")
# print(cursor)
# cursor.execute('SELECT * FROM [shopee].[dbo].[customer]')
# rows = cursor.fetchall()

# for row in rows:
#     print(row)

conn = pyodbc.connect('Driver={SQL Server};'
                    'Server=TLE;'
                    'Database=shopee;'
                    'Trusted_Connection=yes;')
cursor = conn.cursor()
cursor.execute('SELECT * FROM [shopee].[dbo].[customer]')
rows = cursor.fetchall()
customers = []
for row in rows:
    customers.append({
        "customer_id": row[0],
        "customer_name": row[1],
        "id_headquarter": row[2],
        "phone_number": row[3],
        "address": row[4],
    })
print(customers)