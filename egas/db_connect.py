import  mysql.connector as mysql

class db:
    def __init__(self):
        root = "eo"


    def connect(self):
        conn = mysql.connect(host="localhost", user="root", password="", database="egas_db")
        my_conn = conn.cursor()
        return my_conn