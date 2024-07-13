class CrewMember:
    def __init__(self, name):
        self.name = name


class ShipEvent:
    def __init__(self, name):
        self.name = name


class ShipLocation:
    def __init__(self, name):
        self.name = name
        self.active = False


class Game:
    # PlayerID entries need to have a name property!
    def __init__(self, startingShipIntegrity):
        self.shipIntegrity = startingShipIntegrity
        self.gameLoopCount = 0
        self.crewMembers = []

    def addPlayer(self, playerID):
        self.crewMembers.append(CrewMember(playerID))

    def update(self):
        pass
