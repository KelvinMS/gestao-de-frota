import sqlite3

class DriverDataDB():

    #Conntect to db
    def connect_driver_db(self):
        self.conn = sqlite3.connect('driver.bd')
        self.cursor = self.conn.cursor()

    #Disconntect to db
    def desconnec_drive_db(self):
        self.conn.close()


    #Create vehicle tables
    def create_driver_db(self):
        self.connect_vehicle_db()
        print('Connected to DB')
        self.cursor.execute("""                                   
            CREATE TABLE IF NOT EXISTS drive(
                cod INTEGER PRIMARY KEY,
                nome CHAR(15) NOT NULL,
                cpf CHAR(15) NOT NULL,
                cnh_number CHAR(20) NOT NULL,
                email CHAR(15) NOT NULL,
                telefone CHAR(40) NOT NULL,
                cnh_file CHAR(40) NOT NULL
                );
            """)
        self.conn.commit()
        
        print('Banco driver Criado')

