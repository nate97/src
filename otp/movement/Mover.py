from panda3d.core import *
from panda3d.core import LVector3f
from direct.showbase import PythonUtil
from direct.distributed.ClockDelta import globalClockDelta
from direct.interval.IntervalGlobal import *
from direct.directnotify import DirectNotifyGlobal
from otp.movement.PyVec3 import PyVec3

import random
import __builtin__

class Mover():
    notify = DirectNotifyGlobal.directNotify.newCategory('Mover')
    SerialNum = 0
    Profile = 0
    Pstats = 1
    PSCCpp = 'App:Show code:moveObjects:MoverC++'
    PSCPy = 'App:Show code:moveObjects:MoverPy'
    PSCInt = 'App:Show code:moveObjects:MoverIntegrate'

    def __init__(self, objNodePath, fwdSpeed = 1, rotSpeed = 1):
        self.serialNum = Mover.SerialNum
        Mover.SerialNum += 1
        self.VecType = Vec3
        self.impulses = {}
        if Mover.Pstats:
            self.pscCpp = PStatCollector(Mover.PSCCpp)
            self.pscPy = PStatCollector(Mover.PSCPy)
            self.pscInt = PStatCollector(Mover.PSCInt)

        self.objNodePath = objNodePath
        self.fwdSpeed = fwdSpeed
        self.rotSpeed = rotSpeed
        self.rotVel = None
        self.vel = None
        self.dt = 1
        self.nodePath = None


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

            __builtin__.func = func
            PythonUtil.startProfile(cmd='func()', filename='profile', sorts=['cumulative'], callInfo=0)
            del __builtin__.func
            return
        if Mover.Pstats:
            self.pscCpp.start()
        self.processImpulses(dt)
        if Mover.Pstats:
            self.pscCpp.stop()
            self.pscPy.start()

        if Mover.Pstats:
            self.pscPy.stop()
            self.pscInt.start()
        self.integrate()
        if Mover.Pstats:
            self.pscInt.stop()



    def integrate(self):
        if self.nodePath is not None:
            self.walkToPoint()



    def walkToPoint(self):
        currentPos = self.objNodePath.getPos()
        newPos = self.nodePath.getPos()

        dist = Vec3(currentPos - newPos).length()

        self.__seq = Sequence(Func(self.objNodePath.lookAt, newPos), self.objNodePath.posInterval(dist / self.fwdSpeed, newPos, currentPos))
        self.__seq.start()



    def setNodePath(self, np):
        self.nodePath = np

    def getNodePath(self):
        return self.nodePath



    def setFwdSpeed(self, speed):
        self.fwdSpeed = speed
        
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



