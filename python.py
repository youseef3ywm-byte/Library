
#Setting up the libraries
import pandas as pd
import sqlite3
#Setting up the connection to the database
conn=sqlite3.connect('Level3_final_project_library.db')

def run(query):
    return pd.read_sql_query(query,conn)


query = '''
select * from members
'''

print(run(query))

print("--------------------Members_table---------------------")
print()
query = '''
select * from members
'''

print(run(query))

print("--------------------Checkouts_table---------------------")
print()
query = '''
SELECT * FROM Checkouts
'''
print(run(query))

print("--------------------Books_table---------------------")
print()
query = '''
SELECT * FROM Books
'''
print(run(query))

print("--------------------First_question---------------------")
print()
query = '''
SELECT Members.member_id,
 Members.first_name || ' ' || Members.last_name AS full_name,
 COUNT(Checkouts.Member_id) AS name_counts
 FROM Checkouts
 JOIN Members
 ON Checkouts.member_id = Members.member_id
 GROUP BY full_name , Checkouts.member_id
 ORDER BY name_counts DESC
'''
print(run(query))
print()
print("--------------------Second_question---------------------")
print()
query = '''
SELECT title FROM Books WHERE title LIKE 'The%'
'''
print(run(query))
print()
print(" \n I selected the name titles that start with 'The' pattern.")
print()
print("--------------------Third_question---------------------")
print()
query = """
SELECT
    Checkouts.book_id,
    Books.title,
    Books.author,
    COUNT(Checkouts.book_id) AS borrow_count
FROM Checkouts
JOIN Books
ON Checkouts.book_id = Books.book_id
GROUP BY Checkouts.book_id, Books.title, Books.author
ORDER BY borrow_count DESC
LIMIT 5
"""
print(run(query))
print()
print("--------------------Fourth_question---------------------")
print()
query = '''
SELECT
Checkouts.member_id,
Members.first_name || ' ' || Members.last_name AS member_name,
COUNT(Checkouts.member_id) AS Books_borrowed
FROM Checkouts
JOIN Members
ON Checkouts.member_id = Members.member_id
GROUP BY Checkouts.member_id, member_name
ORDER BY Books_borrowed DESC
LIMIT 10
'''
print(run(query))
print()
print("--------------------Fifth_question---------------------")
print()
query = '''
SELECT
Members.neighborhood,
Checkouts.checkout_id,
Checkouts.checkout_date

FROM Checkouts
JOIN Members
ON Checkouts.member_id = Members.member_id
WHERE Members.neighborhood = 'Shubra'
ORDER BY checkout_date DESC
LIMIT 10 OFFSET 10
'''
print(run(query))
print()
print("The selected neighborhood is Shubra.")
print()
print("--------------------First_stage---------------------")
print()
Members = pd.read_sql('SELECT * FROM Members' , conn)
Checkouts = pd.read_sql('SELECT * FROM Checkouts' , conn)
Stage1 = pd.merge(Members , Checkouts , on = 'member_id')
Stage1['books_borrowed'] = Stage1.groupby('member_id')['checkout_id'].transform("count")
Stage1 = Stage1.sort_values(by = 'checkout_id' )
print(Stage1)
print()

print("--------------------Second_stage---------------------")
print()
Book_catalog = pd.read_json('Level3_final_project_library.json')
Stage2 = pd.merge(Book_catalog , Stage1 , on = 'book_id')
print(Stage2)
print()
print("--------------------Third_stage---------------------")
print()
kickoff_file = pd.read_html("Level3_final_project_library.html")[0]
kickoff_file.columns = ['member_id' , 'book_id' , 'checkout_date']
kickoff_file = kickoff_file.merge( Members , on = 'member_id')
kickoff_file = kickoff_file.merge( Book_catalog , on ='book_id' )
Stage3 = pd.concat([kickoff_file , Stage2] , ignore_index = True)
print(Stage3)
print("===============================================================================================================")
print("______________________________________Preparation_the_combined_file_________________________________________________________")
print()
print("-----------------------------------Data Verfication-----------------------------------")
print()
print(f"1_Record count is {len(Stage3)}")
print()
print(f"2_the columns : {list(Stage3.columns)}")
print()
print(f"3_Sample rows:\n {Stage3.head(10)}")

Stage3.to_csv('31006190202239-Library-task1_combined_data.csv')
print("Combined data saved to CSV file.")