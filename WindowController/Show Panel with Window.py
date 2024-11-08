"""
Make a panel visible only when a window has focus.

This is done by using the vanilla window bindings
that aren't (yet?) exposed in ezui.

Relevant Documentation:
- EZWindow and EZPanel: https://typesupply.github.io/ezui/windows.html
- Window.bind: https://vanilla.robotools.dev/en/latest/objects/Window.html#vanilla.Window.bind
"""

import ezui

class DemoWindow(ezui.WindowController):

    def build(self):
        self.panel = None
        content = """
        main: no @mainLabel
        key: no @keyLabel
        """
        descriptionData = dict()
        self.w = ezui.EZWindow(
            content=content,
            descriptionData=descriptionData,
            controller=self,
            size=(200, 200)
        )
        self.w.bind("became main", self.windowBecameMainCallback)
        self.w.bind("resigned main", self.windowResignedMainCallback)
        self.w.bind("became key", self.windowBecameKeyCallback)
        self.w.bind("resigned key", self.windowResignedKeyCallback)

    def started(self):
        self.w.open()

    def destroy(self):
        self.w.unbind("became main", self.windowBecameMainCallback)
        self.w.unbind("resigned main", self.windowResignedMainCallback)
        self.w.unbind("became key", self.windowBecameKeyCallback)
        self.w.unbind("resigned key", self.windowResignedKeyCallback)
        if self.panel is not None:
            if self.panel.w.isVisible():
                self.panel.w.close()
            self.panel = None

    def windowBecameMainCallback(self, sender):
        self.w.setItemValue("mainLabel", "main: yes")
        if self.panel is None:
            self.panel = DemoPanel()
        self.panel.w.show()

    def windowResignedMainCallback(self, sender):
        self.w.setItemValue("mainLabel", "main: no")
        self.panel.w.hide()

    def windowBecameKeyCallback(self, sender):
        self.w.setItemValue("keyLabel", "key: yes")
        if self.panel is None:
            self.panel = DemoPanel()
        self.panel.w.show()

    def windowResignedKeyCallback(self, sender):
        self.w.setItemValue("keyLabel", "key: no")
        self.panel.w.hide()


class DemoPanel(ezui.WindowController):

    def build(self):
        content = """
        [_ A field that can become key. _] @field
        ---X--- @slider
        ---
        key: no @keyLabel
        """
        descriptionData = dict()
        self.w = ezui.EZPanel(
            content=content,
            descriptionData=descriptionData,
            controller=self,
            size=(250, "auto"),
            closable=False
        )
        self.w.bind("became key", self.windowBecameKeyCallback)
        self.w.bind("resigned key", self.windowResignedKeyCallback)

    def started(self):
        self.w.open()

    def destroy(self):
        self.w.unbind("became key", self.windowBecameKeyCallback)
        self.w.unbind("resigned key", self.windowResignedKeyCallback)

    def windowBecameKeyCallback(self, sender):
        self.w.setItemValue("keyLabel", "key: yes")

    def windowResignedKeyCallback(self, sender):
        self.w.setItemValue("keyLabel", "key: no")


DemoWindow()