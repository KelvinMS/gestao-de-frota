import sqlite3



class VehicleDataDB():

        #Conntect to db
    def connect_vehicle_db(self):
        self.conn = sqlite3.connect('vehicles.bd')
        self.cursor = self.conn.cursor()

    #Disconntect to db
    def desconnect_vehicle_db(self):
        self.conn.close()

    #Create vehicle tables
    def createTables(self):
        self.connect_vehicle_db()
        print('Connected to DB')
        self.cursor.execute("""                                   
            CREATE TABLE IF NOT EXISTS vehicles(
                cod INTEGER PRIMARY KEY,
                marca CHAR(15) NOT NULL,
                modelo CHAR(15) NOT NULL,
                placa CHAR(20) NOT NULL,
                quilometragem CHAR(15) NOT NULL,
                ano CHAR(40) NOT NULL,
                combustivel CHAR(40) NOT NULL
                );
            """)
        self.conn.commit()
        print('Banco vehicles Criado')

    #Add vehicle to db and update treeview
    def addVehiclesDB(self):       
        self.connect_vehicle_db()
        self.cursor.execute(""" INSERT INTO  vehicles (marca,modelo,placa,quilometragem,ano,combustivel)
                            VALUES (?,?,?,?,?,?)""", (self.marca,self.modelo,self.placa,self.quilometragem,self.ano,self.combustivel))
        self.conn.commit()
        self.desconnect_vehicle_db()
        print('Veiculo Adicionado')

    