import mysql.connector
 
def get_db_connection():
    return mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "fercho1232",
        database = "nouva",
        port=3306,
    )
#Ending