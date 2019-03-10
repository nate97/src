from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from toontown.uberdog.DataStore import *
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.racing import RaceGlobals




class DistributedLeaderBoardAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedLeaderBoardAI")

    def __init__(self, air):
        DistributedObjectAI.__init__(self, air)
        self.air = air

        self.subscription = None
        self.area = None


        self.nameIterator = 0
        self.nameLOOP = 0
        self.recordTitle = 0 # Iterator/ selector
        self.recordTitleText = TTLocalizer.RecordPeriodStrings[0] # daily, weekly, best

        self.display = ""
        self.nameText = ""
        self.type = ""

        self.currentScore = []



    def generate(self):
        self.cycleLeaderBoard()



    def setScore(self, scores):


        for score in scores:
            print score
            
            trackId = score[0] # actual track
            genre = score[1] # Board type
            time = score[2] # Important, how long race took
            avname = str(score[3]) # Avatar name
            timestamp = score[4] # Use this to purge out weekly daily?

            name = avname.split("/")[1]

            newTupleScore = (trackId, genre, time, name, timestamp)

            if newTupleScore not in self.currentScore:

                print newTupleScore
                self.currentScore.append(newTupleScore)


    def setDisplay(self, display=""):

        print ("setting display!")
        print (self.currentScore)
        test = {"name": self.nameText, "scoreType": self.recordTitleText, "scores": self.currentScore}
        pData = cPickle.dumps(test)
        self.display = pData

        self.sendUpdate('setDisplay', [self.display])


    def getDisplay(self):
        return self.display





    def setType(self, type):
        self.type = type


    def getType(self):
        return self.type





    def setArea(self, area):
        self.area = area
    

    def d_setArea(self, area):
        self.sendUpdate('setArea', [area])
        

    def b_setArea(self, area):
        self.setArea(area)
        self.d_setArea(self, area)
    

    def getArea(self):
        return self.area


    def setPosHpr(self, x, y, z, h, p, r):
        self.sendUpdate('setPosHpr', [x, y, z, h, p, r])


    def getPosHpr(self):
        return [0,0,0,0,0,0]





    def setRecordTitle(self, recordTitleVar):
        self.recordTitleText = TTLocalizer.RecordPeriodStrings[recordTitleVar]
        self.recordTitle = recordTitleVar


    def getRecordTitle(self):
        return self.recordTitle








    def setName(self, name):
        nameText = TTLocalizer.KartRace_TrackNames.get(name)
        self.nameText = nameText

    def getName(self):
        return self.nameIterator
















    def subscribeTo(self, leaderBoardType):
        self.iterateName(leaderBoardType)











    def iterateName(self, leaderBoardType): # NJF
        if leaderBoardType == "stadium":
            track = self.iterateRecordTitle()

            if track == 2: # NEXT TRACK
                self.nameLOOP += 1

                if self.nameLOOP >= 4: # If we go above this many tracks reset back to zero
                    self.nameLOOP = 0

            nameId = RaceGlobals.SpeedwayList[self.nameLOOP] # SELECT NAME

            allScores = self.air.leaderBoardMgr.getAllScores()      
            currentScores = allScores[nameId]
            print (currentScores)
            self.setScore(currentScores)

            self.setName(nameId)



        elif leaderBoardType == "city":
            track = self.iterateRecordTitle()

            if track == 2: # NEXT TRACK
                self.nameLOOP += 1

                if self.nameLOOP >= 4: # If we go above this many tracks reset back to zero
                    self.nameLOOP = 0

            nameId = RaceGlobals.UrbanList[self.nameLOOP] # SELECT NAME

            allScores = self.air.leaderBoardMgr.getAllScores()      
            currentScores = allScores[nameId]
            print (currentScores)
            self.setScore(currentScores)

            self.setName(nameId)




        elif leaderBoardType == "country":
            track = self.iterateRecordTitle()

            if track == 2: # NEXT TRACK
                self.nameLOOP += 1

                if self.nameLOOP >= 4: # If we go above this many tracks reset back to zero
                    self.nameLOOP = 0

            nameId = RaceGlobals.RuralList[self.nameLOOP] # SELECT NAME

            allScores = self.air.leaderBoardMgr.getAllScores()      
            currentScores = allScores[nameId]
            print (currentScores)
            self.setScore(currentScores)

            self.setName(nameId)









    def iterateRecordTitle(self):
        if self.recordTitle == 0:
            self.setRecordTitle(1)
            return 0

        elif self.recordTitle == 1:
            self.setRecordTitle(2)
            return 1

        elif self.recordTitle == 2:
            self.setRecordTitle(0)
            return 2 # NEXT TRACK



    def cycleLeaderBoard(self, task=None):
        self.subscribeTo(self.type)
        self.setDisplay()
        taskMgr.doMethodLater(5, self.cycleLeaderBoard, 'leaderBoardUpdate')



