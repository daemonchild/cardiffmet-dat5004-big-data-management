# 
# Title:        Cricketers Database
# Description:  A simple database program to store and retrieve cricketers using SQLite3
# Author:       Tom Rowan
# Student ID:   ST20285213
# Course code:  DAT-5004-S2_24
# Assignment:   PRAC1 - Task 2
# Course tutor: Dr. Sandeep Sengar
# 

### Import Standard Python Libraries
import os
import sqlite3
import re
from datetime import datetime as dt

# Colours
from colorama import Fore, Back, Style

# Import Pandas to populate database with demo data
import pandas as pd


logo = r'''
           _      _        _                      _       _        _                  
  ___ _ __(_) ___| | _____| |_ ___ _ __ ___    __| | __ _| |_ __ _| |__   __ _ ___  ___ 
 / __| '__| |/ __| |/ / _ \ __/ _ \ '__/ __|  / _` |/ _` | __/ _` | '_ \ / _` / __|/ _ \
| (__| |  | | (__|   <  __/ ||  __/ |  \__ \ | (_| | (_| | || (_| | |_) | (_| \__ \  __/
 \___|_|  |_|\___|_|\_\___|\__\___|_|  |___/  \__,_|\__,_|\__\__,_|_.__/ \__,_|___/\___|
 '''                                                                                      
 
#
#       ***** Short Utility Functions *****
#

# Adds string padding to a string (left or right side)
def string_padding (a_string, length,side="right"):
    if len(a_string) < length:
        # Pad the string with spaces
        if side == "left":
            # Pad on the left
            return " " * (length - len(a_string)) + a_string        
        else:
            return a_string + " " * (length - len(a_string))    
    else:
        # Truncate the string to the specified length
        return a_string[:length]

# Caters for intials as well as capitalising all words
# Eg 1: "tom rowan" -> "Tom Rowan"
# Eg 2: "tABC rowan" -> "TABC Rowan" (initials stay as is)
def capitalize_words_keep_existing(a_string):
    return re.sub(r'\b[a-z]', lambda match: match.group().upper(), a_string)

#
#       ***** Define Cricketer Class *****
#

# This class defines an object for a Cricketer
class Cricketer:

    # New Cricketer object
    # Init function tales optional parameters to allow for multiple ways to initialise a new object
    # Provide either a db_object or all the other parameters by name
    def __init__(self, name="", country="", 
                 matches_played=0, runs_scored=0, 
                 high_score=0, batting_average=0, 
                 year_started=0, year_retired=0,    
                 ## -- Or --
                 db_object=None):

        if db_object:
            if len (db_object) == 9:
                # If a db_object is passed in, use that to populate the object
                # A db_object = (id, name, country, matches_played, runs_scored, high_score, batting_average, year_started, year_retired)
                # Eg: [(123, 'Bob Jones', 'Wales', 34, 123, 17, 1.1, 1910, 1915)]
                # (So we ignore the ID field)

                self.name = db_object[1]
                self.country = db_object[2]
                self.matches_played = db_object[3]
                self.runs_scored = db_object[4]
                self.high_score = db_object[5]
                self.batting_average = db_object[6]
                self.year_started = db_object[7]
                self.year_retired = db_object[8]
            
        else:
            # Simply copy the parameter values nto the object
            self.name = name
            self.country = country
            self.matches_played = matches_played
            self.runs_scored = runs_scored
            self.high_score = high_score
            self.batting_average = batting_average
            self.year_started = year_started 
            self.year_retired = year_retired

    # This function returns a string representation of the object
    def __str__(self):
        if self.year_retired == 0:
            retired = "Present"
        else:
            retired = self.year_retired
        return f"{self.name} ({self.country}) - Matches: {self.matches_played}, Runs: {self.runs_scored}, High Score: {self.high_score}, Average: {self.batting_average}, Years Active: {self.year_started} - {retired}"

    # This function returns a padded string representation of the object
    # This is used to print the results table
    def paddedstr(self):
        if self.year_retired == 0:
            retired = "Present"
        else:
            retired = self.year_retired

        ret= ""
        ret += string_padding(self.name, 32) + string_padding(self.country, 16)
        ret += string_padding(str(self.matches_played), 8, side='left') + string_padding(str(self.runs_scored), 8 ,side='left')
        ret += string_padding(str(self.high_score), 16,side='left') + string_padding(str(self.batting_average), 18, side='left') + "  "
        ret += str(self.year_started) + " - " + string_padding(str(retired), 8)
        return ret


    table_sql = """ CREATE TABLE Cricketers (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                name            TEXT(128) NOT NULL,
                country         TEXT(64) NOT NULL,
                matches_played  INT(5),
                runs_scored     INT(6),
                high_score      INT(4),
                batting_average REAL(6),
                year_started    INT(4),
                year_retired    INT(4)
                ); """

