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
        T
        T shift
        T command shift
        """
        descriptionData = dict()
        self.w = ezui.EZWindow(
            content=content,
            descriptionData=descriptionData,
            controller=self
        )
        self.w.addKeyBinding(
            character="T",
            callback=self.keyTCallback,
            title="Documentation for T."
        )
        self.w.addKeyBinding(
            character="T",
            modifiers=["shift"],
            callback=self.keyTShiftCallback,
            title="Documentation for T + shift."
        )
        self.w.addKeyBinding(
            character="T",
            modifiers=["shift", "command"],
            callback=self.keyTShiftCommandCallback,
            title="Documentation for T + shift + command."
        )

    def started(self):
        self.w.open()

    def keyTCallback(self, sender):
        print("down: t")

    def keyTShiftCallback(self, sender):
        print("down: t shift")

    def keyTShiftCommandCallback(self, sender):
        print("down: t shift command")

DemoWindow()