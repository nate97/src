from direct.directnotify.DirectNotifyGlobal import *
from direct.distributed import DistributedObjectAI
import datetime
import time
import csv
import ast
import os

class DistributedLeaderBoardManagerAI(DistributedObjectAI.DistributedObjectAI):
    notify = directNotify.newCategory('LeaderBoardManagerAI')

    def __init__(self, air):

        self.air = air

        # Directory
        self.backDir = 'backups/'
        self.folderName = 'raceboards/'
        self.fileName = str(self.air.districtId) # Used for our filename
        self.extension = '.csv'
        self.fullPath = self.backDir + self.folderName 
        self.fullName = self.fileName + self.extension

        # Leaderboard instances
        self.stadiumBoard = None
        self.ruralBoard = None
        self.urbanBoard = None

        # How long it takes before we display the next race scores
        self.cycleTime = 10

        # Genres
        Speedway = 0
        Rural = 1
        Urban = 2

        # Record IDs
        Daily = 0
        Weekly = 1
        AllTime = 2

        # Name used for default race player
        self.defaultName = "Goofy"

        # Record text
        LeaderBoard_Daily = 'Daily Scores'
        LeaderBoard_Weekly = 'Weekly Scores'
        LeaderBoard_AllTime = 'All Time Best Scores'
        self.recordPeriodStrings = [LeaderBoard_Daily, LeaderBoard_Weekly, LeaderBoard_AllTime]

        # Racetrack IDs
        RT_Speedway_1 = 0
        RT_Speedway_1_rev = 1
        RT_Speedway_2 = 60
        RT_Speedway_2_rev = 61
        RT_Rural_1 = 20
        RT_Rural_1_rev = 21
        RT_Rural_2 = 62
        RT_Rural_2_rev = 63
        RT_Urban_1 = 40
        RT_Urban_1_rev = 41
        RT_Urban_2 = 64
        RT_Urban_2_rev = 65

        # Minimum requirements to get on board
        speedway1Minimum = 115
        speedway2Minimum = 210
        rural1Minimum = 230
        rural2Minimum = 360
        urban1Minimum = 305
        urban2Minimum = 280

        # Minimum values dict
        self.minimumValueDict = {
        RT_Speedway_1: speedway1Minimum,
        RT_Speedway_1_rev: speedway1Minimum,
        RT_Speedway_2: speedway2Minimum,
        RT_Speedway_2_rev: speedway2Minimum,
        RT_Rural_1: rural1Minimum,
        RT_Rural_1_rev: rural1Minimum,

        RT_Rural_2: rural2Minimum,
        RT_Rural_2_rev: rural2Minimum,
        RT_Urban_1: urban1Minimum,
        RT_Urban_1_rev: urban1Minimum,
        RT_Urban_2: urban2Minimum,
        RT_Urban_2_rev: urban2Minimum,
        }

        # Racetrack names
        KartRace_Reverse = ' Rev'
        self.KartRace_TrackNames = {
        RT_Speedway_1: 'Screwball Stadium',
        RT_Speedway_1_rev: 'Screwball Stadium' + KartRace_Reverse,
        RT_Rural_1: 'Rustic Raceway',
        RT_Rural_1_rev: 'Rustic Raceway' + KartRace_Reverse,
        RT_Urban_1: 'City Circuit',
        RT_Urban_1_rev: 'City Circuit' + KartRace_Reverse,
        RT_Speedway_2: 'Corkscrew Coliseum',
        RT_Speedway_2_rev: 'Corkscrew Coliseum' + KartRace_Reverse,
        RT_Rural_2: 'Airborne Acres',
        RT_Rural_2_rev: 'Airborne Acres' + KartRace_Reverse,
        RT_Urban_2: 'Blizzard Boulevard',
        RT_Urban_2_rev: 'Blizzard Boulevard' + KartRace_Reverse
        }

        self.orderedTrackKeys = {
            Speedway: [(RT_Speedway_1, Daily),
                    (RT_Speedway_1, Weekly),
                    (RT_Speedway_1, AllTime),
                    (RT_Speedway_1_rev, Daily),
                    (RT_Speedway_1_rev, Weekly),
                    (RT_Speedway_1_rev, AllTime),
                    (RT_Speedway_2, Daily),
                    (RT_Speedway_2, Weekly),
                    (RT_Speedway_2, AllTime),
                    (RT_Speedway_2_rev, Daily),
                    (RT_Speedway_2_rev, Weekly),
                    (RT_Speedway_2_rev, AllTime)],
            Rural: [(RT_Rural_1, Daily),
                    (RT_Rural_1, Weekly),
                    (RT_Rural_1, AllTime),
                    (RT_Rural_1_rev, Daily),
                    (RT_Rural_1_rev, Weekly),
                    (RT_Rural_1_rev, AllTime),
                    (RT_Rural_2, Daily),
                    (RT_Rural_2, Weekly),
                    (RT_Rural_2, AllTime),
                    (RT_Rural_2_rev, Daily),
                    (RT_Rural_2_rev, Weekly),
                    (RT_Rural_2_rev, AllTime)],
            Urban: [(RT_Urban_1, Daily),
                    (RT_Urban_1, Weekly),
                    (RT_Urban_1, AllTime),
                    (RT_Urban_1_rev, Daily),
                    (RT_Urban_1_rev, Weekly),
                    (RT_Urban_1_rev, AllTime),
                    (RT_Urban_2, Daily),
                    (RT_Urban_2, Weekly),
                    (RT_Urban_2, AllTime),
                    (RT_Urban_2_rev, Daily),
                    (RT_Urban_2_rev, Weekly),
                    (RT_Urban_2_rev, AllTime)]
        }

        self.recordLists = {
            (RT_Speedway_1, Daily): [],
            (RT_Speedway_1, Weekly): [],
            (RT_Speedway_1, AllTime): [],
            (RT_Speedway_1_rev, Daily): [],
            (RT_Speedway_1_rev, Weekly): [],
            (RT_Speedway_1_rev, AllTime): [],
            (RT_Rural_1, Daily): [],
            (RT_Rural_1, Weekly): [],
            (RT_Rural_1, AllTime): [],
            (RT_Rural_1_rev, Daily): [],
            (RT_Rural_1_rev, Weekly): [],
            (RT_Rural_1_rev, AllTime): [],
            (RT_Urban_1, Daily): [],
            (RT_Urban_1, Weekly): [],
            (RT_Urban_1, AllTime): [],
            (RT_Urban_1_rev, Daily): [],
            (RT_Urban_1_rev, Weekly): [],
            (RT_Urban_1_rev, AllTime): [],
            (RT_Speedway_2, Daily): [],
            (RT_Speedway_2, Weekly): [],
            (RT_Speedway_2, AllTime): [],
            (RT_Speedway_2_rev, Daily): [],
            (RT_Speedway_2_rev, Weekly): [],
            (RT_Speedway_2_rev, AllTime): [],
            (RT_Rural_2, Daily): [],
            (RT_Rural_2, Weekly): [],
            (RT_Rural_2, AllTime): [],
            (RT_Rural_2_rev, Daily): [],
            (RT_Rural_2_rev, Weekly): [],
            (RT_Rural_2_rev, AllTime): [],
            (RT_Urban_2, Daily): [],
            (RT_Urban_2, Weekly): [],
            (RT_Urban_2, AllTime): [],
            (RT_Urban_2_rev, Daily): [],
            (RT_Urban_2_rev, Weekly): [],
            (RT_Urban_2_rev, AllTime): []
        }

        self.stadiumCount = 0
        self.ruralCount = 0
        self.cityCount = 0
        self.countIteratorList = [self.stadiumCount, self.ruralCount, self.cityCount]

        self.createScoreCSV()
        self.leaderBoardTask()



    ###############################################################################################
    ############################### BUILDING OUR DEFAULT DICTIONARY ###############################
    ###############################################################################################

    def createScoreCSV(self):

        if not os.path.exists(self.backDir):
            os.mkdir(self.backDir)

        if not os.path.exists(self.fullPath):
            os.mkdir(self.fullPath)
            self.raceScoresDict = self.createRaceScoreDict()
            self.exportScores(self.raceScoresDict)

        else:

            if not os.path.exists(self.fullPath + self.fullName):
                self.raceScoresDict = self.createRaceScoreDict()
                self.exportScores(self.raceScoresDict)
            else:

                reader = csv.reader(open(self.fullPath + self.fullName, 'r'))
                previousScores = {}
                for row in reader:
                    key, value = row

                    key = ast.literal_eval(key)
                    value = ast.literal_eval(value)

                    previousScores[key] = value

                del reader

                if previousScores != {}: # Patch to not overwrite if file ends up being blank
                    self.raceScoresDict = previousScores
                else:
                    self.raceScoresDict = self.createRaceScoreDict()
                    self.exportScores(self.raceScoresDict)



    def exportScores(self, scoreList):
        w = csv.writer(open(self.fullPath + self.fullName, 'w'))
        for key, val in scoreList.items():
            w.writerow([key, val])
        del w # Close



    def createRaceScoreDict(self): # Only called if records file is empty!
        boardDict = {}

        allTrackGenres = self.orderedTrackKeys

        for genre in allTrackGenres:
            trackRecords = allTrackGenres[genre]

            for raceKey in trackRecords: # raceKey is used in of itsself as a key in the boardDict
                raceId = raceKey[0]
                recordTitleId = raceKey[1]

                raceScores = self.recordLists[raceKey]
                raceScores = self.setDefaultWins(raceScores, raceId) # Furnish our list with the default race player ( Goofy )
      
                completedList = raceScores # IMPORTANT!!! THIS IS WHERE WE'RE APPENDING NEW STUFF

                boardDict[raceKey] = completedList

        return boardDict



    def setDefaultWins(self, raceScores, raceId):
        for defaultRacer in range(0, 10):
            self.setDefaultRacer(raceScores, raceId)
        return raceScores # Returns furnished list



    def setDefaultRacer(self, raceScores, raceId):
        raceScores.append((self.defaultName, self.minimumValueDict[raceId], 0))



    ###############################################################################################
    ############################### THIS MANAGES OUR BOARD INSTANCES ##############################
    ###############################################################################################

    def defineBoardInstance(self, genre, boardInstance): # This function allows us to define the three different leaderboards for us to control them
        if genre == 0: # Stadium
            self.stadiumBoard = boardInstance
        elif genre == 1: # Rural
            self.ruralBoard = boardInstance
        elif genre == 2: # Urban
            self.urbanBoard = boardInstance



    def leaderBoardTask(self, task=None):
        if self.ruralBoard: # If all boards have been generated initiate tasks
            self.cycleBoardMgr(0, self.stadiumBoard)
            self.cycleBoardMgr(1, self.ruralBoard)
            self.cycleBoardMgr(2, self.urbanBoard)

        taskMgr.doMethodLater(self.cycleTime, self.leaderBoardTask, 'leaderBoardTask')



    def cycleBoardMgr(self, genre, boardInstance):
        if self.countIteratorList[genre] >= 12: # If we go over 12, reset ( Cycles 0 through 12 )
            self.countIteratorList[genre] = 0

        activeTracks = self.orderedTrackKeys[genre]
        curTrack = activeTracks[self.countIteratorList[genre]]      

        trackId = curTrack[0]
        recordId = curTrack[1]
        trackScores = self.raceScoresDict[curTrack]

        self.removeAfterXtime(trackId, recordId) # Keeps old entries from accumulating

        trackTitle = self.KartRace_TrackNames[trackId] # Text
        recordTitle = self.recordPeriodStrings[recordId] # Text
        trackData = (trackTitle, recordTitle, trackScores)

        self.setBoardDisplay(trackData, boardInstance) # Send data back to leader board

        self.countIteratorList[genre] = self.countIteratorList[genre] + 1 # Count up



    def setBoardDisplay(self, trackData, boardInstance):
        boardInstance.setDisplay(trackData) 



    ###########################################################################################################
    ############################### MECHANISMS FOR APPENDING & REMOVING PLAYERS ###############################
    ###########################################################################################################



    def appendNewRaceEntry(self, raceId, recordId, av, totalTime, timeStamp): # Appends new race entry IF they qualify
        minimumTimeRequirement =  self.minimumValueDict[raceId]
        if totalTime >= minimumTimeRequirement:
            return # This player took too long to be displayed on the board!

        scoreList = self.findRaceScoreList(raceId, recordId)

        newRaceEntry = (av, totalTime, timeStamp) # Player's info
        scoreList.append(newRaceEntry) # Append this racer to the leaderboard
        self.sortScores(scoreList) # Sort our scores based off of the total time players took
        scoreList.pop() # Remove player who took the longest
        self.exportScores(self.raceScoresDict)



    def removeAfterXtime(self, raceId, recordId):
        if recordId == 0: # Daily
            addTime = 86400 # 24 Hours
        elif recordId == 1: # Weekly
            addTime = 604800
        else: # Best, DO NOT REMOVE BEST SCORES
            return

        scoreList = self.findRaceScoreList(raceId, recordId)

        tempIterScores = list(scoreList) # This is because of some weirdness that happens if we remove something from the original list when trying to loop through it aswell
        for race in tempIterScores:

            staticTimeStamp = race[2]
            expirationimeStamp = staticTimeStamp + addTime # 24 Hours out from whenever the timestamp was created for ending of race
            currentTime = time.time()

            if staticTimeStamp != 0: # A special case here, this is for the default racer ( Goofy ) So that it doesn't get inadvertantly removed.
                if currentTime >= expirationimeStamp: # If the present time is greater than the experiation, we will remove it
                    scoreList.remove(race) # Remove the race entry
                    self.setDefaultRacer(scoreList, raceId) # Append default racer in place of old entry
                    self.sortScores(scoreList)
                    self.exportScores(self.raceScoresDict)


    def findRaceScoreList(self, raceId, recordId): # Find specified race list we want
        wantedKey = (raceId, recordId)
        for raceKey in self.raceScoresDict:
            raceScores = self.raceScoresDict[raceKey]
    
            iterRaceId = raceKey[0]
            iterTitleId = raceKey[1]

            if raceKey == wantedKey:
                return raceScores



    def sortScores(self, scoreList):
        scoreList.sort(key=lambda player: player[1]) # Sort by time it took to complete race



