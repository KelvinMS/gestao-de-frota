import sqlite3



class DriverDataFuntionsDB():

        #Conntect to db
    def connect_drive_db(self):
        self.conn = sqlite3.connect('drivers.bd')
        self.cursor = self.conn.cursor()

    #Disconntect to db
    def desconnect_driver_db(self):
        self.conn.close()

    #Create driver tables
    def createTableDrivers(self):
        self.connect_drive_db()
        print('Connected to DB')
        self.cursor.execute("""                                   
            CREATE TABLE IF NOT EXISTS drivers(
                cod INTEGER PRIMARY KEY,
                nome CHAR(15) NOT NULL,
                cpf CHAR(15) NOT NULL,
                cnh CHAR(20) NOT NULL,
                email CHAR(15) NOT NULL,
                telefone CHAR(40) NOT NULL,
                cnh_path CHAR(40) NOT NULL
                );
            """)
        self.conn.commit()
        print('Banco drivers Criado')

    #Add driver to db and update treeview
    def addDriveToDB(self,nome,cpf,cnh,email,telefone,cnh_path):       
        self.connect_drive_db()
        self.cursor.execute(""" INSERT INTO  drives (nome,cpf,cnh,email,telefone,cnh_path)
                            VALUES (?,?,?,?,?,?)""", (nome,cpf,cnh,email,telefone,cnh_path))
        self.conn.commit()
        self.desconnect_driver_db()
        print('Motorista Adicionado')

    #Delete driver from db
    def deleteDriverToDB(self,cod):
        self.connect_drive_db()
        self.cursor.execute(""" DELETE FROM drivers WHERE cod = ? """, (cod))
        self.conn.commit()
        self.desconnect_driver_db()
        print('Veiculo Deletado')

    #Update driver from db
    def updateDriversDB(self,nome,cpf,cnh,email,telefone,cnh_path, cod):
        self.connect_drive_db()
        self.cursor.execute(""" UPDATE drivers 
            SET  nome = ?,cpf = ?,cnh = ?,email = ?,telefone = ?,cnh_path = ? WHERE cod = ? """,
            (nome,cpf,cnh,email,telefone,cnh_path, cod))
        self.conn.commit()
        self.desconnect_driver_db()
        print('Motorista Atualizado')

    def getDriversDB(self):
        self.connect_drive_db()
        cursorList = self.cursor.execute(""" SELECT cod,nome,cpf,cnh,email,telefone,cnh_path
        FROM drivers ORDER BY cod ASC;""").fetchall()#fetchall() retorna uma lista com todos os registros
        self.desconnect_driver_db()
        if cursorList == []:
            print('Motorista não encontrado')
        else:
            print('Motorista Encontratos')
        return cursorList
        
    def searchDriverDB(self,nome):
        self.connect_drive_db()
        cursorList =self.cursor.execute(""" SELECT cod,nome,cpf,cnh,email,telefone,cnh_path
        FROM drivers WHERE nome LIKE '%s'ORDER BY cod ASC;""" % nome).fetchall()
        self.desconnect_driver_db()
        if cursorList == []:
            print('Motorista não encontrado')
        else:
            print('Motorista Encontrado')
        return cursorList