import pandas as pd
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination
import re
from decimal import *

class RB:
    def __init__(self, input):
        self.data = {}
        self.complete = {}
        self.bayesiana = None
      

        self.genRB(input)

        print(self.data)


    def genRB(self, input):
        
        df = pd.read_csv(input, sep = "=", header = None)

        for i in range(len(df[0])):
            self.data[
                self.getEvent(df[0].__getitem__(i))
            ] = df[1].__getitem__(i)

    def getEvent(self, E):
        E_temp = str(E)
        E_temp = E_temp.replace("P(", "")
        E_temp = E_temp.replace(") ", "")

        return E_temp

    def readEvent(self): 
        0

    def P(self, Event):
        # Find if self.data has already the query
        try:
            return self.data[Event]

        except:
            print('No existe')

    def BayesPGM(self):
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
      self.bayesiana = None
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
        print("Red no esta completamente discreta")


    def representacion(self):
      for key in self.complete:
        print(key+": "+str(self.complete[key])+"\n")
  
    def factores(self):
      for test in self.bayesiana.get_cpds():
        print(test)

    def eliminacion(self, variable):
      infer = VariableElimination(self.bayesiana)
      print(infer.query([variable]))
