"""
Change the scale in a MerzView with a magnifyWithEvent
delegate method. The initial point in the magnifyWithEvent
will be used as the focal point so that the content
at that point will remain visible.

Relevant Documentation:
    - ScrollingMerzView: https://typesupply.github.io/merz/views/merzView.html#scrollingmerzview
    - NSEvent.magnification: https://developer.apple.com/documentation/appkit/nsevent/1531642-magnification?language=objc
    - NSEvent.phase: https://developer.apple.com/documentation/appkit/nsevent/1533550-phase?language=objc
"""

import AppKit
import ezui
import merz

class Demo(ezui.WindowController):

    def build(self):
        self.viewBaseSize = (400, 400)

        content = """
        * ScrollingMerzView @merzView
        """
        descriptionData = dict(
            merzView=dict(
                delegate=self,
                width=self.viewBaseSize[0],
                height=self.viewBaseSize[1]
            )
        )
        self.w = ezui.EZWindow(
            content=content,
            descriptionData=descriptionData,
            controller=self
        )
        self.merzView = self.w.getItem("merzView")
        self.merzView.setMerzViewSize(self.viewBaseSize)

        container = self.merzView.getMerzContainer()
        container.appendOvalSublayer(
            position=(50, 50),
            size=(150, 150),
            fillColor=(1, 0, 0, 1)
        )
        container.appendBaseSublayer(
            position=(50, 200),
            size=(150, 150),
            backgroundColor=(0, 1, 0, 1)
        )
        container.appendBaseSublayer(
            position=(200, 50),
            size=(150, 150),
            backgroundColor=(0, 0, 1, 1)
        )
        container.appendOvalSublayer(
            position=(200, 200),
            size=(150, 150),
            fillColor=(1, 1, 0, 1)
        )

    def started(self):
        self.w.open()

    # MerzView Delegate

    def acceptsFirstResponder(self, sender):
        return True

    magnifyWithEventFocalPoint = None

    def magnifyWithEvent(self, sender, event):
        merzView = self.merzView
        scrollView = merzView.getNSScrollView()
        documentView = merzView.getMerzView().getNSView()
        container = merzView.getMerzContainer()
        eventInfo = merz.unpackEvent(event)
        if "magnification" not in eventInfo:
            # note: unpacking magnification events
            # is in an upcoming merz change as of
            # the writing of this demo.
            eventInfo = tempEventUnpack(event)
        # get the current view state
        oldScale = container.getContainerScale()
        # get the base view size
        unscaledWidth, unscaledHeight = merzView.getMerzViewSize()
        unscaledWidth /= oldScale
        unscaledHeight /= oldScale
        # calculate the new scale
        magnification = eventInfo["magnification"]
        minScale = 0.1
        maxScale = 3.0
        if magnification < 0:
            factor = 0.9
        else:
            factor = 1.1
        scale = oldScale * factor
        if scale > maxScale:
            scale = maxScale
        elif scale < minScale:
            scale = minScale
        # calculate the new size
        width = unscaledWidth * scale
        height = unscaledHeight * scale
        # apply the new scale
        container.setContainerScale(scale)
        # apply the new size
        merzView.setMerzViewSize((width, height))
        # store the focal point at the start of the gesture
        phase = eventInfo["phase"]
        if phase == "began":
            x, y = documentView.convertPoint_fromView_(
                eventInfo["location"],
                None
            )
            x /= oldScale
            y /= oldScale
            self.magnifyWithEventFocalPoint = (x, y)
        # convert the focal point to the scaled coordinates
        x, y = self.magnifyWithEventFocalPoint
        x *= scale
        y *= scale
        # center the point in the visible position of the view
        visibleWidth, visibleHeight = documentView.visibleRect().size
        x = x - (visibleWidth / 2)
        y = y - (visibleHeight / 2)
        # scroll to the point
        documentView.scrollPoint_((x, y))
        # clean up at the end of the gesture
        if phase == "ended":
            self.magnifyWithEventFocalPoint = None

def tempEventUnpack(event):
    _gesturePhaseMap = {
        AppKit.NSEventPhaseNone : "none",
        AppKit.NSEventPhaseBegan : "began",
        AppKit.NSEventPhaseStationary : "stationary",
        AppKit.NSEventPhaseChanged : "changed",
        AppKit.NSEventPhaseEnded : "ended",
        AppKit.NSEventPhaseCancelled : "cancelled",
        AppKit.NSEventPhaseMayBegin : "begin"
    }
    unpacked = dict(
        phase=_gesturePhaseMap.get(event.phase(), "unknown"),
        location=event.locationInWindow(),
        magnification=event.magnification()
    )
    return unpacked


Demo()
