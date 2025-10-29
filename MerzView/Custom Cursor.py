"""
Set a cursor for a MerzView.

Relevant Documentation:
    - MerzView: https://typesupply.github.io/merz/views/merzView.html
"""

import AppKit
import merz
import ezui

size = 15
black = AppKit.NSColor.blackColor()
white = AppKit.NSColor.whiteColor()
oval = AppKit.NSBezierPath.bezierPathWithOvalInRect_(
    ((5, 5), (size - 10, size - 10))
)
cursorImage = AppKit.NSImage.alloc().initWithSize_((size, size))
cursorImage.lockFocus()
white.set()
oval.setLineWidth_(2)
oval.stroke()
black.set()
oval.setLineWidth_(1)
oval.fill()
cursorImage.unlockFocus()
demoCursor = CreateCursor(
    cursorImage,
    hotSpot=(size/2, size/2)
)


class Demo(ezui.WindowController):

    def build(self):
        content = """
        * MerzView @merzView
        """
        descriptionData = dict(
            merzView=dict(
                backgroundColor=(1, 0, 0, 1),
                delegate=self,
                width=500,
                height=500
            )
        )
        self.w = ezui.EZWindow(
            title="Demo",
            content=content,
            descriptionData=descriptionData,
            controller=self
        )

    def started(self):
        self.w.open()

    # Delegate Methods

    def mouseEntered(self, sender, event):
        self._previousCursor = AppKit.NSCursor.currentCursor()
        demoCursor.set()

    def mouseExited(self, sender, event):
        self._previousCursor.set()
        demoCursor.set()


Demo()