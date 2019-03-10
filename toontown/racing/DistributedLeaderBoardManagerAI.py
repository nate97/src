from direct.directnotify.DirectNotifyGlobal import *
from direct.distributed import DistributedObjectAI



class DistributedLeaderBoardManagerAI(DistributedObjectAI.DistributedObjectAI):
    notify = directNotify.newCategory('LeaderBoardManagerAI')

    def __init__(self, air):

        self.Speedway = 0
        self.Rural = 1
        self.Urban = 2

        self.boards = {} # FOR FINDING GENERATED BOARDS, SPEEDWAY, RURAL, URBAN
    
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

        self.speedway1 = []
        self.speedway1rev = []
        self.speedway2 = []
        self.speedway2rev = []

        self.rural1 = []
        self.rural1rev = []
        self.rural2 = []
        self.rural2rev = []

        self.urban1 = []
        self.urban1rev = []
        self.urban2 = []
        self.urban2rev = []

        self.raceIdToScoreList = {
            RT_Speedway_1: self.speedway1, RT_Speedway_1_rev: self.speedway1rev, RT_Speedway_2: self.speedway2, RT_Speedway_2_rev: self.speedway2rev,
            RT_Rural_1: self.rural1, RT_Rural_1_rev: self.rural1rev, RT_Rural_2: self.rural2, RT_Rural_2_rev: self.rural2rev,
            RT_Urban_1: self.urban1, RT_Urban_1_rev: self.urban1rev, RT_Urban_2: self.urban2, RT_Urban_2_rev: self.urban2rev
            }



    def appendBoards(self, board):
        bType = board.getType()

        if bType == "stadium":
            boardType = self.Speedway

        elif bType == "country":
            boardType = self.Rural

        elif bType == "city":
            boardType = self.Urban

        self.boards[boardType] = board



    def getBoards(self):
        return self.boards



    def setScore(self, trackId, genre, time, av, timeStamp): # Racetrack, genre IE speedway rural etc, time, avatar ID
        print "LEADERBOARD MANAGER"

        currentBoard = self.boards[genre]

        boardTuple = (trackId, genre, time, av, timeStamp)

        self.scoreManager(boardTuple)



    def scoreManager(self, boardTuple):

        trackId = boardTuple[0]

        currentList = self.raceIdToScoreList[trackId]

        currentList.append(boardTuple)

        print self.raceIdToScoreList



    def getAllScores(self):
        return self.raceIdToScoreList

