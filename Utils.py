from Cliente import Cliente

#Method used to sort saving in a non increasing fashion
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

def prepareProblem(filename = ''):
    inputFile = open(filename)
    nClienti = int(inputFile.readline())
    inputFile.readline()
    k = int(inputFile.readline())
    clientiL = []
    clientiB = []
    nClientiL =0
    nClientiB =0

    linea = inputFile.readline().split('   ')
    depot = Cliente(name = 0,x=int(linea[0]),y=int(linea[1]),isDepot=True)
    capacity = int(linea[3])
    for i in range(nClienti):
        linea = inputFile.readline().split('   ')
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
            if(c1.name!=c2.name):
                savingsL.append(((c1,c2),c1.saving(c2,depot)))

    savingsL = sortSavings(savingsL)

    for c2 in clientiB:
        for c1 in clientiB:
            if(c1.name!=c2.name):
                savingsB.append(((c1,c2),c1.saving(c2,depot)))


    savingsB = sortSavings(savingsB)
    return depot, clientiL, clientiB, savingsL, savingsB, nClienti, k, capacity

def getInitialRoutes(depot, clienti):
    routes = []
    for cliente in clienti:
        routes.append([depot, cliente, depot])
    return routes

def searchRoute(c1, c2, routes):
    for route in routes:
        if((route[0] == c1 and route[1] == c2 ) or (route[-2] == c1 and route[-1] == c2)):
            return route
    return None

def searchSaving(c,savings):
    for s in savings:
        if(c == s[0][0]):
            return s
    return None

def quantity(route):
    sum = 0
    for c in route:
        if(not c.isDepot):
            sum += c.consegna if c.linehaul else c.ritiro
    return sum

def forcedCombine(routes, k, capacity):
    r = routes
    mixed = True
    while(mixed):
        mixed = False
        routes = r
        check = [False for i in range(len(routes))]
        for i in range(len(routes)):
            for j in range(len(routes)):
                if (j!=i and (not check[i]and not check[j] )):
                    newRoute = routes[i][:-1] + routes[j][1:]
                    if (quantity(newRoute)<=capacity):
                        r.remove(routes[i])
                        r.remove(routes[j])
                        r.append(newRoute)
                        check.append(False)
                        check[i] = True
                        check[j] = True
                        mixed = True
                        if(len(r)<=k):
                            return r
    if(len(r)>k):
            print("Impossible")
    return r

def cost(route):
    somma = 0
    for i in range(len(route)-1):
        somma += route[i].distanza(route[i+1])
    return somma
        

def sortByCost(x):
    #ascendente
    if len(x) <=1:
        return x
    result = []
    mid = int(len(x) / 2)
    y = sortByCost(x[:mid])
    z = sortByCost(x[mid:])
    i = 0
    j = 0
    while i < len(y) and j < len(z):
        if cost(y[i]) > cost(z[j]):
            result.append(z[j])
            j += 1
        else:
            result.append(y[i])
            i += 1
    result += y[i:]
    result += z[j:]
    return result


def merge(routes_c,routes_r):
    dist = []
    result = routes_c
    usati = []
    for c in routes_c:
        for r in routes_r:
            dist.append(((c,r),c[-2].distanza(r[1])))
    dist = sortSavings(dist)[::-1]

    for d in dist:
        if (d[0][0] not in usati and d[0][1] not in usati):
            result.remove(d[0][0])
            result.append(d[0][0][:-2]+d[0][1][1:])
            usati.append(d[0][0])
            usati.append(d[0][1])
    return result

                