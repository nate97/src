from panda3d.core import *
from direct.showbase.PythonUtil import reduceAngle
from otp.movement import Impulse
from otp.movement.PyVec3 import PyVec3
import math

import inspect

class PetChase(Impulse.Impulse):

    def __init__(self, target = None, minDist = None, moveAngle = None):
        Impulse.Impulse.__init__(self)
        self.lookAtNode = NodePath('lookatNode')
        self.target = target
        return



    def setTarget(self, target):
        try:
            self.mover.setInterestTarget(target)
        except:
            pass
        self.target = target



    def setStaticTarget(self, target):
        self.mover.setStaticTarget(stationaryNode)



    def getTarget(self):
        return self.target



    def destroy(self):
        self.lookAtNode.removeNode()
        del self.lookAtNode
        del self.target



    def _setMover(self, mover):
        Impulse.Impulse._setMover(self, mover)
        self.lookAtNode.reparentTo(self.nodePath)



    def _clearMover(self, mover):
        print "Cleared CHASE???"
        self.mover.stopMovingObj()
        stationaryNode = NodePath('stationary_node')
        stationaryNode.setPos(self.target.getPos())
        self.mover.setInterestTarget(stationaryNode)



    def processWander(self, dt):
        Impulse.Impulse._process(self, dt)



    def _process(self, dt):
        Impulse.Impulse._process(self, dt)

        target = self.target

        self.mover.setInterestTarget(target)




