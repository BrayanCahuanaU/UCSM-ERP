import hashlib 
import psycopg2 
from psycopg2 import Error
import json 
 
class CSql(): 
    def __init__(self):
        self.h       = None 
        self.plOk    = True 
        self.pcError = None 
        self.RS      = None
 
    def omConnect(self, p_nDB = None):
        self.plOk = True  
        if p_nDB == 1:  
           lcConnect = "host=localhost dbname=DBERP1 user=postgres password=postgres port=5432" 
        elif p_nDB == 9:  
           lcConnect = "host=localhost dbname=DB_ERP port=5432 user=postgres password=postgres"
        else:  
           lcConnect = "host=localhost dbname=DBERP port=5432 user=postgres password=postgres"
        print(lcConnect)
        try:  
           self.h = psycopg2.connect(lcConnect)   
        except psycopg2.DatabaseError:  
           self.plOk = False  
           self.pcError = 'ERROR AL CONECTAR CON LA BASE DE DATOS'  
        return self.plOk  
 
    def omConnect_old(self, p_nDB = None):
        self.plOk = True  
        if p_nDB == 1:  
           lcConnect = "host=localhost dbname=UCSMListener user=postgres password=postgres port=5432" 
        elif p_nDB == 2:  
           lcConnect = "host=localhost dbname=UCSMINS port=5432 user=postgres password=postgres"
        elif p_nDB == 3:  
           lcConnect = "host=localhost dbname=UCSMASBANC user=postgres password=postgres port=5432" 
        elif p_nDB == 4:  
           lcConnect = "host=localhost dbname=UCSMFactElec_PRUEBA user=postgres password=postgres port=5432"
        elif p_nDB == 5: 
           lcConnect = "host=localhost dbname=UCSMBack_PRUEBA user=postgres password=postgres port=5432"
        elif p_nDB == 6: 
           lcConnect = "host=localhost dbname=UCSM_1103_PRUEBA user=postgres password=postgres port=5432"
        elif p_nDB == 7: 
           lcConnect = "host=localhost dbname=UCSMDEEP port=5432 user=postgres password=postgres"
        else:
           lcConnect = "host=localhost dbname=UCSMERP port=5432 user=postgres password=postgres"
        print(lcConnect)
        try:  
           self.h = psycopg2.connect(lcConnect)   
        except psycopg2.DatabaseError:  
           self.plOk = False  
           self.pcError = 'ERROR AL CONECTAR CON LA BASE DE DATOS'  
        return self.plOk  

    def omExecRS_old(self, p_cSql): 
        #print p_cSql 
        self.plOk = True 
        lcCursor = self.h.cursor() 
        try: 
           lcCursor.execute(p_cSql) 
           RS = lcCursor.fetchall() 
        except psycopg2.DatabaseError as e: 
           self.plOk = False 
           # print e.message 
           self.pcError = 'ERROR AL EJECUTAR COMANDO SELECT' 
           RS = None 
        return RS 
 
    def omExecRS(self, p_cSql): 
        #print p_cSql 
        lcCursor = self.h.cursor() 
        try: 
           lcCursor.execute(p_cSql) 
        except psycopg2.DatabaseError as e: 
           lcCursor = None 
        return lcCursor 
 
    def fetch(self, p_cCursor):
        try:
           RS = p_cCursor.fetchone() 
        except Exception as e:
           print('----------')
           print(e)
        return RS 
 
    def omExec(self, p_cSql): 
        #print p_cSql 
        self.plOk = True 
        lcCursor = self.h.cursor() 
        try: 
           lcCursor.execute(p_cSql) 
        except psycopg2.DatabaseError as e: 
           self.plOk = False 
           print(e.message) 
           self.pcError = 'ERROR AL ACTUALIZAR LA BASE DE DATOS' 
        return self.plOk 
 
    def omDisconnect(self): 
        self.h.close() 
 
    def omCommit(self): 
        self.h.commit() 

