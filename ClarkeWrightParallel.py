from Cliente import Cliente
import Utils as u

def ClarkeWrightParallel(depot, clienti, savings = [], routes = [], k = 0, capacity = 0, forBackhaul = False):
    for s in savings:
        r1 = u.searchRoute(depot, s[0][1], routes)
        r2 = u.searchRoute(s[0][0], depot, routes)
        if((r1 != None and r2 != None) and u.quantity(r1)+u.quantity(r2) <= capacity):
            newRoute = r1[:-1] + r2[1:]
            routes.remove(r1)
            routes.remove(r2)
            routes.append(newRoute)

    routes = u.sortByCost(routes)
    if (len(routes)>k):
        routes = u.forcedCombine(routes,k,capacity)
    
    # if(not forBackhaul):
    #     routes = u.sortByCost(routes)
    #     while(len(routes)<k):
    #         r = routes.pop()
            
    #         half = u.cost(r)/2
    #         acc=0
    #         i=2
    #         #while(acc<half):
    #         #    acc = u.cost(r[:i])
    #         #    i+=1
    #         r1 = r[:i]+[depot]
    #         r2 = [depot]+r[i:]
    #         routes.append(r1)
    #         routes.append(r2)
    #         routes= u.sortByCost(routes)
    return routes