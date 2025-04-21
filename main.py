from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from tkinter import filedialog
import tkinter as tk
import vehicle_data
import drivers_data


root = Tk()


class VehiclesFunctions():

    # Get entry values from frame
    def entryCarVariables(self):
        self.cod = self.entry_cod.get()   
        self.marca = self.entry_marca.get()
        self.modelo = self.entry_modelo.get().upper()
        self.placa = self.entry_placa.get().upper()
        self.combustivel = self.entry_combustivel.get()   
        self.quilometragem = self.entry_quilometragem.get()
        self.ano = self.entry_ano.get()
        if not self.marca or not self.modelo or not self.placa or not self.ano:
           return False
        
    #Clean form Entrys
    def cleanFormCarEntry(self):
        self.entry_cod.delete(0,END)
        self.entry_marca.delete(0,END)
        self.entry_modelo.delete(0,END)
        self.entry_placa.delete(0,END)
        self.entry_quilometragem.delete(0,END)
        self.entry_ano.delete(0,END)
        self.entry_combustivel.delete(0,END)

    #Add vehicle to db and update treeview
    def addVehiclesDB(self):       
            result = self.entryCarVariables()
            if result == False:
                messagebox.showerror("Erro", "Preencha todos os campos necessários para adicionar veículo!")
                return
            vehicle_data.VehicleDataFuntionsDB.addVehiclesDB(self,self.marca,self.modelo,self.placa,self.quilometragem,self.ano,self.combustivel)
            self.updateVehiclesInTreeView()
            messagebox.showinfo("Sucesso", "Veículo adicionado com sucesso!")
    
    #Delete vehicle to db and update treeview
    def deleteVehicleDB(self):
        result = self.entryCarVariables()
        if result==False and not self.cod:
            messagebox.showerror("Erro", "Preencha o código do veículo!")
            return
        vehicle_data.VehicleDataFuntionsDB.deleteVehicleDB(self,self.cod)
        self.cleanFormCarEntry()
        self.updateVehiclesInTreeView()
        messagebox.showinfo("Sucesso", "Veículo removido com sucesso!")
  
    #Update vehicle into db and update treeview
    def updateVehicleDB(self):
        result = self.entryCarVariables()
        if result==False and not self.cod:
            messagebox.showerror("Erro", "Preencha o código do veículo!")
            return
        vehicle_data.VehicleDataFuntionsDB.updateVehicleDB(self,self.marca,self.modelo,self.placa,self.quilometragem,self.ano,self.combustivel,self.cod)
        self.cleanFormCarEntry()
        self.updateVehiclesInTreeView()
        messagebox.showinfo("Sucesso", "Informações do Veículo alteradas com sucesso!")

    #Update treeview with all vehicles from db
    def updateVehiclesInTreeView(self):
        self.treeView_table.delete(*self.treeView_table.get_children())
        cursorList = vehicle_data.VehicleDataFuntionsDB.getVehiclesDB(self)
        for i in cursorList:
            self.treeView_table.insert("",END, values=i)
        self.cleanFormCarEntry()
    
    
    def updateDriversInTreeView(self):
        self.treeView_table.delete(*self.treeView_table.get_children())
        cursorList = drivers_data.DriverDataFuntionsDB.getDriversDB(self)
        for i in cursorList:
            self.treeView_table.insert("",END, values=i)
        self.cleanFormDriverEntry()

    #Search vehicle in db and update treeview
    def searchVehicle(self):
        self.treeView_table.delete(*self.treeView_table.get_children())
        self.entry_marca.insert(END,'%') 
        marca = self.entry_marca.get()
        cursorList = vehicle_data.VehicleDataFuntionsDB.searchVehicleDB(self,marca)
        for i in cursorList:
            self.treeView_table.insert("",END, values=i)
        self.cleanFormCarEntry()
    
    #Load the values of treeview selection on Entrys
    def onDoubleClickVehicleTreeView(self,event):
        self.cleanFormCarEntry()
        self.treeView_table.selection()
        for entry in self.treeView_table.selection():
            col1,col2,col3,col4,col5,col6,col7,col8,col9 = self.treeView_table.item(entry,'values')
            self.entry_cod.insert(END,col1)
            self.entry_marca.insert(END,col2)
            self.entry_modelo.insert(END,col3)
            self.entry_placa.insert(END,col4)
            self.entry_quilometragem.insert(END,col5)
            self.entry_ano.insert(END,col6)
            self.entry_combustivel.insert(END,col7)

    #Load the values of treeview selection on Entrys
    def onDoubleClickDriverTreeView(self,event):
        self.cleanFormDriverEntry()
        self.treeView_table.selection()
        for entry in self.treeView_table.selection():
            col1,col2,col3,col4,col5,col6,col7 = self.treeView_table.item(entry,'values')
            self.entry_cod_driver.insert(END,col1)
            self.entry_name_driver.insert(END,col2)
            self.entry_cpf_driver.insert(END,col3)
            self.entry_cnh_driver.insert(END,col4)
            self.entry_email_driver.insert(END,col5)
            self.entry_phone_driver.insert(END,col6)
            self.label_attachment.config(text=col7)
                        

    def onTabChange(self,event):
        tab = event.widget.tab('current')['text']
        if tab == 'Veículos':	
            self.treeView_table.delete(*self.treeView_table.get_children())
            self.createTreeViewDataVehicles()
            self.updateVehiclesInTreeView()
        elif tab == 'Motoristas':
            self.treeView_table.delete(*self.treeView_table.get_children())
            self.createTreeViewDataDrivers()
            self.updateDriversInTreeView()

    
    

