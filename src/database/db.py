import mysql.connector 

class Database:
    def connect(self):
        self.connection = mysql.connector.connect(
            host ="localhost",
            user="root",
            password = "1234",
            database= "trent"
            
        )
        

    def query(self,query, params=None):
        cursor = self.connection.cursor(dictionary =True)
        if params:
            cursor.execute(query,params)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
    
    def close(self):
        if self.connection.is_connected():
            self.connection.close()
