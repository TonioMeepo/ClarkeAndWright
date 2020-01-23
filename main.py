import Utils as u
from Cliente import Cliente
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import sys
from datetime import datetime as dt
from ClarkeWrightParallel import ClarkeWrightParallel
from ClarkeWrightSequential import ClarkeWrightSequential
import time

#prova
Tk().withdraw() 
filename = askopenfilename() # Chiediamo all'utente di aprire il file

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
routes = u.merge(routes_l,routes_b)
stop_time = time.time()
elapsed_time = stop_time-start_time

if("debug" in sys.argv):
  print()
  print("FINAL ROUTES:")
  print("Capacity: " + str(capacity) + "  #vehicles: " + str(k) + "  #Routes: " + str(len(routes)))
  for route in routes:
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

instanceName = (filename.split('/')[-1]).split('.')[0]
infile = open("./RPA_Solutions/Detailed_Solution_"+instanceName+".txt","r")
for i in range(8):
  infile.readline()
costoMigliore = int(infile.readline().split(' ')[-1].split(".")[0])
infile.close()

outfile = open("Risultati_"+instanceName+".txt","w")
outfile.write("Soluzione del problema "+instanceName+"\n")
costoTot = 0
for i in range(len(routes)):
  outfile.write("Route:"+str(i)+"\n")
  for clnt in routes[i]:
    outfile.write(str(clnt.name)+" ")
  costo = u.cost(routes[i])
  outfile.write("\nCosto route:" + str(costo)+"\n")
  costoTot+=costo
outfile.write("\nNumero di route: "+str(len(routes))+"\n")
outfile.write("Costo totale:" + str(costoTot) + "\n")
erroreRelativo = (costoTot - costoMigliore)/(abs(costoMigliore))
outfile.write("Errore relativo: "+str(erroreRelativo)+"\n")
outfile.write("Tempo di esecuzione: "+str(elapsed_time)+"\n")  
outfile.close()