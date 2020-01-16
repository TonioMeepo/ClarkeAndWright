from Cliente import Cliente

def sortSavings(x):
    if len(x) <=1:
        return x
    result = []
    mid = int(len(x) / 2)
    y = sortSavings(x[:mid])
    z = sortSavings(x[mid:])
    i = 0
    j = 0
    while i < len(y) and j < len(z):
        if y[i][1] < z[j][1]:
            result.append(z[j])
            j += 1
        else:
            result.append(y[i])
            i += 1
    result += y[i:]
    result += z[j:]
    return result

inputFile = open("./Instances/N1.txt")
nClienti = int(inputFile.readLine())
inputFile.readLine()
k = int(inputFile.readLine())
clientiL = []
clientiB = []
nClientiL =0
nClientiB =0

linea = inputFile.readLine().split('   ')
depot = Cliente(name = 0,x=int(linea[0]),y=int(linea[1]),isDepot=True)

for i in range(n):
  linea = inputFile.readLine().split('   ')
  if(int(linea[3]) == 0):
    clientiL.append(Cliente(name=i+1,x=int(linea[0]),y=int(linea[1]),consegna=int(linea[2])))
    nClientiL+=1
  else:
    clientiB.append(Cliente(name=i+1,x=int(linea[0]),y=int(linea[1]),ritiro=int(linea[3])))
    nClientiB+=1

savingsL = []
savingsB = []

for c1 in clientiL:
  for c2 in clientiL:
    savingsL.append(((c1,c2),c1.saving(c2,depot)))

savingsL = sortSavings(savingsL)

for c2 in clientiB:
  for c1 in clientiB:
    savingsB.append(((c1,c2),c1.saving(c2,depot)))


savingsB = sortSavings(savingsB)
