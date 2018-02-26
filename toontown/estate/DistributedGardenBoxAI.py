from toontown.estate.DistributedLawnDecorAI import DistributedLawnDecorAI
from toontown.estate import GardenGlobals

from direct.directnotify import DirectNotifyGlobal


class DistributedGardenBoxAI(DistributedLawnDecorAI):
    notify = directNotify.newCategory("DistributedGardenBoxAI")

    def __init__(self, air, gardenManager, ownerIndex):
        DistributedLawnDecorAI.__init__(self, air, gardenManager, ownerIndex)

        self.typeIndex = None
        self.occupier = GardenGlobals.PlanterBox

    def d_setTypeIndex(self, index):
        self.sendUpdate('setTypeIndex', [index])

    def getTypeIndex(self):
        return self.typeIndex

    def construct(self, gardenData):
        DistributedLawnDecorAI.construct(self, gardenData)

        self.typeIndex = gardenData.getUint8()

    def pack(self, gardenData):
        gardenData.addUint8(self.occupier)

        DistributedLawnDecorAI.pack(self, gardenData)

        gardenData.addUint8(self.typeIndex)
