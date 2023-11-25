"""
Make a WindowController that is also a Subscriber.

Relevant Documentation:
- subscriber: https://robofont.com/documentation/reference/api/mojo/mojo-subscriber/
- WindowController: https://typesupply.github.io/ezui/controllers.html#windowcontroller
"""

import ezui
from mojo.subscriber import Subscriber, registerRoboFontSubscriber

class Demo(Subscriber, ezui.WindowController):

    debug = True

    def build(self):
        content = """
        The current glyph is <none>. @label
        """
        descriptionData = dict()
        self.w = ezui.EZPanel(
            content=content,
            descriptionData=descriptionData,
            controller=self,
            size=(300, "auto")
        )

    def started(self):
        self.w.open()

    def roboFontDidSwitchCurrentGlyph(self, info):
        glyph = info["glyph"]
        if glyph is None:
            glyphName = "<none>"
        else:
            glyphName = glyph.name
        text = f"The current glyph is {glyphName}."
        self.w.setItemValue("label", text)

registerRoboFontSubscriber(Demo)