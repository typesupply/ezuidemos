"""
Open a popover for a specific button.

Relevant Documentation:
    - Popover: https://typesupply.github.io/ezui/windows.html#ezpopover
"""

import ezui

class Demo(ezui.WindowController):

    def build(self):
        content = """
        (Open Popover) @openPopoverButton
        """
        self.w = ezui.EZWindow(
            title="Demo",
            content=content,
            controller=self
        )

    def started(self):
        self.w.open()

    def openPopoverButtonCallback(self, sender):
        button = self.w.getItem("openPopoverButton")
        DemoPopover(button)


class DemoPopover(ezui.WindowController):

    def build(self, parent):
        content = """
        This is Popover content.
        """
        self.w = ezui.EZPopover(
            content=content,
            parent=parent,
            controller=self
        )

    def started(self):
        self.w.open()

Demo()