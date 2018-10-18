""" Nutritional Calendar """

from selenium import webdriver
import mysql.connector
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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
            self.mycursor.execute("CREATE TABLE IF NOT EXISTS Food (id INT AUTO_INCREMENT PRIMARY KEY, Nombre TEXT,Energia FLOAT,Grasas FLOAT,Proteinas FLOAT,Carbohidratos FLOAT)")
            print('La tabla Food ha sido creada')
            try:
                self.mycursor.execute("CREATE VIEW alimentos AS SELECT * from Food")
                print('Vista creada')   
            except:
                print('La vista ya existia')
    
    def clear_table(self):
        self.mycursor.execute('DELETE from Food')
        self.mydb.commit()
        print("Tabla vaciada")
        
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
    
    def wait_get_single(self,element):
        return WebDriverWait(self.browser,10).until(EC.presence_of_element_located(element))
        
    def wait_get_all(self,elements):
        return WebDriverWait(self.browser,10).until(EC.presence_of_all_elements_located(elements))
        
    def open_page(self):
        driverpath = "C:/Users/Poncho/Desktop/chromedriver" 
        self.browser = webdriver.Chrome(driverpath)
        url = 'http://www.bedca.net/bdpub/index.php'
        self.browser.get(url)
        consulta = self.wait_get_single((By.LINK_TEXT,"Consulta"))
        consulta.click()
        lista = self.wait_get_single((By.LINK_TEXT,"Lista alfabética"))
        lista.click()
        todos = self.wait_get_single((By.LINK_TEXT,"Todos   "))
        todos.click()
        
        
        
    #click on each element and extract data we need for row 
    def get_data_a(self):
        self.open_page()
        self.count = 1
        self.rows_a = self.wait_get_all((By.XPATH,"//table[@id='querytable1']/tbody/tr"))
        
        while self.count<len(self.rows_a):
            self.cell = self.rows_a[self.count].find_elements_by_tag_name("td")
            nombre = self.cell[1].text
            self.cell[0].click()
            self.wait_get_single((By.XPATH,"//div[@id='content2']//table[3]"))
            self.rowa = self.wait_get_all((By.CSS_SELECTOR,"tr.row-a"))
            self.rowb = self.wait_get_all((By.CSS_SELECTOR,"tr.row-b"))
            print(nombre)
            energia=self.rowb.text.split()
            print(energia)
            energia=energia[3].replace("(",'')
            try:
                energia = float(energia.replace(")",''))
            except:
                energia=0
            grasa = self.rowa[1].text.split()
            try:
                grasa = float(grasa[4])
            except:
                grasa = 0
            proteina=self.rowb[1].text.split()
            try:
                proteina = float(proteina[2])
            except:
                proteina=0
            ch=self.rowa[3].text.split()
            try:
                ch = float(ch[1])
            except:
                ch = 0
            datos = (nombre,energia,grasa,proteina,ch)
            super(Scrapping, self).__insert__(datos)
            anterior = self.browser.find_element_by_link_text('Listado anterior')
            anterior.click()
            self.count +=1
            self.rows_a = self.wait_get_all((By.XPATH,"//table[@id='querytable1']/tbody/tr"))
        self.browser.close()             
    
        
    