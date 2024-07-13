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
    def __init__(self, startingShipIntegrity, playerIDs):
        self.shipIntegrity = startingShipIntegrity
        self.gameLoopCount = 0
        self.crewMembers = []
        for pID in playerIDs:
            self.crewMembers.append(CrewMember(playerIDs.name))

    def update(self):
        pass
