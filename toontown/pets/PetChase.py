from panda3d.core import *
from direct.showbase.PythonUtil import reduceAngle
from otp.movement import Impulse
from otp.movement.PyVec3 import PyVec3
import math

import inspect

class PetChase(Impulse.Impulse):

    def __init__(self, target = None, minDist = None, moveAngle = None):
        Impulse.Impulse.__init__(self)
        self.targetNode = target
        self.lookAtNode = NodePath('lookatNode')
        return



    def setTarget(self, target):
        try:
            self.mover.setInterestTarget(target)
        except:
            pass
        self.targetNode = target



    def setStaticTarget(self, target):
        self.mover.setStaticTarget(stationaryNode)



    def getTarget(self):
        return self.targetNode



    def destroy(self):
        self.lookAtNode.removeNode()
        del self.lookAtNode
        del self.targetNode



    def _setMover(self, mover):
        Impulse.Impulse._setMover(self, mover)
        self.lookAtNode.reparentTo(self.targetNode)


    def _clearMover(self, mover):
        print "Cleared CHASE???"
        self.mover.stopMovingObj()



    def processWander(self, dt):
        Impulse.Impulse._process(self, dt)



    def _process(self, dt):
        Impulse.Impulse._process(self, dt)

        target = self.lookAtNode
    
        self.mover.setInterestTarget(target)



