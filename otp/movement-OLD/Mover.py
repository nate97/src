from panda3d.core import *
from panda3d.core import LVector3f
from panda3d.ai import *
from direct.showbase import PythonUtil
from direct.distributed.ClockDelta import globalClockDelta
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from direct.task import Task
from otp.movement.PyVec3 import PyVec3

import random
import __builtin__

class Mover():
    notify = DirectNotifyGlobal.directNotify.newCategory('Mover')
    SerialNum = 0
    Profile = 0
    render = NodePath('render')
    nullTargetNodePath = NodePath('nullTargetNodepath')

    def __init__(self, objNodePath, fwdSpeed = 1, rotSpeed = 1):
        print ("Initalizng pet")

        self.serialNum = Mover.SerialNum
        Mover.SerialNum += 1
        self.VecType = Vec3
        self.impulses = {}

        # NEW VARIABLES
        self.petNodePath = objNodePath
        self.targetNodePath = NodePath('targetNodepath')

        self.petLocked = False
        self.petMode = 'unstick'
        self._sadMult = 0.3
        self.fwdSpeed = fwdSpeed
        self.sadFwdSpeed = self.fwdSpeed * self._sadMult

        # Temporary garbage
        self.taskOn = 0

        self.setAI()


    def destroy(self):
        for name, impulse in self.impulses.items():
            Mover.notify.debug('removing impulse: %s' % name)
            self.removeImpulse(name)



    def addImpulse(self, name, impulse):
        self.impulses[name] = impulse
        impulse._setMover(self)



    def removeImpulse(self, name):
        if name not in self.impulses:
            Mover.notify.warning("Mover.removeImpulse: unknown impulse '%s'" % name)
            return
        self.impulses[name]._clearMover(self)
        del self.impulses[name]



    def processImpulses(self, dt = 1):
        self.dt = dt
        if self.dt == -1.0:
            time = globalClockDelta.getRealNetworkTime()
            self.dt = time - dt

        for impulse in self.impulses.values():
            impulse._process(self.dt)



    def getCollisionEventName(self):
        return 'moverCollision-%s' % self.serialNum



    def move(self, dt = -1, profile = 0):
        if Mover.Profile and not profile:

            def func(doMove = self.move):
                for i in xrange(10000):
                    doMove(dt, profile=1)

        self.processImpulses(dt)
        self.integrate()



    def integrate(self):
        try:
            # Do this once
            if self.taskOn == 0:
                taskMgr.add(self.AIUpdate,"AIUpdate")
                self.taskOn = 1
 
        except:
            pass

    def AIUpdate(self, task):
        try:
            self.AIworld.update()
            self.petCollisions()
            self.petRotationFix()
        except:
            pass


        return Task.cont



    def petCollisions(self):
        try:
            # This piece of code is to check the distance between the toon and pet,
            # in order to make sure the doodle does not collide with the toon.
            xToon = int(self.targetNodePath.getX())
            xPet = int(self.petNodePath.getX())
            yToon = int(self.targetNodePath.getY())
            yPet = int(self.petNodePath.getY())

            xDifference = abs(xToon - xPet) # Get the absolute value because we don't care about exact position in the environment
            yDifference = abs(yToon - yPet)

            stopDistance = 2 # Distance the pet should stop before reaching toon

            if xDifference <= stopDistance and yDifference <= stopDistance: # If the distance between toon and pet is 2; stop moving
                self.AIbehaviors.pauseAi('all') # Stop the pet from moving

        except:
            pass


    def petRotationFix(self):
        if self.petMode != 'stick':
            currentHPet = self.petNodePath.getH()
            correctedHPet = currentHPet - 180
            self.petNodePath.setH(correctedHPet)



    def setAI(self):
        #Creating AI World

        self.AIworld = AIWorld(Mover.render)
 
        self.AIchar = AICharacter("petNodePath", self.petNodePath, 50, 10, 25)
        self.AIworld.addAiChar(self.AIchar)
        self.AIbehaviors = self.AIchar.getAiBehaviors()



    def setPetAIMode(self, petMode, target = nullTargetNodePath):
        self.petMode = petMode
        self.targetNodePath = target # This is in case we need to do something else with the target later

        self.AIbehaviors.pauseAi('all') # Before we do any state changes, pause the AI

        if self.petMode == 'stick': # Locks pet and doesn't allow movement
            self.petLocked = True
            self.AIbehaviors.pauseAi('all')

        elif self.petMode == 'unstick':
            self.petLocked = False

        elif self.petMode == 'chase' and self.petLocked == False: # This makes the pet continue to follow a moving object
            self.AIbehaviors.pursue(target)

        elif self.petMode == 'static_chase' and self.petLocked == False: # This makes the pet go to a single spot
            self.AIbehaviors.seek(target)

        elif self.petMode == 'wander' and self.petLocked == False:
            self.AIbehaviors.wander(10, 0, 50, 1.0)

        elif self.petMode == 'flee' and self.petLocked == False:
            self.AIbehaviors.flee(chaser, 20, 20)



    # Pet's walking speed
    def setFwdSpeed(self, speed):
        self.fwdSpeed = speed
        self.AIchar.setMaxForce(self.fwdSpeed) 