#
#       ***** Database Management Functions *****
#

# This function creates an empty database
def init_database (filename):

    # Connect to a SQLite database
    db_connection = sqlite3.connect(filename)
    # Create cursor object
    db_cursor = db_connection.cursor()
    
    # Drop table if already exists - wipe all old data
    db_cursor.execute("DROP TABLE IF EXISTS Cricketers;")

    # Define schema for the Cricketers table
    table_sql = """ CREATE TABLE Cricketers (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                name            TEXT(128) NOT NULL,
                country         TEXT(64) NOT NULL,
                matches_played  INT(5),
                runs_scored     INT(6),
                high_score      INT(4),
                batting_average REAL(6),
                year_started    INT(4),
                year_retired    INT(4)
                ); """
    
    # Execute the SQL query
    db_cursor.execute(table_sql)
    db_connection.commit()

    # Close the database connection
    db_cursor.close()



# Connect to a database
# Return a db_connection and db_cursor object to work with the databae
# The database should already be initialised with the correct table
def connect_database (filename):

    # Connect to a SQLite database
    db_connection = sqlite3.connect(filename)
    # Create cursor object
    db_cursor = db_connection.cursor()

    return db_cursor,db_connection 


# This function fills database with example data from a HTML file
# The HTML file "table.html" comes from https://www.espncricinfo.com/
# This website resists scraping by automated means, so a manual download was used
# Website accessed on 12/03/2025; data is for example purposes only
def fill_with_data_from_html (db_cursor):

    country_codes = {
        'AUS': 'Australia',
        'BAN': 'Bangladesh',
        'ENG': 'England',
        'IND': 'India',
        'IRE': 'Ireland',
        'NZ': 'New Zealand',
        'PAK': 'Pakistan',
        'SA': 'South Africa',
        'SL': 'Sri Lanka',
        'WI': 'West Indies',
        'ZIM': 'Zimbabwe'
    }

    try:
        filehandle = open('table.html')
        tables = pd.read_html(filehandle)
        filehandle.close()
    except:
        print (Fore.RED + "Error: Unable to read HTML file. Please check the file exists." + Style.RESET_ALL)

    if len(tables) > 0:
        df = pd.DataFrame(tables[0])

        # Write out the data to a CSV file for debugging
        df.to_csv('cricketers_data.csv', sep=',', encoding='utf-8', index=False)

        # Loop through the dataframe and insert each row into the database
        for index, row in df.iterrows():
            name = row['Player'].split('(')[0].strip()
            countrycode = row['Player'].split('(')[1].replace(")","")

            # Remove the ICC prefix from the country name
            if "ICC" in countrycode:
                countrycode = countrycode.split("/")[1].strip()

            country = country_codes[countrycode]

            matches_played = int(row['Mat'])
            runs_scored = int(row['Runs'])
            high_score = int(row['HS'].replace("*", ""))
            batting_average = float(row['Ave'])

            # Split out the years active from the 'span' column
            # Eg: 2000-2010
            year_started = row['Span'].split('-')[0].strip()
            year_retired = row['Span'].split('-')[1].strip()

            # Create a new Cricketer object
            new_cricketer = Cricketer(name=name, country=country, matches_played=matches_played, runs_scored=runs_scored, high_score=high_score, batting_average=batting_average, year_started=year_started, year_retired=year_retired)
            # Insert the new cricketer into the database
            insert_cricketer (db_cursor, new_cricketer)
    else:
        print (Fore.RED + "Error: No tables found..." + Style.RESET_ALL)


