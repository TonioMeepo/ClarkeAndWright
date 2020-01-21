from Cliente import Cliente
import Utils as u

def ClarkeWrightParallel(depot, clienti, savings = [], routes = [], k = 0, capacity = 0):
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
    
    while(len(routes)<k):
        r = routes[0]
        half = len(r)/2
        r1 = r[:half]+[depot]
        r2 = [depot]+r[half:]
        routes.append(r1)
        routes.append(r2)
        routes.remove(r)

    return routes