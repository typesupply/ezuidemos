"""
Define a callback for when a slider's editing ends
in adddition to continuous updates during editing.
This uses a coalescer like the one in Subscriber
to delay being notified by the slider's continuous
callbacks. This doesn't definitively tell you when
the slider has ended, but it's a close approximation.

Discord discussion: https://discord.com/channels/1052516637489766411/1076154772362641539/1157070115922251926
"""

import AppKit
import ezui

class Demo(ezui.WindowController):

    def build(self):
        self.coalescer = Coalescer(
            callback=self.sliderEndedCallback,
            delay=0.1
        )
        content = """
        ---X--- @slider
        """
        descriptionData = dict(
            slider=dict(
                continuous=True
            )
        )
        self.w = ezui.EZWindow(
            content=content,
            descriptionData=descriptionData,
            controller=self,
            size=(500, "auto")
        )

    def started(self):
        self.w.open()

    def windowWillClose(self, sender):
        self.coalescer.stop()
        self.coalescer = None

    def sliderCallback(self, sender):
        self.coalescer.restart()
        print("sliderCallback")

    def sliderEndedCallback(self, coalescer):
        print("sliderEndedCallback")


class Coalescer:

    def __init__(self, callback, delay, info={}):
        self.info = info
        self.callback = callback
        self.delay = delay
        self.timer = None

    def appendLowLevelEvent(self, lowLevelEvent):
        self.lowLevelEvents.append(lowLevelEvent)

    def _makeTimer(self):
        self.timer = AppKit.NSTimer.timerWithTimeInterval_target_selector_userInfo_repeats_(
            self.delay,
            self,
            "timerFire:",
            None,
            False
        )
        runloop = AppKit.NSRunLoop.mainRunLoop()
        runloop.addTimer_forMode_(self.timer, AppKit.NSRunLoopCommonModes)

    def timerFire_(self, timer):
        self.fire()

    def start(self):
        if not self.delay:
            self.fire()
        else:
            self._makeTimer()

    def restart(self):
        if self.timer is not None:
            self.timer.invalidate()
        self.start()

    def stop(self):
        if self.timer is None:
            return
        if self.timer.isValid():
            self.timer.invalidate()

    def fire(self):
        self.stop()
        self.callback(self)
        self.timer = None

Demo()