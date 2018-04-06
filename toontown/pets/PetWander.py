"""from panda3d.core import *
from direct.showbase.PythonUtil import reduceAngle, randFloat, normalDistrib
from direct.showbase import DirectObject
from toontown.pets.PetChase import PetChase
from toontown.pets import PetConstants

class PetWander(PetChase, DirectObject.DirectObject):

    def __init__(self, minDist = 5.0, moveAngle = 20.0):
        self.movingTarget = hidden.attachNewNode('petWanderTarget')
        PetChase.__init__(self, self.movingTarget, minDist, moveAngle)
        self.targetMoveCountdown = 0
        self.collEvent = None
        self.gotCollision = False
        return

    def __ignoreCollisions(self):
        if self.collEvent is not None:
            self.ignore(self.collEvent)
            self.collEvent = None
        return

    def _setMover(self, mover):
        PetChase._setMover(self, mover)
        self.mover = mover
        #self.__ignoreCollisions()
        self.collEvent = mover.getCollisionEventName()
        print self.collEvent
        self.accept(self.collEvent, self._handleCollision)

    def _handleCollision(self, collEntry):
        print "Wander collision"
        self.gotCollision = True
        self.movingTarget.setPos(self.lookAtNode.getPos())
        self.targetMoveCountdown *= 0.5

    def destroy(self):
        self.__ignoreCollisions()
        self.movingTarget.removeNode()
        del self.movingTarget

    def _process(self, dt):
        self.targetMoveCountdown -= dt
        if self.targetMoveCountdown <= 0.0:
            distance = normalDistrib(3.0, 30.0)
            heading = normalDistrib(-(90 + 45), 90 + 45)
            if self.gotCollision:
                self.gotCollision = False
                heading = heading + 180
            target = PetChase.getTarget(self)
            target.setPos(self.lookAtNode.getPos())
            target.setH(target, heading)
            target.setY(target, distance)
            duration = distance / self.mover.getFwdSpeed()
            self.targetMoveCountdown = duration * randFloat(1.2, 3.0)

            self.mover.setInterestTarget(target)

        PetChase.processWander(self, dt)"""








from panda3d.core import *
from direct.showbase.PythonUtil import reduceAngle, randFloat, normalDistrib
from direct.showbase import DirectObject
from toontown.pets.PetChase import PetChase
from toontown.pets import PetConstants

class PetWander(PetChase, DirectObject.DirectObject):

    def __init__(self, minDist = 5.0, moveAngle = 20.0):
        self.movingTarget = hidden.attachNewNode('petWanderTarget')
        PetChase.__init__(self, self.movingTarget, minDist, moveAngle)
        self.xx = 1
        self.targetMoveCountdown = 0
        self.collEvent = None
        self.gotCollision = False
        return

    def __ignoreCollisions(self):
        if self.collEvent is not None:
            self.ignore(self.collEvent)
            self.collEvent = None
        return

    def _setMover(self, mover):
        PetChase._setMover(self, mover)
        self.mover = mover
        #self.__ignoreCollisions()
        self.collEvent = mover.getCollisionEventName()
        print self.collEvent
        self.accept(self.collEvent, self._handleCollision)

    def _handleCollision(self, collEntry):
        print "Wander collision"
        self.gotCollision = True
        self.movingTarget.setPos(self.lookAtNode.getPos())
        self.targetMoveCountdown *= 0.5

    def destroy(self):
        self.__ignoreCollisions()
        self.movingTarget.removeNode()
        del self.movingTarget

    def _process(self, dt):

        if self.xx == 1:
            self.mover.setWander()

            self.xx = 0
        PetChase.processWander(self, dt)










