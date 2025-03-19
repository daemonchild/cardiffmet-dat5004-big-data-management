# Cricketers Database Program

import os
import sqlite3
import pandas as pd
import tkinter as tk


def init_database (filename):

    # Connect to a SQLite database
    db_connection = sqlite3.connect(filename)

    # Create cursor object
    db_cursor = db_connection.cursor()
    
    # Drop table if already exists.
    db_cursor.execute("DROP TABLE IF EXISTS Cricketers")

    # Creating table
    table_sql = """ CREATE TABLE Cricketers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT(128) NOT NULL,
                country TEXT(64) NOT NULL,
                matches_played INT(5),
                runs_scored INT(6),
                high_score INT(4),
                batting_average REAL(6),
                years_active TEXT(10)
                ); """
    
    db_cursor.execute(table_sql)
    db_connection.commit()
    db_cursor.close()


def fill_with_data_from_html (db_cursor):

    tables = pd.read_html('table.html')
    df = pd.DataFrame(tables[0])

    df.to_csv('cricketers_data.csv', sep=',', encoding='utf-8', index=False)

    for index, row in df.iterrows():
        name = row['Player'].split('(')[0].strip()
        country = row['Player'].split('(')[1].replace(")","")
        years_active = row['Span']
        matches_played = int(row['Mat'])
        runs_scored = int(row['Runs'])
        high_score = int(row['HS'].replace("*", ""))
        batting_average = float(row['Ave'])
        print("Inserting: ", name, country, matches_played, runs_scored, high_score, batting_average, years_active)
        insert_cricketer (db_cursor, name, country, matches_played, runs_scored, high_score, batting_average, years_active)


def connect_database (filename):

    # Connect to a SQLite database
    db_connection = sqlite3.connect(filename)

    # Create cursor object
    db_cursor = db_connection.cursor()

    return db_cursor,db_connection  


def find_by_name (db_cursor, name):

    sql_query = "SELECT * FROM Cricketers WHERE name = '{}'".format(name)

    db_cursor.execute(sql_query)
    output = db_cursor.fetchall()
    return (output)


def find_by_id (db_cursor, id):

    sql_query = "SELECT * FROM Cricketers WHERE id = '{}'".format(id)

    db_cursor.execute(sql_query)
    output = db_cursor.fetchall()
    return (output)


def insert_cricketer (db_cursor, name, country, matches_played,runs_scored,high_score,batting_average,years_active):

    output = find_by_name(db_cursor, name)
    if len(output) <1 :

        sql_query = ''' INSERT INTO Cricketers (
                    name, country, matches_played, runs_scored, high_score, batting_average, years_active
                    ) 
                    VALUES ( 
                    '{}', '{}', {}, {}, {}, {}, '{}'
                    );
                    '''.format(name, country, matches_played,runs_scored,high_score,batting_average,years_active)
        
        db_cursor.execute(sql_query)
    else: 
        print ("Error: Duplicate name")



def print_all_db (db_cursor):
    sql_query = """ SELECT * from Cricketers ; """
    db_cursor.execute(sql_query)
    print("All The Data:") 
    output = db_cursor.fetchall() 
    for row in output: 
        print(row) 



### Main program starts here
filename = 'cricketers.sqlite3'

if not os.path.exists(filename):
    print (f"Initialising database {filename}")
    init_database(filename)
    db_cursor,db_connection = connect_database(filename)
    fill_with_data_from_html (db_cursor)

else:
    db_cursor,db_connection = connect_database(filename)

# Start Application Window
# main_window.mainloop()

db_connection.commit()
db_cursor.close()

