from direct.distributed.DistributedNodeAI import DistributedNodeAI

from toontown.estate import GardenGlobals


class DistributedLawnDecorAI(DistributedNodeAI):
    notify = directNotify.newCategory('DistributedLawnDecorAI')

    def __init__(self, air, gardenManager, ownerIndex):
        DistributedNodeAI.__init__(self, air)

        self.gardenManager = gardenManager
        self.ownerIndex = ownerIndex

        self.plotIndex = None
        self.plotType = None

        self.boxIndex = None
        self.boxType = None

        self.pos = None
        self.heading = None

        self.movie = None

    def getPlot(self):
        return self.plotIndex

    def getHeading(self):
        return self.heading

    def getPosition(self):
        return self.pos

    def getOwnerIndex(self):
        return self.ownerIndex

    def plotEntered(self):
        pass

    def removeItem(self):
        self.setMovie(GardenGlobals.MOVIE_REMOVE, self.air.getAvatarIdFromSender())
        self.gardenManager.revertToPlot(self.plotIndex)

    def setMovie(self, movie, avId):
        self.movie = movie
        self.sendUpdate('setMovie', [movie, avId])

    def movieDone(self):
        self.setMovie(GardenGlobals.MOVIE_CLEAR, self.air.getAvatarIdFromSender())

    def interactionDenied(self, avId):
        self.sendUpdate('interactionDenied', [avId])

    def construct(self, gardenData):
        # NF
        # Working on getting flower boxes to generate...

        self.plotIndex = gardenData.getUint8()



        if self.plotIndex == 91 or self.plotIndex == 92 or self.plotIndex == 93:
            print "We DO have a flowerbox!!!"

            # TEMP CODE
            self.boxType = 92
            #self.boxType = GardenGlobals.getBoxType(self.ownerIndex, self.plotIndex)
            self.pos = (0,0,50)
            self.heading = 250

        else:
            print "Not a flowerbox!"
            print self.plotIndex2
            print "Not a flowerbox!"

            self.plotType = GardenGlobals.getPlotType(self.ownerIndex, self.plotIndex)
            self.pos = GardenGlobals.getPlotPos(self.ownerIndex, self.plotIndex)
            self.heading = GardenGlobals.getPlotHeading(self.ownerIndex, self.plotIndex)





    def pack(self, gardenData):
        gardenData.addUint8(self.plotIndex)






"""
        # NF
        # Working on getting flower boxes to generate...

        self.plotIndex = gardenData.getUint8()


        if self.plotIndex != GardenGlobals.PlanterBox:

            self.plotType = GardenGlobals.getPlotType(self.ownerIndex, self.plotIndex)
            self.pos = GardenGlobals.getPlotPos(self.ownerIndex, self.plotIndex)
            print self.pos
            self.heading = GardenGlobals.getPlotHeading(self.ownerIndex, self.plotIndex)
            print self.heading
            print "Heading^^^"

        else:

            print "YAS?????????????"
            self.boxType = GardenGlobals.getBoxType(self.ownerIndex, self.plotIndex)
            self.pos = (0,0,50)
            self.heading = 250

"""









