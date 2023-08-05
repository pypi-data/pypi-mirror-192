
def toBayes(red):
  conexion = []

  for key in red.data:
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
  bayesiana = BayesianNetwork(conexion)
  p = bayesiana.nodes()
  variables = []
  for key in red.data:
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

  print(tent)

  for y in p:
      normal = []
      negado = []
      temp = None
      for x in tent:
          if "!" == x[0]:
            if y == x[1]:
                negado.append(1-red.data[x])
                normal.append(red.data[x])
          if y == x[0]:
              negado.append(red.data[x])
              normal.append(1-red.data[x])
      print(normal)
      print(negado)
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
        bayesiana.add_cpds(TabularCPD(y, 2, [normal, negado], evidence=now, evidence_card=[2,2]))
      elif len(normal) == 2:
        print(y, tent)
        temp =temp.replace('!', '').replace(y+"|","").replace(",","").replace("|"," ")
        now = temp.split(" ")
        print(y)
        bayesiana.add_cpds(TabularCPD(y, 2, [normal, negado], evidence=[now[0]], evidence_card=[2]))
      else:
        bayesiana.add_cpds(TabularCPD(y, 2, [normal, negado]))

  for test in bayesiana.get_cpds():
    print(test)
