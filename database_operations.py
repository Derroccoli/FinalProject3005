import psycopg2
from datetime import date


def connect_database():
    try:
        #try to start a connection using credentials to my local pg4 server
        connection = psycopg2.connect(
            dbname="test",
            user="postgres",
            password="postgres",
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


