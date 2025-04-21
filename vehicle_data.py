import sqlite3



class VehicleDataFuntionsDB():

        #Conntect to db
    def connect_vehicle_db(self):
        self.conn = sqlite3.connect('vehicles.bd')
        self.cursor = self.conn.cursor()

    #Disconntect to db
    def desconnect_vehicle_db(self):
        self.conn.close()

    #Create vehicle tables
    def createTableVehicles(self):
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
    def addVehiclesDB(self,marca,modelo,placa,quilometragem,ano,combustivel):       
        self.connect_vehicle_db()
        self.cursor.execute(""" INSERT INTO  vehicles (marca,modelo,placa,quilometragem,ano,combustivel)
                            VALUES (?,?,?,?,?,?)""", (marca,modelo,placa,quilometragem,ano,combustivel))
        self.conn.commit()
        self.desconnect_vehicle_db()
        print('Veiculo Adicionado')

    #Delete vehicle from db
    def deleteVehicleDB(self,cod):
        self.connect_vehicle_db()
        self.cursor.execute(""" DELETE FROM vehicles WHERE cod = ? """, (cod,))
        self.conn.commit()
        self.desconnect_vehicle_db()
        print('Veiculo Deletado')

    #Update vehicle from db
    def updateVehicleDB(self,marca,modelo,placa,quilometragem,ano,combustivel, cod):
        self.connect_vehicle_db()
        self.cursor.execute(""" UPDATE vehicles 
            SET  marca = ?,modelo = ?,placa = ?,quilometragem = ?,ano = ?,combustivel = ? WHERE cod = ? """,
            (marca,modelo,placa,quilometragem,ano,combustivel, cod))
        self.conn.commit()
        self.desconnect_vehicle_db()
        print('Veiculo Atualizado')

    def getVehiclesDB(self):
        self.connect_vehicle_db()
        cursorList = self.cursor.execute(""" SELECT cod,marca,modelo,placa,quilometragem,ano,combustivel
        FROM vehicles ORDER BY cod ASC;""").fetchall()#fetchall() retorna uma lista com todos os registros
        self.desconnect_vehicle_db()
        if cursorList == []:
            print('Veiculo não encontrado')
        else:
            print('Veiculos Encontratos')
        return cursorList
        
    def searchVehicleDB(self,marca):
        self.connect_vehicle_db()
        cursorList =self.cursor.execute(""" SELECT cod,marca,modelo,placa,quilometragem,ano,combustivel
        FROM vehicles WHERE marca LIKE '%s'ORDER BY cod ASC;""" % marca).fetchall()
        self.desconnect_vehicle_db()
        if cursorList == []:
            print('Veiculo não encontrado')
        else:
            print('Veiculo Encontrado')
        return cursorList