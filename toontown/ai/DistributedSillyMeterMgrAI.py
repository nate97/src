from direct.directnotify import DirectNotifyGlobal
from toontown.ai.DistributedPhaseEventMgrAI import DistributedPhaseEventMgrAI

class DistributedSillyMeterMgrAI(DistributedPhaseEventMgrAI):
    notify = DirectNotifyGlobal.directNotify.newCategory("DistributedSillyMeterMgrAI")