#
#       ***** Perform Database Queries *****
#

# Generic function to run a simple SQL query
# (NB: This would allow SQL injection attacks if used in a real world application)
def find_by_single_field (db_cursor, field, searchterm, exact_match=False):

    if exact_match:
        sql_query = "SELECT * FROM Cricketers WHERE {} = '{}' COLLATE NOCASE;".format(field, searchterm)
    else:
        sql_query = "SELECT * FROM Cricketers WHERE {} LIKE '%{}%' COLLATE NOCASE;".format(field, searchterm)

    # Execute the SQL query
    db_cursor.execute(sql_query)

    # Fetch the output and convert to a list of Cricketer objects
    output = db_cursor.fetchall()

    if len(output) > 0:
        cricketers = []

        # Cycle through the output and create a new Cricketer object for each row
        # Append the new object to the list
        for row in output:
            new_cricketer = Cricketer(db_object=row)
            cricketers.append(new_cricketer)
        return cricketers
    else:
        return []


# Find a cricketer by name
# NB - does not use an exact match by default
def find_by_name (db_cursor, name, exact_match=False):

    results = find_by_single_field (db_cursor, 'name', name, exact_match=exact_match)    
    return results


# Find all cricketers by country
def find_by_country (db_cursor, country):

    results = find_by_single_field (db_cursor, 'country', country, exact_match=False)    
    return results


# Find the cricketer with the highest score
def find_best_score (db_cursor):
    
    # There are several ways to imnplement this query
    # Eg: sql_query = "SELECT * FROM Cricketers ORDER BY high_score DESC LIMIT 1;"
    # This should be the most efficient way to do it for a large table:
    sql_query = "SELECT * FROM Cricketers WHERE high_score = (SELECT MAX(high_score) FROM Cricketers);"

    # Execute the SQL query
    db_cursor.execute(sql_query)

    # Fetch the output and convert to a list of Cricketer objects
    # This should only return one row, but it will be returned as a list for the display function
    output = db_cursor.fetchall()

    if len(output) > 0:
        cricketers = []
        for row in output:
            new_cricketer = Cricketer(db_object=row)
            cricketers.append(new_cricketer)
        return cricketers
    else:
        return []
    

# Generic function to find top x cricketers by a given field
def find_top_x (db_cursor, field, x=10):

    # Define the SQL query
    sql_query = f"SELECT * FROM Cricketers ORDER BY {field} DESC LIMIT {x};"

    # Execute the SQL query
    db_cursor.execute(sql_query)

    # Fetch the output and convert to a list of Cricketer objects
    output = db_cursor.fetchall()

    if len(output) > 0:
        cricketers = []
        for row in output:
            new_cricketer = Cricketer(db_object=row)
            cricketers.append(new_cricketer)
        return cricketers
    else:
        return []



    

# Find a cricketer by ID
# NB: Not used...
def find_by_id (db_cursor, id):

    sql_query = "SELECT * FROM Cricketers WHERE id = '{}'".format(id)

    db_cursor.execute(sql_query)
    output = db_cursor.fetchall()
    return (output)


# Insert a new cricketer into the database
def insert_cricketer (db_cursor, new_cricketer):

    # Check if the cricketer already exists
    output = find_by_name(db_cursor, new_cricketer.name, exact_match=True)
    if len(output) == 0:
    
        sql_query = ''' INSERT INTO Cricketers (
                    name, country, matches_played, runs_scored, high_score, batting_average, year_started, year_retired
                    ) 
                    VALUES ( 
                    '{}', '{}', {}, {}, {}, {}, {}, {}
                    );
                    '''.format(new_cricketer.name, 
                               new_cricketer.country, 
                               new_cricketer.matches_played,
                               new_cricketer.runs_scored,
                               new_cricketer.high_score,
                               new_cricketer.batting_average,
                               new_cricketer.year_started,
                               new_cricketer.year_retired)
        db_cursor.execute(sql_query)
        db_connection.commit()
        print (Fore.GREEN + f"Cricketer {new_cricketer.name} added successfully." + Style.RESET_ALL)
    else: 
        # They exist already, so the user should run an update...
        print (Fore.RED + "Error: Cricketer already exists. Update instead." + Style.RESET_ALL)

