import math

from gestures.gesture import Gesture
import utils.zoom_helper as ShortkeyHelper
from gestures.hand_value import HandPoint, getHandPointByIndex


class OkHandGesture(Gesture):

    def __init__(self):
        self.initLastPositions(20)

    def check(self, left, right):
        self.addLastPosition(left, right)
        return self.checkOneHand(self.lastRightHandPositions) or self.checkOneHand(self.lastLeftHandPositions)

    def is_equal(self, x1, y1, x2, y2):
        TRESHOLD = 0.05
        dx = x1-x2
        dy = y1-y2
        dist = math.sqrt(dx*dx+dy*dy)

        if dist > TRESHOLD:
            return False
        else:
            return True

    def isOkHand(self, v):

        a = v.getPosition(HandPoint.THUMB_TIP)
        b = v.getPosition(HandPoint.INDEX_FINGER_TIP)

        if not self.is_equal(a.x, a.y, b.x, b.y):
            self.onInvalid()
            return False

        # 6 unter 12, 16, 20

        ysix = v.getPosition(getHandPointByIndex(6)).y
        other = [v.getPosition(getHandPointByIndex(i)).y for i in [12, 16, 20]]

        for yfinger in other:
            if yfinger > ysix:
                self.onInvalid()
                return False

        print(v.getPosition(getHandPointByIndex(2)).y - v.getPosition(getHandPointByIndex(6)).y)
        if v.getPosition(getHandPointByIndex(2)).y + 0.165 < v.getPosition(getHandPointByIndex(6)).y:
            self.onInvalid()
            return False

        self.onValid()
        return True

    def checkOneHand(self, positions):
        for v in positions:
            if not v:
                return False
            if not self.isOkHand(v):
                self.onInvalid()
                return False

        self.onValid()
        return True

    def onValid(self):
        self.initLastPositions(self.maxLastPositions)
        ShortkeyHelper.setOkHandState(True)
        print("ok hand")

    def onInvalid(self):
        ShortkeyHelper.setOkHandState(False)
