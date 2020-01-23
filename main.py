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
routes_b = ClarkeWrightSequential(depot, clientiB, savingsB, initialRoutesB, k, capacity)
routes = u.merge(routes_l,routes_b)
stop_time = time.time()
elapsed_time = stop_time-start_time

if("debug" in sys.argv):
  print()
  print("Backhaul")
  print("Capacity: " + str(capacity) + "  #vehicles: " + str(k) + "  #Routes: " + str(len(routes)))
  for route in routes:
    print(str(list(map(lambda x : x.name,route))) + " " + str(u.cost(route)))

infile = open("Detailed_Solution_"+filename,"r")
for i in range(8):
  infile.readline()
costoMigliore = int(infile.readline())
infile.close()

outfile = open("Risultati_"+filename,"w")
outfile.write("Soluzione del problema "+filename+"\n")
for i in range(len(routes)):
  outfile.write("Route:"+i+"\n")
  costoTot = 0
  for clnt in routes[i]:
    outfile.write(clnt.name+" ")
  costo = u.cost(routes[i])
  outfile.write("\nCosto route:" + costo+"\n")
  costoTot+=costo
outfile.write("\nNumero di route: "+len(routes)+"\n")
outfile.write("Costo totale:" + costoTot + "\n")
erroreRelativo = (costoTot - costoMigliore)/(abs(costoMigliore))
outfile.write("Errore relativo: "+erroreRelativo+"\n")
outfile.write("Tempo di esecuzione: "+elapsed_time+"\n")  
outfile.close()