# Delete a cricketer from the database
def delete_cricketer (db_cursor, name):

    # It only makes sense to delete a cricketer if they exist
    output = find_by_name(db_cursor, name, exact_match=True)
    if len(output) > 0:

        # They exist, so delete them
        sql_query = ''' DELETE FROM Cricketers WHERE name = '{}'; '''.format(name)
        db_cursor.execute(sql_query)
        db_connection.commit()
        print (Fore.GREEN + f"Deleted {name} successfully." + Style.RESET_ALL)
    else: 
        print (Fore.RED + f"Error! {name} not found." + Style.RESET_ALL)




# Update a cricketer's details
def update_cricketer (db_cursor,name):

    # It only makes sense to update a cricketer if they exist
    output = find_by_name(db_cursor, name, exact_match=True)
    if len(output) > 0:

        # They exist, so get the cricketer's details
        updated_cricketer = get_cricketer_details(name=name)

        sql_query = ''' UPDATE Cricketers SET 
                    country = '{}',
                    matches_played = {},
                    runs_scored = {},
                    high_score = {},
                    batting_average = {},
                    year_started = {},
                    year_retired = {} 
                    WHERE name = '{}';
                    '''.format(updated_cricketer.country, 
                               updated_cricketer.matches_played, 
                               updated_cricketer.runs_scored,
                               updated_cricketer.high_score,
                               updated_cricketer.batting_average,
                               updated_cricketer.year_started,
                               updated_cricketer.year_retired,
                               updated_cricketer.name)
        # Execute the SQL query
        db_cursor.execute(sql_query)
        db_connection.commit()

        print (Fore.GREEN + f"Updated {updated_cricketer.name} successfully." + Style.RESET_ALL)
    else: 
        print (Fore.RED + f"Error! {name} not found." + Style.RESET_ALL)


# Get all cricketers from the database
# Takes optional 'order_by' parameter to sort the results
def fetch_all_cricketers (db_cursor, order_by='name'):

    # Define the SQL query
    sql_query = f""" SELECT * from Cricketers ORDER by {order_by}; """

    # Execute the SQL query
    db_cursor.execute(sql_query)

    # Convert the output to a list of Cricketer objects
    output = db_cursor.fetchall()
    if len(output) > 0:
        cricketers = []
        for row in output:
            new_cricketer = Cricketer(db_object=row)
            cricketers.append(new_cricketer)
        return cricketers
    else:
        return []


def list_countries (db_cursor):

    # Define the SQL query
    sql_query = "SELECT DISTINCT country FROM Cricketers;"

    # Execute the SQL query
    db_cursor.execute(sql_query)

    # Convert the output to a list of country names
    output = db_cursor.fetchall()
    if len(output) > 0:
        countries = []
        for row in output:
            countries.append(row[0])
        return countries
    else:
        return []


#
#       ***** Menu System *****
#

