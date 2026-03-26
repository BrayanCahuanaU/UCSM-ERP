#import psycopg2
import random
import datetime
import string
import re, json

class CBase:
   def __init__(self):
       self.pcError   = None

class CDate(CBase):
   
   def valDate(self, p_cFecha):
       llOk = True
       try:
          ldFecha = datetime.datetime.strptime(p_cFecha, "%Y-%m-%d")
       except Exception as e: 
          llOk = False
       return llOk
  
   def mxValDate(self, p_cFecha):
       try:
          ldFecha = datetime.datetime.strptime(p_cFecha, "%Y-%m-%d")
       except Exception as e: 
          return None
       return ldFecha
  
   def mxValDateTime(self, p_cFecha):
       try:
          ldFecha = datetime.datetime.strptime(p_cFecha, "%Y-%m-%d %H:%M")
       except Exception as e: 
          return None
       return ldFecha
  
   def add(self, p_cFecha, p_nDias):
       llOk = self.valDate(p_cFecha)
       ldFecha = datetime.datetime.strptime(p_cFecha, "%Y-%m-%d")
       ldFecha = ldFecha + datetime.timedelta(days = p_nDias)
       return ldFecha.strftime('%Y-%m-%d')
      
   def diff(self, p_cFecha1, p_cFecha2):
       llOk = self.valDate(p_cFecha1)
       if not llOk:
          return None
       llOk = self.valDate(p_cFecha2)
       if not llOk:
          return None
       ldFecha1 = self.mxValDate(p_cFecha1)
       ldFecha2 = self.mxValDate(p_cFecha2)
       d = ldFecha1 - ldFecha2
       return d.days

   def dow(self, p_cFecha):
       llOk = self.valDate(p_cFecha)
       if not llOk:
          return None
       ldFecha = self.mxValDate(p_cFecha)
       return ldFecha.weekday()

   def day(self, p_cFecha):
       llOk = self.valDate(p_cFecha)
       if not llOk:
          return None
       ldFecha = self.mxValDate(p_cFecha)
       return int(ldFecha.strftime('%d'))

   def month(self, p_cFecha):
       llOk = self.valDate(p_cFecha)
       if not llOk:
          return None
       ldFecha = self.mxValDate(p_cFecha)
       return int(ldFecha.strftime('%m'))

   def valTime(self, p_cTime):
       if not re.match('^\d{2}\:\d{2}$', p_cTime):
          return False
       elif not (p_cTime[0:2] >= '00' and p_cTime[0:2] <= '23'):
          return False
       elif not (p_cTime[3:5] >= '00' and p_cTime[3:5] <= '59'):
          return False
       return True

def fxCorrelativo(p_cCodigo):
    lcCodigo = p_cCodigo
    i = len(lcCodigo) - 1
    while i >= 0:
       lcDigito = p_cCodigo[i]
       if lcDigito == '9':
          lcDigito = 'A'
       elif lcDigito < '9':
          lcDigito = str(int(lcDigito) + 1)
       elif lcDigito < 'Z':
          lcDigito = chr(ord(lcDigito) + 1)
       elif lcDigito == 'Z':
          lcDigito = '0'
       lcCodigo = lcCodigo[:i] + lcDigito + lcCodigo[i + 1:]
       if lcDigito != '0':
          break
       i -= 1
    return lcCodigo;

def f_DayOfWeek(p_cDow):
    if p_cDow == '1':
       return 'LUNES'
    elif p_cDow == '2':
       return 'MARTES'
    elif p_cDow == '3':
       return 'MIÉRCOLES'
    elif p_cDow == '4':
       return 'JUEVES'
    elif p_cDow == '5':
       return 'VIERNES'
    elif p_cDow == '6':
       return 'SÁBADO'
    elif p_cDow == '7':
       return 'DOMINGO'
    return '* ERR *'     

def fxAddMinute(p_cHora, p_nMinuto):
    #print(p_cHora)
    lnHora = int(p_cHora[0:2])
    #print(lnHora, p_cHora[0:2])
    lnMinuto = int(p_cHora[3:5])
    #print(lnMinuto, p_cHora[3:5])
    lnMinuto += p_nMinuto
    if lnMinuto < 0:
       lnMinuto = 60 + lnMinuto
       lnHora -= 1
    elif lnMinuto >= 60:
       lnMinuto = lnMinuto - 60
       lnHora += 1
    lcHora = '0' + str(lnHora)
    lcHora = lcHora[-2:]
    lcMinuto = '0' + str(lnMinuto)
    lcMinuto = lcMinuto[-2:]
    return lcHora + ':' + lcMinuto

def fxBitacora(p_mBitaco, p_aBitaco):
    p_aBitaco['TMODIFI'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")   
    laBitaco = p_mBitaco
    try:
       laBitaco.append(p_aBitaco)
    except Exception as e:   
       laBitaco = []
       laBitaco.append(p_aBitaco)
    lmBitaco = json.dumps(laBitaco)
    return lmBitaco
