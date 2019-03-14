from direct.directnotify.DirectNotifyGlobal import *
from direct.distributed import DistributedObjectAI



class DistributedLeaderBoardManagerAI(DistributedObjectAI.DistributedObjectAI):
    notify = directNotify.newCategory('LeaderBoardManagerAI')

    def __init__(self, air):

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
        #self.countIteratorList[genre] # We have to directly call this variable because I can't think of how todo this better right now

        currentTracks = self.LBSubscription[genre]
        
        if self.countIteratorList[genre] > 11: # If we go over 11 tracks, reset
            self.countIteratorList[genre] = 0

        trackKey = currentTracks[self.countIteratorList[genre]]
        
        iterCount, curRaceTrackScores = self.iterateThroughBoard(genre, self.countIteratorList[genre], trackKey)
        self.countIteratorList[genre] = iterCount

        print curRaceTrackScores

        # SEND BACK TO CORRECT GENRE BOARD
        #print trackKey

        records = curRaceTrackScores[4]
        
        trackTitle = self.KartRace_TrackNames[trackKey[0]]
        recordTitle = self.RecordPeriodStrings[trackKey[1]]


        print trackTitle
        print recordTitle
        print records

        ourTuple = (trackTitle, recordTitle, records)

        leaderBoard.setDisplay(ourTuple)





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

            #print ""
            #print raceTitle
            #print recordTitle

            currentTuple = (raceId, recordTitleId)

            scoreList = self.recordLists[currentTuple]

            identifyTuple = (raceId, recordTitleId)
            completedTuple = (raceId, recordTitleId, raceTitle, recordTitle, scoreList)


            boardDict[identifyTuple] = completedTuple

        return boardDict



    def specificListProxy(self, raceId, recordTitle, av = 0, totalTime = 0, timeStamp = 0): # This is a proxy for a race to append a winner, will need more data
        for genre in range(0,3): # iterate over all three genres
            try:
                self.findSpecificList(raceId, recordTitle, genre, av, totalTime, timeStamp)
            except:
                pass
            


    def findSpecificList(self, raceId, recordTitle, genre, av, totalTime, timeStamp): # Finds specific list we want (NEVER CALL THIS DIRECTLY ALWAYS USE PROXY)
        wantedTuple = (raceId, recordTitle)

        for raceTracks in self.LBSubscription[genre]: # genre is in square brackets

            iterRaceId = raceTracks[0]
            iterTitleId = raceTracks[1]

            genreDict = self.allDicts[genre]

            currentLists = genreDict[raceTracks]
            iterRaceText = currentLists[0]
            iterTitleText = currentLists[1]     
    

            iterateTuple = (iterRaceId, iterTitleId)

            if iterateTuple == wantedTuple:

                recordList = currentLists[4] # IMPORTANT LIST FOR THIS TRACK, AND PARTICULAR RECORDTITLE

                newEntry = (av, totalTime, timeStamp)
                recordList.append(newEntry) # Append to correct racetrack and record type list



    def cycleLeaderBoard(self, task=None):
        self.iterateManager(0, self.stadiumBoard)
        self.iterateManager(1, self.ruralBoard)
        self.iterateManager(2, self.urbanBoard)

        taskMgr.doMethodLater(10, self.cycleLeaderBoard, 'cycleLeaderBoards')



