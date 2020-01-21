import Utils as u
from Cliente import Cliente
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import sys
from datetime import datetime as dt
from ClarkeWrightParallel import ClarkeWrightParallel
from ClarkeWrightSequential import ClarkeWrightSequential

#prova
Tk().withdraw() 
filename = askopenfilename() # Chiediamo all'utente di aprire il file

depot, clientiL, clientiB, savingsL, savingsB, nClienti, k, capacity = u.prepareProblem(filename) # otteniamo i dati dal file

if("debug" in sys.argv):# se l'utente ha chiesto il debug
  for saving in savingsB:# controlliamo che i savings siano stati ordinati correttamente
    print(str(saving[0][0].name) + " " + str(saving[0][1].name) + " " + str(saving[1]))
  print(dt.now())


initialRoutesL = u.getInitialRoutes(depot, clientiL)
routes_l = ClarkeWrightSequential(depot, clientiL, savingsL, initialRoutesL, k, capacity)


initialRoutesB = u.getInitialRoutes(depot, clientiB)
routes_b = ClarkeWrightSequential(depot, clientiB, savingsB, initialRoutesB, k, capacity)



routes = u.merge(routes_l,routes_b)


if("debug" in sys.argv):
  print()
  print("Backhaul")
  print("Capacity: " + str(capacity) + "  #vehicles: " + str(k) + "  #Routes: " + str(len(routes)))
  for route in routes:
    print(str(list(map(lambda x : x.name,route))) + " " + str(u.cost(route)))