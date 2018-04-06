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

    def __init__(self, objNodePath, fwdSpeed = 1, rotSpeed = 1):
        print ("Initalizng pet")
        self.serialNum = Mover.SerialNum
        Mover.SerialNum += 1
        self.VecType = Vec3
        self.impulses = {}

        self.objNodePath = objNodePath
        self.moverTarget = None

        self.fwdSpeed = fwdSpeed
        self.rotSpeed = rotSpeed

        self._sadMult = 0.3
        self.sadFwdSpeed = self.fwdSpeed * self._sadMult
        self.sadRotSpeed = self.rotSpeed * self._sadMult

        self.rotVel = None
        self.vel = None

       
        self.enabled = 0
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


    def setAI(self):
        #Creating AI World

        self.AIworld = AIWorld(Mover.render)
 
        self.AIchar = AICharacter("objNodePath", self.objNodePath, 50, 10, 25)
        self.AIworld.addAiChar(self.AIchar)
        self.AIbehaviors = self.AIchar.getAiBehaviors()
        


    def AIUpdate(self, task):
        try:
            self.AIworld.update()
            self.objNodePath.lookAt(self.moverTarget)
        except:
            pass
        return Task.cont





    def setInterestTarget(self, moverTarget):
        self.moverTarget = moverTarget
        self.AIbehaviors.pursue(moverTarget)



    def getInterestTarget(self):
        return self.moverTarget



    def setStaticTarget(self, moverTarget):
        self.stopMovingObj()
        self.moverTarget = moverTarget
        self.AIbehaviors.seek(moverTarget)


    def setWander(self):
        self.stopMovingObj()
        self.AIbehaviors.wander(10, 0, 50, 1.0)


    def stopMovingObj(self):
        self.AIbehaviors.pauseAi('all')


    def setFwdSpeed(self, speed):
        self.fwdSpeed = speed
        self.AIchar.setMaxForce(self.fwdSpeed) 

    def getFwdSpeed(self):
        return self.fwdSpeed
        
    def setRotSpeed(self, speed):
        self.rotSpeed = speed

    def getRotSpeed(self):
        return self.rotSpeed







    def addRotShove(self, rotVel):
        self.rotVel = rotVel

    def addShove(self, vel):
        self.vel = vel


