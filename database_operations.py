import psycopg2
from tabulate import tabulate
from datetime import date


def connect_database():
    try:
        #try to start a connection using credentials to my local pg4 server
        connection = psycopg2.connect(
            dbname="test",
            user="postgres",
            password="Cmilk333",
            host="localhost",
            port="5432"
        )
        print("Connected to database!")
        return connection
        #exception if we dont connect to database
    except psycopg2.Error as e:
        print("Unable to connect to database:", e)
        return None


#function for query execution
def executeQuery(connection, query, data=None, fetchOne=False):
    try:
        cursor = connection.cursor()

        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        
        if query.strip().split()[0].upper() == 'SELECT':
            if fetchOne:
                result = cursor.fetchone()
                return result
            else:
                results = cursor.fetchall()
                return results
            
        else:
            connection.commit()
            print("Query executed successfully")
    except psycopg2.Error as e:
        print("error executing: ", e)
    
    finally:
        if cursor:
            cursor.close()



def getHeaders(connection, tableName):
    try:
        # Create a cursor
        cursor = connection.cursor()

        # Execute query to get column names
        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{tableName}'")

        # Fetch all column names
        headers = [row[0] for row in cursor.fetchall()]

        # Close the cursor
        cursor.close()

        return headers

    except psycopg2.Error as e:
        print("Error retrieving table headers:", e)
        return None


#function to print tables in a nice way
def printTable(sql_query_result, headers, one=False):
    if not sql_query_result:
        print("No data found")
        return
    
    rows = []

    if(one):
        rows.append(sql_query_result)
        
    else:
        for row in sql_query_result:
            if not headers:
                headers = tuple(range(1, len(row) + 1))
            rows.append(row)

    print(tabulate(rows, headers=headers, tablefmt="grid"))