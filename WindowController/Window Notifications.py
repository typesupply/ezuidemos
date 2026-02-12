"""
Make a WindowController that notifies its subclass
when the window is selected, deselected, closed,
resized or moved.

Relevant Documentation:
    - WindowController: https://typesupply.github.io/ezui/controllers.html#windowcontroller
"""

import ezui

class Demo(ezui.WindowController):

    def build(self):
        content = """
        Window is not yet open. @status
        """
        descriptionData = {}
        self.w = ezui.EZWindow(
            content=content,
            descriptionData=descriptionData,
            controller=self,
            size=(500, 500),
            minSize=(300, 300)
        )

    def started(self):
        self.w.open()

    def windowWillClose(self, sender):
        print("Window will close.")

    def windowDidMove(self, sender):
        self.w.setItemValue("status", "Window moved.")

    def windowDidResize(self, sender):
        self.w.setItemValue("status", "Window changed size.")

    def windowDidSelect(self, sender):
        self.w.setItemValue("status", "Window is selected.")

    def windowDidDeselect(self, sender):
        self.w.setItemValue("status", "Window is not selected.")

Demo()