import Utils as u
from Cliente import Cliente
from tkinter import Tk
from tkinter.filedialog import askopenfilename



Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

depot, clientiL, clientiB, savingsL, savingsB, nClienti, k = u.prepareProblem(filename)

for saving in savingsB:
  print(str(saving[0][0].name) + " " + str(saving[0][1].name) + " " + str(saving[1]))