# This function gets the cricketer details from the user
# It takes an optional name parameter to allow for updating an existing cricketer
def get_cricketer_details (name=None):

    # Get the current year
    this_year = dt.now().year

    # If a name is provided, use this to find the cricketer in the database
    # Then we can provide default options to help the user out
    if name:
        result = find_by_name(db_cursor, name, exact_match=True)
        if len(result) > 0:
            print ("Note: hit enter to accept current values.")
            country = input(f"Enter country [{result[0].country}]: ")
            if country == "":
                country = result[0].country
            else:
                country = capitalize_words_keep_existing(country)
            
            matches_played = input(f"Enter number of matches played {result[0].matches_played}: ")
            if matches_played == "":
                matches_played = result[0].matches_played
            else:
                matches_played = int(matches_played)

            runs_scored = input(f"Enter runs scored [{result[0].runs_scored}]: ")
            if runs_scored == "":
                runs_scored = result[0].runs_scored
            else:   
                runs_scored = int(runs_scored)

            high_score = input(f"Enter high score [{result[0].high_score}]: ")
            if high_score == "":
                high_score = result[0].high_score
            else:
                high_score = int(high_score)

            batting_average = input(f"Enter batting average [{result[0].batting_average}]: ")
            if batting_average == "":
                batting_average = result[0].batting_average
            else:
                batting_average = float(batting_average)

            year_started = input(f"Enter year career started [{result[0].year_started}]: ")
            if year_started == "":
                year_started = result[0].year_started
            else:
                year_started = int(year_started)

            year_retired = input(f"Enter year retired (enter 0 if still active) [{result[0].year_retired}]: ")
            if year_retired == "":
                year_retired = result[0].year_retired
            else:
                if year_retired > this_year:
                    print (Fore.RED + "Warning: Year retired is greater than current year." + Style.RESET_ALL)
                if year_retired != "0" and year_retired < year_started:
                    print (Fore.RED + "Warning: Year retired is before year started." + Style.RESET_ALL)

            new_cricketer = Cricketer(name=name, country=country, matches_played=matches_played, runs_scored=runs_scored, high_score=high_score, batting_average=batting_average, year_started=year_started, year_retired=year_retired)
            return new_cricketer

    # The calling function didn't set a name, and/or we didn't find the cricketer they asked for so:

    name = input(f"Enter name: ")
    name = capitalize_words_keep_existing(name)
    country = input(f"Enter country: ")
    country = capitalize_words_keep_existing(country)
    matches_played = int(input(f"Enter number of matches played: "))
    runs_scored = int(input(f"Enter runs scored: "))
    high_score = int(input(f"Enter high score: "))
    batting_average = float(input(f"Enter batting average: "))
    year_started = input(f"Enter year career started: ")
    year_retired = input(f"Enter year retired (enter 0 if still active): ")

    new_cricketer = Cricketer(name, country, matches_played, runs_scored, high_score, batting_average, year_started, year_retired)
    return new_cricketer


# Print Results Table
def print_results_table (results, table_title = "Results"):

    if len(results) < 1:
        print (Fore.RED + "No results found" + Style.RESET_ALL)
    else:
        print ("")
        print (Fore.YELLOW + table_title + Style.RESET_ALL)

        header_row = string_padding("Name", 32) + string_padding("Country", 16)
        header_row += string_padding("Matches", 8,side='left') + string_padding("Runs", 8,side='left')
        header_row += string_padding("High Score", 16,side='left') + string_padding("Batting Average", 18,side='left') + "  "
        header_row += string_padding("Years Active", 12)
        print ((len(header_row)+2) * "-")
        print (header_row)
        print ((len(header_row)+2) * "-")

        # Print each row of the results in alternating stripes
        row_count = 0
        for row in results:
            if row_count % 2 == 0:
                print (Fore.CYAN + row.paddedstr() + Style.RESET_ALL)
            else:   
                print (Fore.WHITE + row.paddedstr() + Style.RESET_ALL)
            row_count += 1

        print ((len(header_row)+2) * "-")
        print ("Total Results: ", len(results))
        print ((len(header_row)+2) * "-")
        print ("")

# List the menu options
main_menu_text = """
  1. Insert Cricketer
  2. View All Cricketers
  3. Find Cricketer by Name
  4. Find Best Score (on 'High Score')
  5. Update Cricketer
  6. Delete Cricketer
"""

menu_extended = """
 10. Find Cricketers by Country
 11. List Top 10 Cricketers by High Score
 12. List Top 10 Cricketers by Batting Average
 13. List Top 10 Cricketers by Matches Played
 14. List Top 10 Cricketers by Runs Scored
"""

