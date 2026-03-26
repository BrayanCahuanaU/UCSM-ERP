#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import json
import time
import random
import re
import datetime
from CBase import *
from CSql import *

class CTesis():

   def __init__(self):
       self.paData  = []
       self.paDatos = []
       self.laData  = []
       self.laDatos = []
       self.loSql   = CSql()

   def mxValParamCodigoUsuario(self):
       if not 'CCODUSU' in self.paData or not re.match('^[0-9A-Z\-]{4}$', self.paData['CCODUSU']):
          self.pcError = 'CÓDIGO DE USUARIO NO DEFINIDO O INVÁLIDO'
          return False
       return True   

   def mxValParamDNI(self):
       if not 'CNRODNI' in self.paData or not re.match('^[0-9A-Z\-]{8}$', self.paData['CNRODNI']):
          self.pcError = 'DOCUMENTO DE IDENTIDAD NO DEFINIDO O INVÁLIDO'
          return False
       return True   

   def mxValParamCodigoEstudiante(self):
       if not 'CCODEST' in self.paData or not re.match('^[0-9A-Z\-]{6}$', self.paData['CCODEST']):
          self.pcError = 'CÓDIGO DE ESTUDIANTE NO DEFINIDO O INVÁLIDO'
          return False
       return True

   def mxValParamUnidadAcademica(self):
       if not 'CUNIACA' in self.paData or not re.match('^[0-9A-Z\-]{4}$', self.paData['CUNIACA']):
          self.pcError = 'UNIDAD ACADÉMICA NO DEFINIDA O INVÁLIDA'
          return False
       return True

   def mxValParamIdTesis(self):
       if not 'CIDTESI' in self.paData or not re.match('^[0-9A-Z\-]{4}$', self.paData['CIDTESI']):
          self.pcError = 'ID TESIS NO DEFINIDO O INVÁLIDO'
          return False
       return True

   def mxVerPermisos(self):
       return True

   # -------------------------------------------------------------------------
   # Inicio de registro de BDT
   # 2026-03-23 FPM Creacion
   # -------------------------------------------------------------------------
   def omInitTesis(self):
       llOk = self.mxValParamCodigoEstudiante()
       if not llOk:
          return False
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False
       llOk = self.mxInitTesis()
       if not llOk:
          self.loSql.omDisconnect()
          return False
       llOk = self.mxCargarLineas()
       self.loSql.omDisconnect()
       return llOk

   def mxInitTesis(self):
       # Carga unidad academica + fecha de egreso
       lcSql = f"""SELECT A.cUniAca, B.cNomUni, A.dEgreso FROM A01MEST A 
                   INNER JOIN A01MUAC B ON B.cUniAca = A.cUniAca
                   WHERE A.cCodEst = '{self.paData['CCODEST']}'"""
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       if not laTmp or len(laTmp)== 0:
          self.pcError = f"CÓDIGO DE ESTUDIANTE [{self.paData['CCODEST']}] NO EXISTE"
          return False
       elif laTmp[2] == None:
          self.pcError = f"CÓDIGO DE ESTUDIANTE [{self.paData['CCODEST']}] NO TIENE FECHA DE EGRESO"
          return False
       self.laData = {'CUNIACA': laTmp[0], 'CNOMUNI': laTmp[1], 'DATOS': None}
       # Verifica tesis
       lcSql = f"SELECT cEstado FROM A03DEST WHERE cCodEst = '{self.paData['CCODEST']}'"
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       if not laTmp or len(laTmp)== 0:
          pass
       elif laTmp[0] == 'X':
          pass 
       else:      
          self.pcError = f"ESTUDIANTE [{self.paData['CCODEST']}] TIENE TESIS PENDIENTE"
          return False
       return True

   def mxCargarLineas(self):
       # Carga lineas de tesis
       laDatos = []
       lcSql = f"SELECT cLinea, cDescri FROM A02MLIN WHERE cUniAca = '{self.laData['CUNIACA']}' AND cEstado = 'A' ORDER BY cLinea"
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       while laTmp != None:
          laDatos.append({'CLINEA': laTmp[0], 'CDESCRI': laTmp[1]})
          laTmp = self.loSql.fetch(RS)
       if len(laDatos)== 0:
          self.pcError = f"NO HAY LÍNEAS DE INVESTIGACIÓN DE TESIS DEFINIDAS PARA UNIDAD ACADÉMICA [{self.laData['CUNIACA']}]"
          return False
       self.laData['DATOS'] = laDatos
       self.paData = self.laData 
       return True

   # -------------------------------------------------------------------------
   # Buscar egresado 
   # 2026-03-23 FPM Creacion
   # -------------------------------------------------------------------------
   def omBuscarEgresadoTesis(self):
       llOk = self.mxValParamBuscarEgresadoTesis()
       if not llOk:
          return False
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False
       llOk = self.mxBuscarEgresadoTesis()
       self.loSql.omDisconnect()
       return llOk

   def mxValParamBuscarEgresadoTesis(self):
       if not self.mxValParamDNI():
          return False
       elif not self.mxValParamUnidadAcademica():
          return False
       return True   

   def mxBuscarEgresadoTesis(self):
       # Busca egresado 
       lcSql = f"""SELECT A.cCodEst, B.cName, A.dEgreso FROM A01MEST A
                   INNER JOIN S01MPER B ON B.cNroDni = A.cNroDni 
                   WHERE A.cNroDni = '{self.paData['CNRODNI']}' AND A.cUniAca = '{self.paData['CUNIACA']}'"""
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       if not laTmp or len(laTmp)== 0:
          self.pcError = f"DOCUMENTO [{self.paData['CNRODNI']}] NO TIENE CÓDIGO ASIGNADO A ACADÉMICA DEFINIDA"
          return False
       elif laTmp[2] == None:
          self.pcError = f"CÓDIGO [{laTmp[0]}] NO TIENE FECHA DE EGRESO"
          return False
       laData = {'CNRODNI': self.paData['CNRODNI'], 'CCODEST': laTmp[0], 'CNOMBRE': laTmp[1]}
       # Verifica tesis
       lcSql = f"SELECT cEstado FROM A03DEST WHERE cCodEst = '{laData['CCODEST']}'"
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       if not laTmp or len(laTmp)== 0:
          pass
       elif laTmp[0] == 'X':
          pass 
       else:      
          self.pcError = f"ESTUDIANTE [{laData['CCODEST']}] TIENE TESIS PENDIENTE"
          return False
       self.paData = laData   
       return True

   # -------------------------------------------------------------------------
   # Grabar PDT
   # 2026-03-23 FPM Creacion
   # -------------------------------------------------------------------------
   def omGrabarPlanTesis(self):
       llOk = self.mxValParamGrabarPlanTesis()
       if not llOk:
          return False
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False
       llOk = self.mxVerDatos()
       if not llOk:
          self.loSql.omDisconnect()
          return False
       llOk = self.mxGrabarPlanTesis()
       if llOk:
          self.loSql.omCommit()
       self.loSql.omDisconnect()
       return llOk

   def mxValParamGrabarPlanTesis(self):
       if not 'CLINEA' in self.paData or not re.match('^[0-9A-Z\-]{4}$', self.paData['CLINEA']):
          self.pcError = 'LÍNEA DE INVESTIGACIÓN DE TESIS NO DEFINIDA O INVÁLIDA'
          return False
       elif not 'CUNIACA' in self.paData or not re.match('^[0-9A-Z\-]{4}$', self.paData['CUNIACA']):
          self.pcError = 'UNIDAD ACADÉMICA NO DEFINIDA O INVÁLIDA'
          return False
       elif not 'MTITULO' in self.paData: # or not re.match('^[0-9A-Z\-]{4}$', self.paData['MTITULO']):
          self.pcError = 'TÍTULO DE TESIS NO DEFINIDO O INVALIDO'
          return False
       i = 0
       for lcCodEst in self.paData['ACODEST']:
           i += 1
           if not re.match('^[0-9A-Z\-]{6}$', lcCodEst):
              self.pcError = f"CÓDIGO [{lcCodEst}] INVÁLIDO"
              return False
       if i == 0:
          self.pcError = f"NO HAY DATOS DE EGRESADOS"
          return False
       return True

   def mxVerDatos(self):
       laData = self.paData
       for lcCodEst in self.paData['ACODEST']:
           self.paData['CCODEST'] = lcCodEst
           llOk = self.mxInitTesis()
           if not llOk:
              return False
           elif self.paData['CUNIACA'] != laData['CUNIACA']:
              self.pcError = f"UNIDAD ACADÉMICA NO CORRESPONDE PARA CÓDIGO [{lcCodEst}]"
              return False
       self.paData = laData
       # Valida unidad academica
       lcSql = f"SELECT cUniAca, cEstado FROM A02MLIN WHERE cLinea = '{self.paData['CLINEA']}'"
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       if not laTmp or len(laTmp)== 0:
          self.pcError = f"LÍNEA DE INVESTIGACIÓN [{self.paData['CLINEA']}] NO EXISTE"
          return False
       elif laTmp[1] != 'A':
          self.pcError = f"LÍNEA DE INVESTIGACIÓN NO ESTÁ ACTIVA"
          return False
       elif laTmp[0] != self.paData['CUNIACA']:
          self.pcError = f"UNIDAD ACADÉMICA DE LÍNEA DE INVESTIGACIÓN NO CORRESPONDE"
          return False
       return True

   def mxGrabarPlanTesis(self):
       # Graba tesis
       lcSql = f"SELECT MAX(cIdTesi)FROM A03MTES"
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       if not laTmp or len(laTmp)== 0 or laTmp[0] == None:
          lcIdTesi = '0000'
       else:
          lcIdTesi = laTmp[0]
       lcIdTesi = fxCorrelativo(lcIdTesi)
       lmBitaco = fxBitacora([], {'CESTADO': 'A', 'CCODUSU': 'ZZZZ', 'TMODIFI': None})
       lcSql = f"""INSERT INTO A03MTES (cIdTesi, cLinea, mTitulo, mBitaco)VALUES ('{lcIdTesi}', '{self.paData['CLINEA']}',
                   '{self.paData['MTITULO']}', '{lmBitaco}')"""
       llOk = self.loSql.omExec(lcSql)
       if not llOk:
          self.pcError = 'NO SE PUDO INSERTAR PLAN DE TESIS'
          return False
       for lcCodEst in self.paData['ACODEST']:
           lcSql = f"INSERT INTO A03DEST (cIdTesi, cCodEst, mBitaco)VALUES ('{lcIdTesi}', '{lcCodEst}', '{lmBitaco}')"
           llOk = self.loSql.omExec(lcSql)
           if not llOk:
              self.pcError = 'NO SE PUDO INSERTAR EGRESADO [{lcCodEst}]'
              return False
       self.paData = {'OK': 'OK'}       
       return True

   # -------------------------------------------------------------------------
   # Init asignar dictaminadores PDT
   # 2026-03-23 FPM Creacion
   # -------------------------------------------------------------------------
   def omInitAsignarDictaminadoresPDT(self):
       llOk = self.mxValParamInitAsignarDictaminadoresPDT()
       if not llOk:
          return False
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False
       llOk = self.mxCargarUnidadAcademica()
       if not llOk:
          self.loSql.omDisconnect()
          return False
       llOk = self.mxInitAsignarDictaminadoresPDT()
       if llOk:
          self.loSql.omCommit()
       self.loSql.omDisconnect()
       return llOk

   def mxValParamInitAsignarDictaminadoresPDT(self):
       if not self.mxValParamCodigoUsuario():
          return False
       return True

   def mxCargarUnidadAcademica(self):
       self.laData = {'CUNIACA': '0049', 'CNOMUNI': None, 'DATOS': None}   # OJOFPM
       lcSql = f"SELECT cNomUni FROM A01MUAC WHERE cUniAca = '{self.laData['CUNIACA']}'"
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       if not laTmp or len(laTmp)== 0:
          self.pcError = f"UNIDAD ACADEMICA [{self.laData['CUNIACA']}] NO ESTÁ DEFINIDA"
          return False
       self.laData['CNOMUNI'] = laTmp[0]
       return True   

   def mxInitAsignarDictaminadoresPDT(self):
       laDatos = []
       lcSql = f"""SELECT A.cIdTesi, TO_CHAR(A.tPresen, 'YYYY-MM-DD HH24:MI'), A.mTitulo, A.cLinea, B.cDescri FROM A03MTES A
                   INNER JOIN A02MLIN B ON B.cLinea = A.cLinea 
                   WHERE A.cEstado = 'A' AND B.cUniAca = '{self.laData['CUNIACA']}'
                   ORDER BY A.tPresen"""
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       while laTmp != None:
          laData = {'CIDTESI': laTmp[0], 'TPRESEN': laTmp[1], 'MTITULO': laTmp[2], 'CLINEA': laTmp[3], 'CDESLIN': laTmp[4], 'CNOMEST': None, 'NFLAG': 0}
          llFirst = True
          i = 0
          lcSql = f"""SELECT C.cName FROM A03DEST A 
                      INNER JOIN A01MEST B ON B.cCodEst = A.cCodEst
                      INNER JOIN S01MPER C ON C.cNroDni = B.cNroDni
                      WHERE A.cIdTesi = '{laTmp[0]}' ORDER BY C.cName"""
          R1 = self.loSql.omExecRS(lcSql)
          laTmp1 = self.loSql.fetch(R1)
          while laTmp1 != None:
             i += 1
             if llFirst:
                llFirst = False
                laData['CNOMEST'] = laTmp1[0]
             laTmp1 = self.loSql.fetch(R1)
          if i == 0:
             self.pcError = f"ID DE TESIS [{laTmp[0]}] NO TIENE EGRESADOS ASIGNADOS"
             return False
          laData['NFLAG'] = i   
          laDatos.append(laData)
          laTmp = self.loSql.fetch(RS)
       if len(laDatos)== 0:
          self.pcError = f"NO HAY PLANES DE TESIS PENDIENTES"
          return False
       self.laData['DATOS'] = laDatos
       self.paData = self.laData
       return True

   # -------------------------------------------------------------------------
   # Cargar dictaminadores de PDT
   # 2026-03-22 FPM Creacion
   # -------------------------------------------------------------------------
   def omCargarDictaminadoresPDT(self):
       llOk = self.mxValParamCargarDictaminadoresPDT()
       if not llOk:
          return False
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False
       llOk = self.mxVerDictaminadoresPDT()
       if not llOk:
          self.loSql.omDisconnect()
          return False
       llOk = self.mxCargarDictaminadoresPDT()
       self.loSql.omDisconnect()
       return llOk

   def mxValParamCargarDictaminadoresPDT(self):
       if not self.mxValParamIdTesis():
          return False
       return True

   def mxVerDictaminadoresPDT(self):
       lcSql = f"SELECT cEstado, mBitaco FROM A03MTES WHERE cIdTesi = '{self.paData['CIDTESI']}'"
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       if not laTmp or len(laTmp)== 0:
          self.pcError = f"ID TESIS NO EXISTE"
          return False
       elif laTmp[0] != 'A':
          self.pcError = f"ESTADO DE TESIS NO PERMITE ASIGNAR DICTAMINADORES DE PLAN DE TESIS"
          return False
       self.laData = {'MBITACO': laTmp[1]}
       lcSql = f"SELECT cCodDoc FROM A03DDOC WHERE cIdTesi = '{self.paData['CIDTESI']}' AND cTipo = 'P' AND cEstado = 'A'"
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       if not (not laTmp or len(laTmp)== 0):
          self.pcError = f"TESIS YA TIENE DEFINIDOS DICTAMINADORES DE PLAN DE TESIS"
          return False
       return True

   def mxCargarDictaminadoresPDT(self):
       # Carga docentes
       laCodDoc = []
       laDatos = []
       lcSql = f"SELECT cCodDoc, cNombre FROM F_A02DDOC_1('{self.paData['CIDTESI']}')"
       #print(lcSql)           
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       while laTmp != None:
          laCodDoc.append({'CCODDOC': laTmp[0], 'CNOMBRE': laTmp[1]})
          laTmp = self.loSql.fetch(RS)
       if len(laCodDoc)< 2:
          self.pcError = "NO HAY DOCENTES SUFICIENTES PARA NOMBRAR DICTAMINADORES DE PLAN DE TESIS"
          return False
       elif len(laCodDoc)== 2:
          for laTmp in laCodDoc:
              laDatos.append({'CCODDOC': laTmp['CCODDOC'], 'CNOMBRE': laTmp['CNOMBRE']})
       else:
          llFlag = False
          i = 0
          while True:
             for laTmp in laCodDoc:
                 if random.random()<= 0.8:
                    if not laTmp['CCODDOC'] in laCodDoc:
                       laDatos.append({'CCODDOC': laTmp['CCODDOC'], 'CNOMBRE': laTmp['CNOMBRE']})
                       i += 1
                       if i == 2:
                          llFlag = True
                          break
             if llFlag:
                break             
       laDatos = sorted(laDatos, key=lambda k: (k["CNOMBRE"]))
       self.paDatos = laDatos
       return True
       
   # -------------------------------------------------------------------------
   # Grabar dictaminadores de PDT
   # 2026-03-22 FPM Creacion
   # -------------------------------------------------------------------------
   def omGrabarDictaminadoresPDT(self):
       llOk = self.mxValParamGrabarDictaminadoresPDT()
       if not llOk:
          return False
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False
       llOk = self.mxVerDictaminadoresPDT()
       if not llOk:
          self.loSql.omDisconnect()
          return False
       llOk = self.mxGrabarDictaminadoresPDT()
       if llOk:
          self.loSql.omCommit()
       self.loSql.omDisconnect()
       return llOk

   def mxValParamGrabarDictaminadoresPDT(self):
       if not self.mxValParamCodigoUsuario():
          return False
       elif not self.mxValParamIdTesis():
          return False
       # OJOFPM FALTA VALIDAR DATOS DE DOCENTES    
       return True

   def mxGrabarDictaminadoresPDT(self):
       lmBitaco = fxBitacora([], {'CCODUSU': self.paData['CCODUSU'], 'CESTADO': 'A', 'TMODIFI': None})
       for laTmp in self.paData['DATOS']:
           lcSql = f"INSERT INTO A03DDOC (cIdTesi, cTipo, cCodDoc, mBitaco)VALUES ('{self.paData['CIDTESI']}', 'P', '{laTmp['CCODDOC']}', '{lmBitaco}')"
           llOk = self.loSql.omExec(lcSql)
           if not llOk:
              self.pcError = "NO SE PUDO INSERTAR DOCENTES DICTAMINADORES DE PLAN DE TESIS"
              return False
       print('0)', self.laData['MBITACO'])      
       lmBitaco = fxBitacora(self.laData['MBITACO'], {'CCODUSU': self.paData['CCODUSU'], 'CESTADO': 'B', 'TMODIFI': None})
       lcSql = f"UPDATE A03MTES SET cEstado = 'B', mBitaco = '{lmBitaco}' WHERE cIdTesi = '{self.paData['CIDTESI']}'"
       llOk = self.loSql.omExec(lcSql)
       if not llOk:
           self.pcError = "NO SE PUDO ACTUALIZAR ESTADO DE TESIS PARA DOCENTES DICTAMINADORES DE PLAN DE TESIS"
           return False
       self.paData = {'OK': 'OK'}    
       return True
      