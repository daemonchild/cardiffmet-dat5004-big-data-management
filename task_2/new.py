




### Database Queries


def run_sql_query (query_string, db_cursor):
    return ("")










### Main program starts here

# Define Global Variables
filename = 'cricketers.sqlite3'

if not os.path.exists(filename):
    print (f"Initialising database {filename}")
    init_database(filename)
    db_cursor,db_connection = connect_database(filename)
    fill_with_data_from_html (db_cursor)

else:
    print (f"Opening database {filename}")
    db_cursor,db_connection = connect_database(filename)

db_connection.commit()
db_cursor.close()


