'''
Las opciones para observar y grabar el PDT
Para la asignación de asesor: el init, la búsqueda del asesor y la grabación del asesor
Falta terminar y probar el código
'''



   # -------------------------------------------------------------------------
   # Observar PDT
   # 2026-03-22 FPM Creacion
   # -------------------------------------------------------------------------
   def omObservarPDT(self):
       llOk = self.mxValParamObservarPDT()
       if not llOk:
          return False
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False
       llOk = self.mxVerificarPDT()
       if not llOk:
          self.loSql.omDisconnect()
          return False
       llOk = self.mxObservarPDT()
       if llOk:
          self.loSql.omCommit()
       self.loSql.omDisconnect()
       return llOk

   def mxValParamObservarPDT(self):
       if not self.mxValParamCodigoUsuario():
          return False
       elif not self.mxValParamIdTesis():
          return False
       # FALTA VALIDAR LA OBSERVACION MOBSERV
       return True

   def mxVerificarPDT(self):
       # Verifica que A03MTES.cEstado = 'B' y que el self.paData['CCODUSU'] este en el A03DDOC para el cIdTesi, aprovechar para cargar las observaciones anteriores
       # en self.laData['MOBSERV']
       # TODO
       return True

   def mxInitRevisarPDT(self):
       # Juntar las observaciones con el codigo de usuarioo y la observacion nueva
       # TODO
       # Grabar la observacion en A03DDOC
       # TODO
       return True

   # -------------------------------------------------------------------------
   # Aprobar PDT
   # 2026-03-22 FPM Creacion
   # -------------------------------------------------------------------------
   def omAprobarPDT(self):
       llOk = self.mxValParamAprobarPDT()
       if not llOk:
          return False
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False
       llOk = self.mxVerificarPDT()
       if not llOk:
          self.loSql.omDisconnect()
          return False
       llOk = self.mxAprobarPDT()
       if llOk:
          self.loSql.omCommit()
       self.loSql.omDisconnect()
       return llOk

   def mxValParamAprobarPDT(self):
       if not self.mxValParamCodigoUsuario():
          return False
       elif not self.mxValParamIdTesis():
          return False
       # FALTA VALIDAR LA OBSERVACION MOBSERV
       return True

   def mxAprobarPDT(self):
       # Actualizar la aprobacion en A03DDOC
       # TODO
       # Verificar si el otro docente aprobo, si es asi actualzar el A03MTES.cEstado = 'C'
       return True

   # -------------------------------------------------------------------------
   # Init asignar asesor de BDT
   # 2026-03-25 FPM Creacion
   # -------------------------------------------------------------------------
   def omInitAsignarAsesorBDT(self):
       llOk = self.mxValParamInitAsignarAsesorBDT()
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
       llOk = self.mxInitAsignarAsesorBDT()
       self.loSql.omDisconnect()
       return llOk

   def mxValParamInitAsignarDictaminadoresPDT(self):
       if not self.mxValParamCodigoUsuario():
          return False
       return True

   def mxInitAsignarAsesorBDT(self):
       laDatos = []
       lcSql = f"""SELECT A.cIdTesi, TO_CHAR(A.tPresen, 'YYYY-MM-DD HH24:MI'), A.mTitulo, A.cLinea, B.cDescri FROM A03MTES A
                   INNER JOIN A02MLIN B ON B.cLinea = A.cLinea 
                   WHERE A.cEstado = 'C' AND B.cUniAca = '{self.laData['CUNIACA']}'
                   ORDER BY A.tPresen"""   # OJOFPM el orden hay que corregir
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
          self.pcError = f"NO HAY PLANES DE TESIS APROBADOS PENDIENTES"
          return False
       self.laData['DATOS'] = laDatos
       self.paData = self.laData
       return True

   # -------------------------------------------------------------------------
   # Buscar docente para asesor 
   # 2026-03-25 FPM Creacion
   # -------------------------------------------------------------------------
   def omBuscarDocente(self):
       llOk = self.mxValParamBuscarDocente()
       if not llOk:
          return False
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False
       llOk = self.mxBuscarDocente()
       self.loSql.omDisconnect()
       return llOk

   def mxValParamBuscarDocente(self):
       if not 'CPARAM' in self.paData or not re.match('^[0-9A-Z ]{5, 20}$', self.paData['CPARAM']):
          self.pcError = 'PARÁMETRO DE BÚSQUEDA NO DEFINIDO O INVÁLIDO'
          return False
       return True   

   def mxBuscarDocente(self):
       laDatos = []
       lcNombre = self.paData['CPARAM'].strip().replace(' ', '%') + '%'
       lcSql = f"""SELECT A.cCodUsu, B.cName FROM S01MUSU A
                   INNER JOIN S01MPER B ON B.cNroDni = A.cNroDni 
                   WHERE B.cName LIKE '{lcNombre}' ORDER BY B.cName"""   # OJOFPM el orden hay que corregir
       RS = self.loSql.omExecRS(lcSql)
       laTmp = self.loSql.fetch(RS)
       while laTmp != None:
          laDatos.append({'CCODDOC': laTmp[0], 'CNOMBRE': laTmp[1]})
          laTmp = self.loSql.fetch(RS)
       if len(laDatos)== 0:
          self.pcError = f"NO HAY DOCENTES QUE CUMPLAN CRITERIO DE BÚSQUEDA"
          return False
       self.paDatos = laDatos
       return True

   # -------------------------------------------------------------------------
   # Grabar asesor de BDT
   # 2026-03-22 FPM Creacion
   # -------------------------------------------------------------------------
   def omGrabarAsesorBDT(self):
       llOk = self.mxValParamGrabarAsesorBDT()
       if not llOk:
          return False
       llOk = self.loSql.omConnect()
       if not llOk:
          self.pcError = self.loSql.pcError
          return False
       llOk = self.mxVerAsesorBDT()
       if not llOk:
          self.loSql.omDisconnect()
          return False
       llOk = self.mxGrabarAsesorBDT()
       if llOk:
          self.loSql.omCommit()
       self.loSql.omDisconnect()
       return llOk

   def mxValParamGrabarAsesorBDT(self):
       if not self.mxValParamCodigoUsuario():
          return False
       elif not self.mxValParamIdTesis():
          return False
       elif not 'CCODDOC' in self.paData or not re.match('^[0-9A-Z\-]{4}$', self.paData['CCODDOC']):
          self.pcError = 'CÓDIGO DE DOCENTE NO DEFINIDO O INVÁLIDO'
          return False
       return True

   def mxGrabarAsesorBDT(self):
       # Falta validar que cCodDoc este en S01MUSU y este vigente, ademas que el A03MTES.cEstado sea C
       # TODO
       lmBitaco = fxBitacora([], {'CCODUSU': self.paData['CCODUSU'], 'CESTADO': 'A', 'TMODIFI': None})
       lcSql = f"INSERT INTO A03DDOC (cIdTesi, cTipo, cCodDoc, mBitaco) VALUES ('{self.paData['CIDTESI']}', 'A', '{laTmp['CCODDOC']}', '{lmBitaco}')"
       llOk = self.loSql.omExec(lcSql)
       if not llOk:
          self.pcError = "NO SE PUDO INSERTAR ASESOR DE BORRADOR DE TESIS"
          return False
       lmBitaco = fxBitacora(self.laData['MBITACO'], {'CCODUSU': self.paData['CCODUSU'], 'CESTADO': 'D', 'TMODIFI': None})
       lcSql = f"UPDATE A03MTES SET cEstado = 'D', mBitaco = '{lmBitaco}' WHERE cIdTesi = '{self.paData['CIDTESI']}'"
       llOk = self.loSql.omExec(lcSql)
       if not llOk:
           self.pcError = "NO SE PUDO ACTUALIZAR ESTADO DE ASESORÍA DE TESIS"
           return False
       self.paData = {'OK': 'OK'}    
       return True

