from pandac.PandaModules import * 
from direct.gui.DirectGui import *
from direct.gui.DirectGui import DirectFrame
from direct.gui import DirectGuiGlobals




class AdminPane():

    def __init__(self):
        print 'Initalization'
        self.loadGUI()



    def loadGUI(self):
        print 'Load admin gui'


        adminFrame = DirectFrame(parent=base.a2dTopCenter, frameColor=(1, 1, 1, 0.2),
                            frameSize=(-0.2, 0.2, -0.2, 0.2),
                            pos=(0, 0, -0.4))            


        self.bFriendsList = DirectButton(parent=adminFrame, scale=(0.05), text='Set Ghost', command=self.sendAdminCMD)
        


    def sendAdminCMD(self):
        print 'Set ghost'

        base.talkAssistant.sendOpenTalk('~ghost')

