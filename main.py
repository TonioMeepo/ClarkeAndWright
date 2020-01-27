import Utils as u
from Cliente import Cliente
import sys
from datetime import datetime as dt
from ClarkeWrightParallel import ClarkeWrightParallel
from ClarkeWrightSequential import ClarkeWrightSequential
import time
import glob
import os
from statistics import mean
import pandas as pd

s_errori = []
s_tempi = []
s_erroreMedio = 0
s_tempoMedio = 0

names = []
dimensioniProb = []

p_errori = []
p_tempi = []
p_erroreMedio = 0
p_tempoMedio = 0

path = "C:/Users/marti/Documents/ClarkeAndWright/Instances/"
filenames = glob.glob(path + '*.txt')

for filename in filenames:

  depot, clientiL, clientiB, savingsL, savingsB, nClienti, k, capacity = u.prepareProblem(filename) # otteniamo i dati dal file

  if("debug" in sys.argv):# se l'utente ha chiesto il debug
    for saving in savingsB:# controlliamo che i savings siano stati ordinati correttamente
      print(str(saving[0][0].name) + " " + str(saving[0][1].name) + " " + str(saving[1]))
    print(dt.now())

  start_time = time.time()
  initialRoutesL = u.getInitialRoutes(depot, clientiL)
  routes_l = ClarkeWrightSequential(depot, clientiL, savingsL, initialRoutesL, k, capacity)


  initialRoutesB = u.getInitialRoutes(depot, clientiB)
  routes_b = ClarkeWrightSequential(depot, clientiB, savingsB, initialRoutesB, k, capacity, forBackhaul=False)
  s_routes = u.merge(routes_l,routes_b)
  stop_time = time.time()
  s_elapsed_time = stop_time-start_time

  if("debug" in sys.argv):
    print()
    print("SEQUENTIAL")
    print("FINAL ROUTES:")
    print("Capacity: " + str(capacity) + "  #vehicles: " + str(k) + "  #Routes: " + str(len(s_routes)))
    for route in s_routes:
      print(str(list(map(lambda x : x.name,route))) + " " + str(u.cost(route)))
    print()
    print("LINEHAUL ROUTES:")
    print("Capacity: " + str(capacity) + "  #vehicles: " + str(k) + "  #Routes: " + str(len(routes_l)))
    for route in routes_l:
      print(str(list(map(lambda x : x.name,route))) + " " + str(u.cost(route)))
    print()
    print("BACKHAUL ROUTES:")
    print("Capacity: " + str(capacity) + "  #vehicles: " + str(k) + "  #Routes: " + str(len(routes_b)))
    for route in routes_b:
      print(str(list(map(lambda x : x.name,route))) + " " + str(u.cost(route)))


  depot, clientiL, clientiB, savingsL, savingsB, nClienti, k, capacity = u.prepareProblem(filename) # otteniamo i dati dal file

  if("debug" in sys.argv):# se l'utente ha chiesto il debug
    for saving in savingsB:# controlliamo che i savings siano stati ordinati correttamente
      print(str(saving[0][0].name) + " " + str(saving[0][1].name) + " " + str(saving[1]))
    print(dt.now())

  p_start_time = time.time()
  initialRoutesL = u.getInitialRoutes(depot, clientiL)
  routes_l = ClarkeWrightParallel(depot, clientiL, savingsL, initialRoutesL, k, capacity)


  initialRoutesB = u.getInitialRoutes(depot, clientiB)
  routes_b = ClarkeWrightParallel(depot, clientiB, savingsB, initialRoutesB, k, capacity, forBackhaul=False)
  p_routes = u.merge(routes_l,routes_b)
  stop_time = time.time()
  p_elapsed_time = stop_time-start_time

  if("debug" in sys.argv):
    print()
    print("PARALLEL")
    print("FINAL ROUTES:")
    print("Capacity: " + str(capacity) + "  #vehicles: " + str(k) + "  #Routes: " + str(len(p_routes)))
    for route in p_routes:
      print(str(list(map(lambda x : x.name,route))) + " " + str(u.cost(route)))
    print()
    print("LINEHAUL ROUTES:")
    print("Capacity: " + str(capacity) + "  #vehicles: " + str(k) + "  #Routes: " + str(len(routes_l)))
    for route in routes_l:
      print(str(list(map(lambda x : x.name,route))) + " " + str(u.cost(route)))
    print()
    print("BACKHAUL ROUTES:")
    print("Capacity: " + str(capacity) + "  #vehicles: " + str(k) + "  #Routes: " + str(len(routes_b)))
    for route in routes_b:
      print(str(list(map(lambda x : x.name,route))) + " " + str(u.cost(route)))



  instanceName = (filename.split('/')[-1]).split('.')[0].split('\\')[-1]
  
  names.append(instanceName)
  infile = open("./RPA_Solutions/Detailed_Solution_"+instanceName+".txt","r")
  for i in range(8):
    infile.readline()
  costoMigliore = int(infile.readline().split(' ')[-1].split(".")[0])
  infile.close()

  outfile = open("./Sequential/Risultati_"+instanceName+".txt","w")
  outfile.write("Soluzione del problema "+instanceName+"\n")
  s_costoTot = 0
  for i in range(len(s_routes)):
    outfile.write("Route:"+str(i)+"\n")
    for clnt in s_routes[i]:
      outfile.write(str(clnt.name)+" ")
    costo = u.cost(s_routes[i])
    outfile.write("\nCosto route:" + str(costo)+"\n")
    s_costoTot+=costo
  outfile.write("\nNumero di route: "+str(len(s_routes))+"\n")
  outfile.write("Numero di mezzi: "+str(k)+"\n")
  outfile.write("Costo totale:" + str(s_costoTot) + "\n")
  s_erroreRelativo = (s_costoTot - costoMigliore)/(abs(costoMigliore))
  outfile.write("Errore relativo: "+str(s_erroreRelativo)+"\n")
  outfile.write("Tempo di esecuzione: "+str(s_elapsed_time)+"\n")  
  outfile.close()
  s_errori.append(s_erroreRelativo)
  s_tempi.append(s_elapsed_time)
  dimensioniProb.append(k)

  outfile = open("./Parallel/Risultati_"+instanceName+".txt","w")
  outfile.write("Soluzione del problema "+instanceName+"\n")
  p_costoTot = 0
  for i in range(len(p_routes)):
    outfile.write("Route:"+str(i)+"\n")
    for clnt in p_routes[i]:
      outfile.write(str(clnt.name)+" ")
    costo = u.cost(p_routes[i])
    outfile.write("\nCosto route:" + str(costo)+"\n")
    p_costoTot+=costo
  outfile.write("\nNumero di route: "+str(len(p_routes))+"\n")
  outfile.write("Numero di mezzi: "+str(k)+"\n")
  outfile.write("Costo totale:" + str(p_costoTot) + "\n")
  p_erroreRelativo = (p_costoTot - costoMigliore)/(abs(costoMigliore))
  outfile.write("Errore relativo: "+str(p_erroreRelativo)+"\n")
  outfile.write("Tempo di esecuzione: "+str(p_elapsed_time)+"\n")  
  outfile.close()
  p_errori.append(p_erroreRelativo)
  p_tempi.append(p_elapsed_time)
  

df = pd.DataFrame(list(zip(*[names,p_errori,p_tempi,s_errori,s_tempi,dimensioniProb]))).add_prefix('Col')
df.columns = ['Nome_file','Errore parallelo','Tempo parallelo','Errore sequenziale','Tempo sequenziale','N mezzi']
df.to_csv('./dati.csv', index=False)

meanFile = open("./Sequential/GeneralResults.txt","w")
meanFile.write("Errore relativo medio: "+str(mean(s_errori)))
meanFile.write("\nTempo di esecuzione medio: "+str(mean(s_tempi)))
meanFile.close()

meanFile = open("./Parallel/GeneralResults.txt","w")
meanFile.write("Errore relativo medio: "+str(mean(p_errori)))
meanFile.write("\nTempo di esecuzione medio: "+str(mean(p_tempi)))
meanFile.close()

