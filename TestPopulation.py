class Individual:
    def __init__(self, x, y, color):
        self.xpos = x
        self.ypos = y
        self.color = color

    def behavior(self, neighbors, requests):
        raise NotImplementedError("All subclasses must have a behavior!")

    def getpos(self):
        return self.xpos, self.ypos

    def getColor(self):
        return self.color


class Dead(Individual):
    color = (0, 0, 0)

    def __init__(self, x, y):
        super(Dead, self).__init__(x, y, Dead.color)

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

    def __init__(self, x, y):
        super(Alive, self).__init__(x, y, Alive.color)

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

    def __init__(self, x, y):
        super(FireElemental, self).__init__(x, y, FireElemental.color)

    def behavior(self, neighbors, requests):
        weakness = 0
        for individual in neighbors:
            if isinstance(individual, AirElemental): weakness += 1
        if weakness >= 3:
            requests[self.xpos][self.ypos] = AirElemental(self.xpos, self.ypos)
        else:
            requests[self.xpos][self.ypos] = FireElemental(self.xpos, self.ypos)


class AirElemental(Individual):
    color = (255, 200, 100)

    def __init__(self, x, y):
        super(AirElemental, self).__init__(x, y, AirElemental.color)

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

    def __init__(self, x, y):
        super(WaterElemental, self).__init__(x, y, WaterElemental.color)

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

    def __init__(self, x, y):
        super(EarthElemental, self).__init__(x, y, EarthElemental.color)

    def behavior(self, neighbors, requests):
        weakness = 0
        for individual in neighbors:
            if isinstance(individual, FireElemental): weakness += 1
        if weakness >= 3:
            requests[self.xpos][self.ypos] = FireElemental(self.xpos, self.ypos)
        else:
            requests[self.xpos][self.ypos] = EarthElemental(self.xpos, self.ypos)


class Agar(Individual):
    color = (50, 255, 50)

    def __init__(self, x, y):
        super(Agar, self).__init__(x, y, Agar.color)

    def behavior(self, neighbors, requests):
        eaten = False
        for individual in neighbors:
            if isinstance(individual, Bacteria):
                eaten = True
                break
        if eaten:
            requests[self.xpos][self.ypos] = Bacteria(self.xpos, self.ypos)
        else:
            requests[self.xpos][self.ypos] = Agar(self.xpos, self.ypos)


class Bacteria(Individual):
    color = (100, 200, 200)

    def __init__(self, x, y):
        super(Bacteria, self).__init__(x, y, Bacteria.color)

    def behavior(self, neighbors, requests):
        crowding = 0
        for individual in neighbors:
            if isinstance(individual, Bacteria) or isinstance(individual, Waste):
                crowding += 1
        if crowding >= 6:
            requests[self.xpos][self.ypos] = Waste(self.xpos, self.ypos)
        else:
            requests[self.xpos][self.ypos] = Bacteria(self.xpos, self.ypos)


class Waste(Individual):
    color = (100, 100, 50)

    def __init__(self, x, y):
        super(Waste, self).__init__(x, y, Waste.color)

    def behavior(self, neighbors, requests):
        eaten = False
        for individual in neighbors:
            if isinstance(individual, Amoeba):
                eaten = True
                break
        if eaten:
            requests[self.xpos][self.ypos] = Amoeba(self.xpos, self.ypos)
        else:
            requests[self.xpos][self.ypos] = Waste(self.xpos, self.ypos)


class Amoeba(Individual):
    color = (200, 200, 100)

    def __init__(self, x, y):
        super(Amoeba, self).__init__(x, y, Amoeba.color)

    def behavior(self, neighbors, requests):
        feeding = False
        for individual in neighbors:
            if isinstance(individual, Waste):
                feeding = True
                break
        if feeding:
            requests[self.xpos][self.ypos] = Agar(self.xpos, self.ypos)
        else:
            requests[self.xpos][self.ypos] = Amoeba(self.xpos, self.ypos)
