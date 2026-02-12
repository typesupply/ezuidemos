"""
Call callbacks when specific key down/up
events happen in a window.

Relevant Documentation:
- EZWindow: https://typesupply.github.io/ezui/windows.html
"""

import ezui

class DemoWindow(ezui.WindowController):

    def build(self):
        self.panel = None
        content = """
        Try these key combinations:
        t
        t shift
        t command shift
        """
        descriptionData = dict()
        self.w = ezui.EZWindow(
            content=content,
            descriptionData=descriptionData,
            controller=self
        )
        self.w.addKeyDownBinding(
            character="t",
            callback=self.keyDownTCallback
        )
        self.w.addKeyDownBinding(
            character="t",
            modifiers=["shift"],
            callback=self.keyDownTShiftCallback
        )
        self.w.addKeyDownBinding(
            character="t",
            modifiers=["shift", "command"],
            callback=self.keyDownTShiftCommandCallback
        )
        self.w.addKeyUpBinding(
            character="t",
            callback=self.keyUpTCallback
        )
        self.w.addKeyUpBinding(
            character="t",
            modifiers=["shift"],
            callback=self.keyUpTShiftCallback
        )
        self.w.addKeyUpBinding(
            character="t",
            modifiers=["shift", "command"],
            callback=self.keyUpTShiftCommandCallback
        )

    def started(self):
        self.w.open()

    def keyDownTCallback(self, sender):
        print("down: t")

    def keyDownTShiftCallback(self, sender):
        print("down: t shift")

    def keyDownTShiftCommandCallback(self, sender):
        print("down: t shift command")

    def keyUpTCallback(self, sender):
        print("up: t")

    def keyUpTShiftCallback(self, sender):
        print("up: t shift")

    def keyUpTShiftCommandCallback(self, sender):
        print("up: t shift command")

DemoWindow()