class DriversFunctions():

    
    # Get entry values from frame
    def entryDriverVariables(self):
        self.cod_driver = self.entry_cod_driver.get()   
        self.name_driver = self.entry_name_driver.get()
        self.cpf_driver = self.entry_cpf_driver.get().upper()
        self.cnh_driver = self.entry_cnh_driver.get().upper()
        self.email_driver = self.entry_email_driver.get()   
        self.phone_driver = self.entry_phone_driver.get()
        self.cnh_path = self.label_attachment.cget("text")
        
        if not self.name_driver or not self.cpf_driver or not self.cnh_driver:
           return False

    #Clean form Entrys
    def cleanFormDriverEntry(self):
        self.entry_cod_driver.delete(0,END)
        self.entry_name_driver.delete(0,END)
        self.entry_cpf_driver.delete(0,END)
        self.entry_cnh_driver.delete(0,END)
        self.entry_email_driver.delete(0,END)
        self.entry_phone_driver.delete(0,END)
        self.label_attachment.config(text="")

    #Add vehicle to db and update treeview
    def addDriverDB(self):       
            result = self.entryDriverVariables()
            if result == False:
                messagebox.showerror("Erro", "Preencha todos os campos necessários para adicionar Motorista!")
                return
            drivers_data.DriverDataFuntionsDB.addDriveToDB(self,self.name_driver,self.cpf_driver,self.cnh_driver,self.email_driver,self.phone_driver,self.cnh_path)
            self.updateDriversInTreeView()
            messagebox.showinfo("Sucesso", "Motorista adicionado com sucesso!")
    
    #Delete driver to db and update treeview
    def deleteDriverDB(self):
        result = self.entryDriverVariables()
        if result==False and not self.cod_driver:
            messagebox.showerror("Erro", "Preencha o código do Motorista!")
            return
        drivers_data.DriverDataFuntionsDB.deleteDriverToDB(self,self.cod_driver)
        self.cleanFormDriverEntry()
        self.updateDriversInTreeView()
        messagebox.showinfo("Sucesso", "Motorista removido com sucesso!")
  
    #Update vehicle into db and update treeview
    def updateDriverDB(self):
        result = self.entryDriverVariables()
        if result==False and not self.cod_driver:
            messagebox.showerror("Erro", "Preencha o código do motorista!")
            return
        drivers_data.DriverDataFuntionsDB.updateDriversDB(self,self.name_driver,self.cpf_driver,self.cnh_driver,self.email_driver,self.phone_driver,self.cnh_path,self.cod_driver)
        self.cleanFormDriverEntry()
        self.updateDriversInTreeView()
        messagebox.showinfo("Sucesso", "Informações do Motorista alteradas com sucesso!")

    #Search vehicle in db and update treeview
    def searchDriver(self):
        self.treeView_table.delete(*self.treeView_table.get_children())
        self.entry_name_driver.insert(END,'%') 
        name = self.entry_name_driver.get()
        cursorList = drivers_data.DriverDataFuntionsDB.searchDriverDB(self,name)
        for i in cursorList:
            self.treeView_table.insert("",END, values=i)
        self.cleanFormDriverEntry()
    
    #Update treeview with all vehicles from db
    def updateDriversInTreeView(self):
        self.treeView_table.delete(*self.treeView_table.get_children())
        cursorList = drivers_data.DriverDataFuntionsDB.getDriversDB(self)
        for i in cursorList:
            self.treeView_table.insert("",END, values=i)
        self.cleanFormDriverEntry()

    #Attachement logic
    def saveAttachment(self):
        self.attachment_path = filedialog.askopenfilename(title='Selecione um arquivo')
        self.label_attachment.config(text=self.attachment_path)
        
        return self.attachment