# This function defines the main menu
def main_menu (db_cursor, extended = False):

    # Loop until the user quits
    while True:
        
        # Display the Menu
        print ("")
        print (Fore.YELLOW + Style.BRIGHT + "   Cricketers Database - Main Menu   " + Style.RESET_ALL)
        print (Fore.YELLOW + Style.BRIGHT + "-------------------------------------" + Style.RESET_ALL)
        print (Fore.CYAN+ "-- Required Options --" + Style.RESET_ALL, end="")
        print (main_menu_text)
        if extended:
            print (Fore.CYAN + "-- Extended Menu --" + Style.RESET_ALL, end="")
            print (menu_extended)

        print (Fore.CYAN+ "-- Program Options --" + Style.RESET_ALL)      
        print (" 90. Load example data from HTML file (table.html)")
        print("")
        print (Fore.GREEN + " 99. Quit" + Style.RESET_ALL)

        choice = input("Select an option: ")

        # Menu options requested in the assignment (1-6)

        if choice == '1':
            # Insert Cricketer
            new_cricketer = get_cricketer_details ()
            insert_cricketer(db_cursor, new_cricketer)

        elif choice == '2':
            # View All Cricketers
            results = fetch_all_cricketers(db_cursor)
            print_results_table(results,table_title="All Cricketers")

        elif choice == '3':
            # Find Cricketer by Name
            name = input("Enter name: ")
            results = find_by_name(db_cursor, name)
            print_results_table(results, table_title="Cricketers matching: " + name)

        elif choice == '4':
            # Find Best Score
            results = find_best_score(db_cursor)
            print_results_table(results, table_title="Best Score")

        elif choice == '5':
            # Update Cricketer
            name = input("Enter name to update: ")
            update_cricketer (db_cursor, name)

        elif choice == '6':
            # Delete Cricketer
            name = input("Enter name to delete: ")
            delete_cricketer (db_cursor, name)

        # Extended Menu Options (10+)

        elif choice == '10':

            valid_countries = list_countries(db_cursor)
            print ("Countries in the database currently: ")
            for country in valid_countries:
                print (Fore.CYAN + " - " + country + Style.RESET_ALL)
            print ("")
            entry = input("Enter Country: ")
            results = find_by_country(db_cursor, entry)
            print_results_table(results, table_title="Cricketers from " + entry)

        elif choice == '11':
            results = find_top_x(db_cursor, 'high_score', x=10)
            print_results_table(results, table_title="Top 10 Cricketers by High Score")
        
        elif choice == '12':
            results = find_top_x(db_cursor, 'batting_average', x=10)
            print_results_table(results, table_title="Top 10 Cricketers by Batting Average")
        
        elif choice == '13':
            results = find_top_x(db_cursor, 'matches_played', x=10)
            print_results_table(results, table_title="Top 10 Cricketers by Matches Played")

        elif choice == '14':
            results = find_top_x(db_cursor, 'runs_scored', x=10)
            print_results_table(results, table_title="Top 10 Cricketers by Runs Scored")


        elif choice == '90':
            # Load data from HTML file
            fill_with_data_from_html(db_cursor)


        # Quit the program
        
        elif choice == '99':
            break

        else:
            print ("Invalid option")










### Main program starts here

# Banner
print ("\n")
print (Fore.GREEN + Style.BRIGHT + logo + Style.RESET_ALL)
print (Fore.WHITE + "     by Tom Rowan, ST20285213" + Style.RESET_ALL)
print ("")

# Top Level Program Control Variables
# Set this to True to enable the extended menu options
EXTENDED_MENU = True
filename = 'cricketers.sqlite3'

if not os.path.exists(filename):
    print (Fore.RED + f"-- Initialising database {filename}" + Style.RESET_ALL)
    init_database(filename)
else:
    print (Fore.MAGENTA + f"-- Opening database {filename}" + Style.RESET_ALL)

db_cursor,db_connection = connect_database(filename)
main_menu(db_cursor, extended=EXTENDED_MENU)

# Commit changes and close the database connection1
db_connection.commit()
db_cursor.close()

