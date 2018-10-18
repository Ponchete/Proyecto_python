""" Nutritional Calendar """

from selenium import webdriver
import time
import mysql.connector

class Connection():
    def __init__(self):
        mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Ponchete9289"
                )
    
        self.mycursor = mydb.cursor()
    
        self.mycursor.execute("CREATE DATABASE IF NOT EXISTS Nutrition")
        
    def connect(self):
        self.mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    passwd="Ponchete9289",
                    database="Nutrition"
                    )
        self.mycursor = self.mydb.cursor()
        print("Conectado a la BBDD")
    
    def create_table(self):
            self.mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    passwd="Ponchete9289",
                    database="Nutrition"
                    )
            self.mycursor = self.mydb.cursor()
            self.mycursor.execute(f"CREATE TABLE IF NOT EXISTS Food (id INT AUTO_INCREMENT PRIMARY KEY, Nombre TEXT,Energia FLOAT,Grasas FLOAT,Proteinas FLOAT,Carbohidratos FLOAT)")
            print(f'La tabla Food ha sido creada')
            try:
                self.mycursor.execute(f"CREATE VIEW alimentos AS SELECT * from Food")
                print('Vista creada')   
            except:
                print('La vista ya existia')
    
    def drop_table(self):
        try:
            self.mycursor.execute(f'DROP TABLE IF EXISTS Food')
            print("Tabla eliminada")
        except:
            print('La tabla no existe')
    def __insert__(self,datos):
        self.mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    passwd="Ponchete9289",
                    database="Nutrition"
                    )
        self.mycursor = self.mydb.cursor()
        sql = "INSERT INTO Food (Nombre,Energia,Grasas,Proteinas,Carbohidratos) VALUES (%s,%s,%s,%s,%s)"
        self.mycursor.execute(sql, datos)
        self.mydb.commit()
        self.mycursor.close()

    def close_connection(self):
        self.mydb.close()
        print('Conexion cerrada')




class Scrapping(Connection):
    
    def get_data(self):
        driverpath = "C:/Users/Poncho/Desktop/chromedriver" 
        browser = webdriver.Chrome(driverpath)
        url = 'http://www.bedca.net/bdpub/index.php'
        browser.get(url)
           
        time.sleep(2)
        consulta = browser.find_element_by_link_text('Consulta')
        consulta.click()
        time.sleep(1)
        lista = browser.find_element_by_link_text('Lista alfabética')
        lista.click()
        time.sleep(1)
        todos = browser.find_element_by_link_text('Todos   ')
        todos.click()
        time.sleep(1)
        rows_a = browser.find_elements_by_css_selector("tr.row-a")
        count = 0
        #click on each element and extract data we need for row a
        for row in rows_a:
            cell = rows_a[count].find_elements_by_tag_name("td")
            nombre = cell[1].text
            cell[0].click()
            time.sleep(1)
            rowa = browser.find_elements_by_css_selector("tr.row-a")
            rowb = browser.find_elements_by_css_selector("tr.row-b")
            print(nombre)
            energia=rowb[0].text.split()
            energia=energia[3].replace("(",'')
            try:
                energia = float(energia.replace(")",''))
            except:
                energia=0
            grasa = rowa[1].text.split()
            try:
                grasa = float(grasa[4])
            except:
                grasa = 0
            proteina=rowb[1].text.split()
            try:
                proteina = float(proteina[2])
            except:
                proteina=0
            ch=rowa[3].text.split()
            try:
                ch = float(ch[1])
            except:
                ch = 0
            datos = (nombre,energia,grasa,proteina,ch)
            count +=1
            super(Scrapping, self).__insert__(datos)
            anterior = lista = browser.find_element_by_link_text('Listado anterior')
            anterior.click()
            time.sleep(1)
            rows_a = browser.find_elements_by_css_selector("tr.row-a")
            time.sleep(1)
        
        rows_b = browser.find_elements_by_css_selector("tr.row-b")
        count = 0
        #click on each element and extract data we need for row b
        for row in rows_b:
            cell = rows_b[count].find_elements_by_tag_name("td")
            nombre = cell[1].text
            cell[0].click()
            time.sleep(1)
            rowa = browser.find_elements_by_css_selector("tr.row-a")
            rowb = browser.find_elements_by_css_selector("tr.row-b")
            print(nombre)
            energia=rowb[0].text.split()
            energia=energia[3].replace("(",'')
            try:
                energia = float(energia.replace(")",''))
            except:
                energia=0
            grasa = rowa[1].text.split()
            try:
                grasa = float(grasa[4])
            except:
                grasa = 0
            proteina=rowb[1].text.split()
            try:
                proteina = float(proteina[2])
            except:
                proteina=0
            ch=rowa[3].text.split()
            try:
                ch = float(ch[1])
            except:
                ch = 0
            datos = (nombre,energia,grasa,proteina,ch)
            count +=1
            super(Scrapping, self).__insert__(datos)
            anterior = lista = browser.find_element_by_link_text('Listado anterior')
            anterior.click()
            time.sleep(1)
            rows_b = browser.find_elements_by_css_selector("tr.row-a")
            time.sleep(1)

        super(Scrapping,self).close_connection()
    