class Application(VehiclesFunctions,DriversFunctions,vehicle_data.VehicleDataFuntionsDB,drivers_data.DriverDataFuntionsDB):
    def __init__(self):
        self.root = root
        vehicle_data.VehicleDataFuntionsDB.createTableVehicles(self)
        drivers_data.DriverDataFuntionsDB.createTableDrivers(self)
        
        self.mainPage()
        self.frames()
        self.updateVehiclesInTreeView()
        self.menus()
        root.mainloop()

    def mainPage(self):
        self.root.title('Gestão de Frota')
        self.root.configure(background='RoyalBlue4')
        self.root.geometry('1200x720')
        self.root.resizable(False,False)
        self.root.minsize(width=600,height=350)

    #Creation of Frames
    def frames(self):
        self.framePanelData_1 = Frame(self.root,bd=4,bg='#dfe3ee',
            highlightbackground='#759fe6', highlightthickness=3)
        self.framePanelData_1.place(relx=0.05,rely=0.05,relwidth=0.90,relheight=.42)

        self.frameTreeView_1 = Frame(self.root,bd=4,bg='#dfe3ee',
            highlightbackground='#759fe6', highlightthickness=2)
        self.frameTreeView_1.place(relx=0.05,rely=0.5,relwidth=0.90,relheight=.50)

        self.createWidgets()
        self.treeView_table = ttk.Treeview(self.frameTreeView_1, height=1,columns=('col1','col2','col3','col4','col5','col6','col7','col8','col9'))
        self.createTreeViewDataVehicles()
        
    #widgets tab veiculos
    def widgetsTabVehiclesData(self):
        
        self.btn_search_car = tk.Button(self.tab_car_data, text="Pesquisar",command=self.searchVehicle).grid(row=0, column=0, pady=5)
        self.btn_add_car = tk.Button(self.tab_car_data, text="Adicionar Veículo",command=self.addVehiclesDB).grid(row=1, column=0, pady=5)
        self.btn_delete_car = tk.Button(self.tab_car_data, text="Remover Veículo",command=self.deleteVehicleDB).grid(row=2, column=0, pady=5)
        self.btn_update_car = tk.Button(self.tab_car_data, text="Editar Veículo",command=self.updateVehicleDB).grid(row=3, column=0, pady=5)
        self.btn_delete_formEntry = tk.Button(self.tab_car_data, text="Apagar campos de pesquisa",command=self.cleanFormCarEntry).grid(row=4, column=0,pady=1)

        #Entry and labels
        tk.Label(self.tab_car_data, text="Código do Veículo:").grid(row=0, column=4,sticky="W")
        self.entry_cod = tk.Entry(self.tab_car_data)
        self.entry_cod.grid(row=0, column=5)
        
        tk.Label(self.tab_car_data, text="Marca:").grid(row=1, column=4,sticky="W")
        self.entry_marca = tk.Entry(self.tab_car_data)
        self.entry_marca.grid(row=1, column=5)

        tk.Label(self.tab_car_data, text="Modelo:").grid(row=2, column=4,sticky="W")
        self.entry_modelo = tk.Entry(self.tab_car_data)
        self.entry_modelo.grid(row=2, column=5)

        tk.Label(self.tab_car_data, text="Placa:").grid(row=3, column=4,sticky="W")
        self.entry_placa = tk.Entry(self.tab_car_data)
        self.entry_placa.grid(row=3, column=5)

        tk.Label(self.tab_car_data, text="Quilometragem:").grid(row=4, column=4,sticky="W")
        self.entry_quilometragem = tk.Entry(self.tab_car_data)
        self.entry_quilometragem.grid(row=4, column=5)

        tk.Label(self.tab_car_data, text="Ano:").grid(row=5, column=4,sticky="W")
        self.entry_ano = tk.Entry(self.tab_car_data)
        self.entry_ano.grid(row=5, column=5)

        tk.Label(self.tab_car_data, text="Combustível:").grid(row=6, column=4,sticky="W")
        self.entry_combustivel = tk.Entry(self.tab_car_data)
        self.entry_combustivel.grid(row=6, column=5)
    
    #Creation of buttons
    def widgetsTabDriverData(self):
        
        self.btn_search_driver = tk.Button(self.tab_driver_data, text="Pesquisar",command=self.searchDriver).grid(row=0, column=0, pady=5)
        self.btn_add_driver = tk.Button(self.tab_driver_data, text="Adicionar Motorista",command=self.addDriverDB).grid(row=1, column=0, pady=5)
        self.btn_delete_driver = tk.Button(self.tab_driver_data, text="Remover Motorista",command=self.deleteDriverDB).grid(row=2, column=0, pady=5)
        self.btn_update_driver = tk.Button(self.tab_driver_data, text="Editar Dados do Motorista",command=self.updateDriverDB).grid(row=3, column=0, pady=5)
        self.btn_delete_formEntry = tk.Button(self.tab_driver_data, text="Apagar campos de pesquisa",command=self.cleanFormCarEntry).grid(row=4, column=0,pady=1)

        #Entry and labels
        tk.Label(self.tab_driver_data, text="Código do Motorista:").grid(row=0, column=4,sticky="W")
        self.entry_cod_driver = tk.Entry(self.tab_driver_data)
        self.entry_cod_driver.grid(row=0, column=5)
        self.entry_cod_driver.bind()
        
        tk.Label(self.tab_driver_data, text="Nome:").grid(row=1, column=4,sticky="W")
        self.entry_name_driver = tk.Entry(self.tab_driver_data)
        self.entry_name_driver.grid(row=1, column=5)

        tk.Label(self.tab_driver_data, text="CPF:").grid(row=2, column=4,sticky="W")
        self.entry_cpf_driver = tk.Entry(self.tab_driver_data)
        self.entry_cpf_driver.grid(row=2, column=5)

        tk.Label(self.tab_driver_data, text="CNH:").grid(row=3, column=4,sticky="W")
        self.entry_cnh_driver = tk.Entry(self.tab_driver_data)
        self.entry_cnh_driver.grid(row=3, column=5)

        tk.Label(self.tab_driver_data, text="Email:").grid(row=4, column=4,sticky="W")
        self.entry_email_driver = tk.Entry(self.tab_driver_data)
        self.entry_email_driver.grid(row=4, column=5)

        tk.Label(self.tab_driver_data, text="Telefone").grid(row=5, column=4,sticky="W")
        self.entry_phone_driver = tk.Entry(self.tab_driver_data)
        self.entry_phone_driver.grid(row=5, column=5)
        
        self.label_attachment = tk.Label(self.tab_driver_data, text="Anexar CNH:").grid(row=6, column=4,columnspan=2,sticky="W")
        self.attachment_icon = PhotoImage(file='images\\icon_attachment.png')
        tk.Button(self.tab_driver_data, image=self.attachment_icon,command=self.saveAttachment).grid(row=6, column=4,sticky="E")
        self.label_attachment = tk.Label(self.tab_driver_data, text="", wraplength=250, anchor="w", justify="left")
        self.label_attachment.grid(row=6, column=5,columnspan=3,sticky="W")



        #self.attachment_icon = PhotoImage(file='images\\icon_attachment.png').subsample(10,10)

    #Call the functions to create widgets individually
    def createWidgets(self):
        self.tabs_notebook =ttk.Notebook(self.framePanelData_1)
        self.tab_car_data = Frame(self.tabs_notebook,background='lightgray')
        self.tab_driver_data = Frame(self.tabs_notebook,background='lightgray')
        self.tab_notification_data = Frame(self.tabs_notebook,background='lightgray')

        self.tabs_notebook.add(self.tab_car_data,text='Veículos')
        self.tabs_notebook.add(self.tab_driver_data,text='Motoristas')
        self.tabs_notebook.add(self.tab_notification_data,text='Notificações')
        self.tabs_notebook.place(relx=0,rely=0,relwidth=.98,relheight=.98)

        self.tabs_notebook.bind('<<NotebookTabChanged>>', self.onTabChange)

        self.widgetsTabVehiclesData()
        self.widgetsTabDriverData()

    #Creation of treeview
    def createTreeViewDataVehicles(self):
             
        self.treeView_table.heading('#0', text='')
        self.treeView_table.heading('#1', text='cod')
        self.treeView_table.heading('#2', text='Marca')
        self.treeView_table.heading('#3', text='Modelo')
        self.treeView_table.heading('#4', text='Placa')
        self.treeView_table.heading('#5', text='Quilometragem')
        self.treeView_table.heading('#6', text='Ano')
        self.treeView_table.heading('#7', text='Combustível')
        self.treeView_table.heading('#8', text='Data Prox Revisão')
        self.treeView_table.heading('#9', text='Data Ult Revisão')

        self.treeView_table.column('#0',width=10,stretch=NO)
        self.treeView_table.column('#1',width=15,anchor=CENTER,stretch=NO)
        self.treeView_table.column('#2',width=150,anchor=CENTER,stretch=NO)
        self.treeView_table.column('#3',width=150,anchor=CENTER,stretch=NO)
        self.treeView_table.column('#4',width=150,anchor=CENTER,stretch=NO)
        self.treeView_table.column('#5',width=150,anchor=CENTER,stretch=NO)
        self.treeView_table.column('#6',width=150,anchor=CENTER,stretch=NO)
        self.treeView_table.column('#7',width=150,anchor=CENTER,stretch=NO)
        self.treeView_table.column('#8',width=150,anchor=CENTER,stretch=NO)
        self.treeView_table.column('#9',width=150,anchor=CENTER,stretch=NO)
        self.treeView_table.place(relx=0.01,rely=.01,relwidth=.97,relheight=.95)
        self.treeView_table.bind("<Double-1>",self.onDoubleClickVehicleTreeView)
        
        #ScrollBar Vertical and Horizontal
        scrollbarVerticalTreeView = Scrollbar(self.frameTreeView_1,orient='vertical',)
        self.treeView_table.config(yscroll=scrollbarVerticalTreeView.set)
        scrollbarVerticalTreeView.place(relx=0.98,rely=.01,relwidth=.023,relheight=.95)
                
        scrollbarHorizontalTreeView = Scrollbar(self.frameTreeView_1,orient='horizontal',)
        self.treeView_table.config(xscroll=scrollbarHorizontalTreeView.set)
        scrollbarHorizontalTreeView.place(relx=0.01,rely=.96,relwidth=.97,relheight=.040)
           
    #Creation of treeview
    def createTreeViewDataDrivers(self):
        self.treeView_table.heading('#0', text='')
        self.treeView_table.heading('#1', text='cod')
        self.treeView_table.heading('#2', text='Nome')
        self.treeView_table.heading('#3', text='CPF')
        self.treeView_table.heading('#4', text='CNH')
        self.treeView_table.heading('#5', text='Email')
        self.treeView_table.heading('#6', text='Telefone')
        self.treeView_table.heading('#7', text='CNH')

        self.treeView_table.column('#0',width=10)
        self.treeView_table.column('#1',width=15,anchor=CENTER)
        self.treeView_table.column('#2',width=150,anchor=CENTER)
        self.treeView_table.column('#3',width=150,anchor=CENTER)
        self.treeView_table.column('#4',width=150,anchor=CENTER)
        self.treeView_table.column('#5',width=150,anchor=CENTER)
        self.treeView_table.column('#6',width=150,anchor=CENTER)
        self.treeView_table.column('#7',width=150,anchor=CENTER)
        self.treeView_table.bind("<Double-1>",self.onDoubleClickDriverTreeView)
        


    #Create menus
    def menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        def quit(): self.root.destroy()
        def dev_info():messagebox.showinfo("Desenvolvedor",'Dev:kelvin651b@gmail.com\nlinkedin:kelvin-moreira-dos-santos-30614a48')

        menu_Option1 = Menu(menubar)
        menu_Option2 = Menu(menubar)
        menubar.add_cascade(label="Opções",menu=menu_Option1)
        menubar.add_cascade(label="Sobre",menu=menu_Option2)

        menu_Option1.add_command(label='Sair',command=quit)
        menu_Option2.add_command(label='Desenvolvedor',command=dev_info)
        





Application()
