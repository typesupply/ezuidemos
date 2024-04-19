"""
Change the scale in a MerzView with a magnifyWithEvent
delegate method. Note: this does not center the scaled
content at the center point of the event. That is a more
complex operation that will be shown in a different demo.

Relevant Documentation:
    - MerzView: https://typesupply.github.io/merz/views/merzView.html
    - NSEvent.magnification: https://developer.apple.com/documentation/appkit/nsevent/1531642-magnification?language=objc
"""

import ezui
import merz

class Demo(ezui.WindowController):

    def build(self):
        content = """
        * MerzView @merzView
        """
        descriptionData = dict(
            merzView=dict(
                delegate=self,
                backgroundColor=(1, 0, 0, 1)
            )
        )
        self.w = ezui.EZWindow(
            content=content,
            descriptionData=descriptionData,
            controller=self,
            size=(500, 500)
        )
        self.merzView = self.w.getItem("merzView")
        container = self.merzView.getMerzContainer()
        parent = container
        scale = 1.0
        size = 400
        for i in range(10):
            parent.appendOvalSublayer(
                position=("center", "center"),
                size=(size * scale, size * scale),
                fillColor=(0, 0, 1, 0.25),
                strokeColor=(1, 1, 0, 1),
                strokeWidth=1
            )
            scale *= 0.75
        container.setContainerScale(0.5)


    def started(self):
        self.w.open()

    # MerzView Delegate

    def acceptsFirstResponder(self, sender):
        return True

    def magnifyWithEvent(self, sender, event):
        minScale = 0.1
        maxScale = 3.0
        magnificationDelta = event.magnification()
        if magnificationDelta < 0:
            factor = 0.9
        else:
            factor = 1.1
        container = self.merzView.getMerzContainer()
        scale = container.getContainerScale()
        scale *= factor
        if scale > maxScale:
            scale = maxScale
        elif scale < minScale:
            scale = minScale
        container.setContainerScale(scale)

Demo()
