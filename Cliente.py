class Cliente:

  def init(self, name = 0, x = 0, y = 0, consegna = 0, ritiro = 0, isDepot=False):
    self.name = name
    self.x = x
    self.y = y
    if(consegna == 0):
      self.linehaul = False
    else:
      self.linehaul = True

    self.ritiro = ritiro
    self.consegna = consegna

  def distanza(self,other):
    return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

  def saving(self,other,depot):
    return self.distanza(depot)+depot.distanza(other)-self.distanza(other)