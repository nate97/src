from pandac.PandaModules import * 
from direct.gui import DirectGuiGlobals
from direct.gui.DirectGui import *



class AdminPane():

    def __init__(self):
        print 'Initalization'
        self.loadGUI()



    def loadGUI(self):
        print 'Do nothing'
        self.bFriendsList = DirectButton(pos=(0, 0, -0.2), parent=base.a2dTopCenter, scale=(0.05), text='Set Ghost', command=self.sendAdminCMD)
        


    def sendAdminCMD(self):
        print 'Set ghost'

        base.talkAssistant.sendOpenTalk('~ghost')


