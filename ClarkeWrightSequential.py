from Cliente import Cliente
import Utils as u

def ClarkeWrightSequential(depot, clienti, savings = [], routes = [], k = 0, capacity = 0):
    r = routes.pop()
    head = False
    result = []
    while(r != None):
        s1=u.searchSaving(r[1],savings)
        s2=u.searchSaving(r[-2],savings)
        while(s1!=None or s2 != None):
            if(s2 == None):
                head = True
                r1 = u.searchRoute(depot, s1[0][1], routes)
                savings.remove(s1)
            elif(s1 == None):
                head = False
                r1 = u.searchRoute(s2[0][1], depot, routes)
                savings.remove(s2)
            elif(s1[1] > s2[1]):
                head = True
                r1 = u.searchRoute(depot, s1[0][1], routes)
                savings.remove(s1)
            else:
                head = False
                r1 = u.searchRoute(s2[0][1], depot, routes)
                savings.remove(s2)

            if(r1 != None and (u.quantity(r1) + u.quantity(r) <= capacity)):
                newRoute = r[:-1] + r1[1:] if head else r1[:-1] + r[1:]
                routes.remove(r1)
                r=newRoute
            s1=u.searchSaving(r[1],savings)
            s2=u.searchSaving(r[-2],savings)
        result.append(r)
        if(len(routes) == 0):
            r = None
        else:
            r=routes.pop()
    return result