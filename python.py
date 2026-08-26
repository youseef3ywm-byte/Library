print("_____________________________________________________________________TASK1_____________________________________________________________________")
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

Stage3.to_csv('31006190202239-Library-task1_combined_data.csv' , index = False)
print("Combined data saved to CSV file.")
print()
print("----------------------------Importing_the_combined_csv_file----------------------------")
print()
combined_file = pd.read_csv('31006190202239-Library-task1_combined_data.csv')
combined_file
print()
print()
print("_____________________________________________________________________TASK2_____________________________________________________________________")
print()
print()
print("-------------------------First_problem(missing_values)--------------------------")
print()
print(f"NANs sum before: \n{combined_file.isna().sum()} ")
print()
print(f"The missing values rows:\n{combined_file[combined_file.isna().any(axis=1)]}")
combined_file['checkout_id'] = combined_file['checkout_id'].fillna('-')
combined_file['books_borrowed'] = combined_file.groupby('member_id')['book_id'].transform('count')
combined_file['return_date'] = combined_file['return_date'].fillna('Not returned')
combined_file['publication_year'] = combined_file['publication_year'].fillna('Unknown')
combined_file['grade'] = combined_file['grade'].fillna(combined_file['grade'].mode()[0])
combined_file['join_date'] = combined_file['join_date'].fillna('Unknown')
print()
print(f"NANs sum after: \n{combined_file.isna().sum()}")
print()
print("-------------------------Second_problem(Duplicated_values)--------------------------")
print()
print(f"The Shape before:\n{combined_file.shape}")
print()
print(f"The duplicated values before\n{combined_file.duplicated().sum()}")
print()
print(f"The count of every record before cleaning:\n{combined_file.value_counts()}")
combined_file = combined_file.drop_duplicates()
print()
print("--"*10000)
print(f"The count of every record after cleaning:\n{combined_file.value_counts()}")
print("--"*10000)
print(f"The value counts of checkout_id column:\n{combined_file['checkout_id'].value_counts()}")
print()
print(f"The duplicated values after\n{combined_file.duplicated().sum()}")
print()
print(f"The shape after:\n{combined_file.shape}")
combined_file = combined_file.reset_index(drop=True)
print()
print("-------------------------Additional_problem(Data_types_format)--------------------------")
print()
print(f"The data types of every column:\n{combined_file.dtypes}")
print()
combined_file['grade'] = combined_file['grade'].astype(int)
combined_file[['checkout_id' , 'publication_year']] = combined_file[['checkout_id' , 'publication_year']].astype(str).replace('.0' , '' , regex = False)
print()
print("-------------------------Third_problem(Inconsistence_values)--------------------------")
print()
print(f"Unique values of first name  column:\n{combined_file['first_name'].unique()}")
print()
print(f"Unique values of last name column:\n{combined_file['last_name'].unique()}")
print()
print(f"Unique values of neighborhood column before:\n{combined_file['neighborhood'].unique()}")
combined_file['neighborhood'] = combined_file['neighborhood'].str.strip()
print()
combined_file['neighborhood'] = combined_file['neighborhood'].replace({
    "HELIOPOLIS" : "Heliopolis",
    "zamalek":"Zamalek",
    "NASR CITY":"Nasr City"

})
print()
print(f"Unique values of neighborhood after:\n{combined_file['neighborhood'].unique()}")
print()
print(f"Unique values of membership status column before:\n{combined_file['membership_status'].unique()}")
print()
combined_file['membership_status'] = combined_file['membership_status'].str.capitalize()
print(f"Unique values of membership status column after:\n{combined_file['membership_status'].unique()}")
print()
print(f"Unique values of genre column:\n{combined_file['genre'].unique()}")
print()
print(f"Unique values of publisher column:\n{combined_file['publisher'].unique()}")
print()
print(f"All the values of the two fixed columns:\n{combined_file[['neighborhood' , 'membership_status']]}")
print()
print("-------------------------Fourth_problem(Checkouts with no matching member)--------------------------")
print()
Invalid_checkouts = combined_file[~combined_file['member_id'].isin(Members['member_id'])]
print(Invalid_checkouts)
print()
combined_file.to_csv('31006190202239-Library-task2_cleaned_data.csv' , index = False)
print("cleaned csv has saved successfully!")