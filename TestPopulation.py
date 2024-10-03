class Individual:
    def __init__(self, xindex, yindex, color):
        self.xpos = xindex
        self.ypos = yindex
        self.color = color

    def behavior(self, neighbors, requests):
        raise NotImplementedError("All subclasses must have a behavior!")

    def getpos(self):
        return self.xpos, self.ypos

    def getColor(self):
        return self.color


class Dead(Individual):
    color=(0, 0, 0)
    def __init__(self, xindex, yindex):
        super(Dead, self).__init__(xindex, yindex, Dead.color)

    def behavior(self, neighbors, requests):
        crowding = 0
        for individual in neighbors:
            if isinstance(individual, Alive): crowding += 1
        if crowding == 3:
            requests[self.xpos][self.ypos] = Alive(self.xpos, self.ypos)
        else:
            requests[self.xpos][self.ypos] = Dead(self.xpos, self.ypos)


class Alive(Individual):
    color = (255, 255, 255)
    def __init__(self, xindex, yindex):
        super(Alive, self).__init__(xindex, yindex, Alive.color)

    def behavior(self, neighbors, requests):
        crowding = 0
        for individual in neighbors:
            if isinstance(individual, Alive): crowding += 1
        if crowding == 2 or crowding == 3:
            requests[self.xpos][self.ypos] = Alive(self.xpos, self.ypos)
        else:
            requests[self.xpos][self.ypos] = Dead(self.xpos, self.ypos)

class FireElemental(Individual):
    color = (255, 100, 100)
    def __init__(self, xindex, yindex):
        super(FireElemental, self).__init__(xindex, yindex, FireElemental.color)

    def behavior(self, neighbors, requests):
        weakness=0
        for individual in neighbors:
            if isinstance(individual, AirElemental): weakness += 1
        if weakness >= 3:
            requests[self.xpos][self.ypos] = AirElemental(self.xpos, self.ypos)
        else:
            requests[self.xpos][self.ypos] = FireElemental(self.xpos, self.ypos)

class AirElemental(Individual):
    color = (255, 200, 100)
    def __init__(self, xindex, yindex):
        super(AirElemental, self).__init__(xindex, yindex, AirElemental.color)

    def behavior(self, neighbors, requests):
        weakness = 0
        for individual in neighbors:
            if isinstance(individual, WaterElemental): weakness += 1
        if weakness >= 3:
            requests[self.xpos][self.ypos] = WaterElemental(self.xpos, self.ypos)
        else:
            requests[self.xpos][self.ypos] = AirElemental(self.xpos, self.ypos)

class WaterElemental(Individual):
    color = (100, 100, 255)
    def __init__(self, xindex, yindex):
        super(WaterElemental, self).__init__(xindex, yindex, WaterElemental.color)

    def behavior(self, neighbors, requests):
        weakness = 0
        for individual in neighbors:
            if isinstance(individual, EarthElemental): weakness += 1
        if weakness >= 3:
            requests[self.xpos][self.ypos] = EarthElemental(self.xpos, self.ypos)
        else:
            requests[self.xpos][self.ypos] = WaterElemental(self.xpos, self.ypos)

class EarthElemental(Individual):
    color = (50, 200, 50)
    def __init__(self, xindex, yindex):
        super(EarthElemental, self).__init__(xindex, yindex, EarthElemental.color)

    def behavior(self, neighbors, requests):
        weakness = 0
        for individual in neighbors:
            if isinstance(individual, FireElemental): weakness += 1
        if weakness >= 3:
            requests[self.xpos][self.ypos] = FireElemental(self.xpos, self.ypos)
        else:
            requests[self.xpos][self.ypos] = EarthElemental(self.xpos, self.ypos)