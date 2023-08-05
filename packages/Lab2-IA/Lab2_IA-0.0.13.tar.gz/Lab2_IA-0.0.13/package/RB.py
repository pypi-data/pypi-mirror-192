import pandas as pd
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
import re
from decimal import *

#Se crea la clase
class RB:
    #Se definen las variables de data y red bayesiana
    def __init__(self, input):
        self.data = {}
        self.complete = {}
        self.bayesiana = None
        self.genRB(input)

        print(self.data)

    #Se genera la red bayesiana y se guarda en data
    def genRB(self, input):
        df = pd.read_csv(input, sep = "=", header = None)
        for i in range(len(df[0])):
            self.data[
                self.getEvent(df[0].__getitem__(i))
            ] = df[1].__getitem__(i)

    #Se toma un evento individual
    def getEvent(self, E):
        E_temp = str(E)
        E_temp = E_temp.replace("P(", "")
        E_temp = E_temp.replace(") ", "")

        return E_temp
    
    #Se lee un evento
    def readEvent(self): 
        pass

    #Encontrar si la data tiene el query que se desea
    def P(self, Event):
        try:
            return self.data[Event]
        except:
            print('No existe')

    #Se realiza la funcion de Bayes
    def BayesPGM(self):
      
        #Se realiza la iteracion en las llaves de cada nodo de data
        conexion = []
        for key in self.data:
            m = ''.join(c for c in key if c.isalpha())
            if len(m) == 1:
                continue
            else:
                for n in m[1:]:
                    temp = (n, m[0])
                    if temp not in conexion:
                        conexion.append(temp)
                    else:
                        continue
                
        self.bayesiana = BayesianNetwork(conexion)
        p = self.bayesiana.nodes()
        variables = []
        for key in self.data:
            new_string = key.replace(" ", "").replace(",", "|")
            splits = new_string.split("|")
            variables.append(splits)
      
        tent = []
        for n in variables:
            for m in p:
                if n[0][0] == "!":
                    if m == n[0][1]:
                        if len(n[0]) == "!":
                            tent.append(m)
                        m = "!" + m
                        if len(n) == 1:
                            tent.append(m)
                            continue
                        m += "|"
                        for q in n[1:]:
                            m += q + ", "
                        if m[:-2] not in tent and m[:-2] != "":
                            tent.append(m[:-2])
                if m == n[0]:
                    if len(n) == 1:
                        tent.append(m)
                    m += "|"
                    for q in n[1:]:
                        m += q + ", "
                    if m[:-2] not in tent and m[:-2] != "":
                        tent.append(m[:-2])
                        
        try:
            for y in p:
                normal = []
                negado = []
                temp = None
                for x in tent:
                    if "!" == x[0]:
                        if y == x[1]:
                            self.complete[x] = self.data[x]
                            self.complete["!"+x] =1-self.data[x]
                            negado.append(1-self.data[x])
                            normal.append(self.data[x])
                    if y == x[0]:
                        self.complete[x] = self.data[x]
                        self.complete["!"+x] =1-self.data[x]
                        negado.append(self.data[x])
                        normal.append(1-self.data[x])
                for x in tent:
                    if "!" == x[0]:
                        if y == x[1]:
                            temp = x
                    if y == x[0]:
                        temp = x
                        break
                if len(normal) == 4:
                    temp =temp.replace('!', '').replace(y+"|","").replace(",","")
                    now = temp.split(" ")
                    self.bayesiana.add_cpds(TabularCPD(y, 2, [normal, negado], evidence=now, evidence_card=[2,2]))
                elif len(normal) == 2:
                    temp =temp.replace('!', '').replace(y+"|","").replace(",","").replace("|"," ")
                    now = temp.split(" ")
                    self.bayesiana.add_cpds(TabularCPD(y, 2, [normal, negado], evidence=[now[0]], evidence_card=[2]))
                else:
                    self.bayesiana.add_cpds(TabularCPD(y, 2, [normal, negado]))
            print("Red esta completamente descrita")
        except:
            print("Red no esta completamente descrita")

    #Funcion para representar el codigo
    def representacion(self):
      for key in self.complete:
        print(key + ": " + str(self.complete[key]) + "\n")
    
    #Funcion para mostrar los factores de la red bayesiana
    def factores(self):
      for test in self.bayesiana.get_cpds():
        print(test)

    #Funcion para eliminacion de variables
    def eliminacion(self, variable):
      infer = VariableElimination(self.bayesiana)
      print(infer.query([variable]))
