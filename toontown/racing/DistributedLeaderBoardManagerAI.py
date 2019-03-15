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


        # Genres
        Speedway = 0
        Rural = 1
        Urban = 2

        # Record IDs
        Daily = 0
        Weekly = 1
        AllTime = 2

        LeaderBoard_Name = 'Racer Name'

        # Record text
        LeaderBoard_Daily = 'Daily Scores'
        LeaderBoard_Weekly = 'Weekly Scores'
        LeaderBoard_AllTime = 'All Time Best Scores'
        self.RecordPeriodStrings = [LeaderBoard_Daily, LeaderBoard_Weekly, LeaderBoard_AllTime]

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


        self.LBSubscription = {
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

        self.createCSV()

        #print self.recordLists


        self.stadiumCount = 0
        self.ruralCount = 0
        self.cityCount = 0
        self.countIteratorList = [self.stadiumCount, self.ruralCount, self.cityCount]

        self.stadiumDict = self.createBoardDict(0) # Will be created for each leaderboard
        self.ruralDict = self.createBoardDict(1) # Will be created for each leaderboard
        self.urbanDict = self.createBoardDict(2) # Will be created for each leaderboard
        self.allDicts = [self.stadiumDict, self.ruralDict, self.urbanDict]

        self.stadiumBoard = None
        self.ruralBoard = None
        self.urbanBoard = None



    def createCSV(self):
        if not os.path.exists(self.fullPath):
            os.mkdir(self.fullPath)
            self.writeToCSV(self.recordLists)

        else:

            if not os.path.exists(self.fullPath + self.fullName):
                self.writeToCSV(self.recordLists)
            else:

                reader = csv.reader(open(self.fullPath + self.fullName, 'r'))
                previousScores = {}
                for row in reader:
                    key, value = row

                    key = ast.literal_eval(key)
                    value = ast.literal_eval(value)

                    previousScores[key] = value

                del reader

                self.recordLists = previousScores







    def writeToCSV(self, scoreList):
        w = csv.writer(open(self.fullPath + self.fullName, 'w'))
        for key, val in scoreList.items():
            w.writerow([key, val])
        del w # Close



    def setBoard(self, genre, board): # This function allows us to send the leaderboard over to us so we can manage it directly
        if genre == 0: # Stadium
            self.stadiumBoard = board
        elif genre == 1: # Rural
            self.ruralBoard = board
        elif genre == 2: # Urban
            self.urbanBoard = board


        # SHOULDN'T BE HERE, IMPORTANT!!!
        if self.ruralBoard: # If all boards have been generated initiate tasks
            self.cycleLeaderBoard()



    def iterateManager(self, genre, leaderBoard):
        records = []

        currentTracks = self.LBSubscription[genre]
   
        if self.countIteratorList[genre] > 11: # If we go over 11 tracks, reset
            self.countIteratorList[genre] = 0

        trackKey = currentTracks[self.countIteratorList[genre]]
        trackId = trackKey[0]
        recordId = trackKey[1]

        iterCount, curRaceTrackScores = self.iterateThroughBoard(genre, self.countIteratorList[genre], trackKey)
        self.countIteratorList[genre] = iterCount



        #######################################################################################
        ########################### PROBABLY SHOULD BE NEW FUNCTION ###########################
        #######################################################################################

        records = curRaceTrackScores[4] # IMPORTANT!!! Our current list of player records
        #print records

        # Sort records from least amount of time to greatest
        records = self.sortScores(records)


        # Purge expired scores!!!
        if records != [] and recordId != 2: # If our records list is NOT empty...
            # Remove old stuff from records
            records = self.removeAfterXtime(genre, trackId, recordId)
        else:
            pass
            # Append our DEFAULT GOOFY SCORES here! """   




        trackTitle = self.KartRace_TrackNames[trackId] # Text
        recordTitle = self.RecordPeriodStrings[recordId] # Text

        ourTuple = (trackTitle, recordTitle, records)

        # SEND BACK TO CORRECT BOARD
        leaderBoard.setDisplay(ourTuple) # SHOULD BE MOVED TO IT'S OWN FUNCTION!!!



    def iterateThroughBoard(self, genre, iterCount, trackKey):
        genreDict = self.allDicts[genre]
        curRaceTrackScores = genreDict[trackKey]
        iterCount = iterCount + 1
        return iterCount, curRaceTrackScores
        


    def sendDisplayToLeaderboard(self, genre):
        pass



    def createBoardDict(self, genre = 1):
        boardDict = {}

        something = self.LBSubscription[genre]
        
        for trackrecord in something:

            raceId = trackrecord[0]
            recordTitleId = trackrecord[1]
    
            raceTitle = self.KartRace_TrackNames[raceId]
            recordTitle = self.RecordPeriodStrings[recordTitleId]


            currentTuple = (raceId, recordTitleId)

            scoreList = self.recordLists[currentTuple]

            identifyTuple = (raceId, recordTitleId)
            completedList = [raceId, recordTitleId, raceTitle, recordTitle, scoreList] # IMPORTANT!!! THIS IS WHERE WE'RE APPENDING NEW STUFF

            boardDict[identifyTuple] = completedList

        return boardDict



    def specificListProxy(self, raceId, recordId, av = 0, totalTime = 0, timeStamp = 0): # This is a proxy for a race to append a winner, will need more data
        # Continue from here!!! ######################################

        # Function to find requiredTime called here!!!
        #requiredTime = 5

        #if totalTime >= requiredTime: # Return if totalTime exceeds minimum requirement!!!
            #return


        # Go through all genre's and track titles


        for genre in range(0,3): # iterate over all three genres
            try:
                self.findSpecificList(raceId, recordId, genre, av, totalTime, timeStamp)
            except:
                pass
            


    def findSpecificList(self, raceId, recordId, genre, av, totalTime, timeStamp): # Finds specific list we want (NEVER CALL THIS DIRECTLY ALWAYS USE PROXY)
        wantedTuple = (raceId, recordId)

        for raceTracks in self.LBSubscription[genre]: # genre is in square brackets
            iterRaceId = raceTracks[0]
            iterTitleId = raceTracks[1]

            genreDict = self.allDicts[genre]

            currentLists = genreDict[raceTracks]
            iterRaceText = currentLists[0]
            iterTitleText = currentLists[1]     
    

            iterateTuple = (iterRaceId, iterTitleId)

            if iterateTuple == wantedTuple:

                recordList = currentLists[4] # IMPORTANT LIST FOR THIS TRACK, AND PARTICULAR RECORDID

                newEntry = (av, totalTime, timeStamp)
                recordList.append(newEntry) # Append to correct racetrack and record type list

                self.writeToCSV(self.recordLists)



    def removeAfterXtime(self, genre, raceId, recordId):
        if recordId == 0: # Daily
            addTime = 86400 # 24 Hours
        elif recordId == 1: # Weekly
            addTime = 604800

        wantedTuple = (raceId, recordId)

        for raceTracks in self.LBSubscription[genre]: # genre is in square brackets

            genreDict = self.allDicts[genre]
            currentLists = genreDict[raceTracks]

            iterRaceId = raceTracks[0]
            iterTitleId = raceTracks[1]
            iterateTuple = (iterRaceId, iterTitleId)

            if iterateTuple == wantedTuple:
   
                recordList = currentLists[4] # IMPORTANT LIST FOR THIS TRACK, AND PARTICULAR RECORDID
                for players in recordList:
                    print players
                    staticTimeStamp = players[2]
                    futureTimeStamp = staticTimeStamp + addTime # 24 Hours out from whenever the timestamp was created for ending of race
                    currentTime = time.time()

                    if currentTime >= futureTimeStamp:
                        recordList.remove(players)
                        #print "REMOVED"

        self.writeToCSV(self.recordLists)
        return recordList



    def sortScores(self, scores):
        sortedScores = sorted(scores, key=lambda player: player[1])   # sort by time it took to complete race
        return sortedScores



    def cycleLeaderBoard(self, task=None):
        self.iterateManager(0, self.stadiumBoard)
        self.iterateManager(1, self.ruralBoard)
        self.iterateManager(2, self.urbanBoard)

        taskMgr.doMethodLater(10, self.cycleLeaderBoard, 'cycleLeaderBoards')



