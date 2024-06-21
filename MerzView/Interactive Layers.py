"""
Allow a user to move layers around.

Relevant Documentation:
    - MerzView: https://typesupply.github.io/merz/views/merzView.html
"""

import merz
import ezui

class Demo(ezui.WindowController):

    def build(self):
        points = [
            (50, 50),
            (150, 300),
            (350, 200),
            (450, 450)
        ]
        self.points = {f"point{i}" : p for i, p in enumerate(points)}
        content = """
        * MerzView @merzView
        """
        descriptionData = dict(
            merzView=dict(
                backgroundColor=(1, 1, 1, 1),
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
        self.merzView = merzView = self.w.getItem("merzView")
        self.merzContainer = merzContainer = merzView.getMerzContainer()
        self.handle1Layer = merzContainer.appendLineSublayer(
            size=(500, 500),
            strokeColor=(0, 0, 0, 0.3),
            strokeWidth=1,
            acceptsHit=False
        )
        self.handle2Layer = merzContainer.appendLineSublayer(
            size=(500, 500),
            strokeColor=(0, 0, 0, 0.3),
            strokeWidth=1,
            acceptsHit=False
        )
        self.pathLayer = merzContainer.appendPathSublayer(
            size=(500, 500),
            fillColor=None,
            strokeColor=(0, 0, 0, 1),
            strokeWidth=2,
            acceptsHit=False
        )
        self.point0Layer = merzContainer.appendOvalSublayer(
            name="point0",
            size=(20, 20),
            fillColor=(1, 0, 0, 0.75),
            strokeWidth=4,
            anchor=(0.5, 0.5),
            acceptsHit=True
        )
        self.point1Layer = merzContainer.appendOvalSublayer(
            name="point1",
            size=(20, 20),
            fillColor=(0, 0, 1, 0.75),
            strokeWidth=4,
            anchor=(0.5, 0.5),
            acceptsHit=True
        )
        self.point2Layer = merzContainer.appendOvalSublayer(
            name="point2",
            size=(20, 20),
            fillColor=(0, 0, 1, 0.75),
            strokeWidth=4,
            anchor=(0.5, 0.5),
            acceptsHit=True
        )
        self.point3Layer = merzContainer.appendOvalSublayer(
            name="point3",
            size=(20, 20),
            fillColor=(1, 0, 0, 0.75),
            strokeWidth=4,
            anchor=(0.5, 0.5),
            acceptsHit=True
        )
        self.selectedPoint = None
        self.updateDisplay()

    def started(self):
        self.w.open()

    def updateDisplay(self):
        point0 = self.points["point0"]
        point1 = self.points["point1"]
        point2 = self.points["point2"]
        point3 = self.points["point3"]
        path = merz.MerzPen()
        path.moveTo(point0)
        path.curveTo(point1, point2, point3)
        path.endPath()
        with self.handle1Layer.propertyGroup():
            self.handle1Layer.setStartPoint(point0)
            self.handle1Layer.setEndPoint(point1)
        with self.handle2Layer.propertyGroup():
            self.handle2Layer.setStartPoint(point3)
            self.handle2Layer.setEndPoint(point2)
        self.pathLayer.setPath(path.path)
        self.point0Layer.setPosition(point0)
        self.point1Layer.setPosition(point1)
        self.point2Layer.setPosition(point2)
        self.point3Layer.setPosition(point3)

    # Delegate Methods

    def acceptsFirstResponder(self, sender):
        return True

    def _convertEventToPoint(self, event):
        event = merz.unpackEvent(event)
        location = event["location"]
        location = self.merzView.convertWindowCoordinateToViewCoordinate(
            point=location
        )
        point = self.merzContainer.convertViewCoordinateToLayerCoordinate(
            location,
            self.merzContainer
        )
        return point

    def mouseDown(self, sender, event):
        point = self._convertEventToPoint(event)
        hits = self.merzContainer.findSublayersContainingPoint(
            point,
            onlyAcceptsHit=True,
            recurse=True
        )
        if hits:
            layer = hits[0]
            self.selectedPoint = layer.getName()
            self.selectedLayer = layer
            layer.setStrokeColor((0, 1, 0, 0.75))

    def mouseDragged(self, sender, event):
        if self.selectedPoint is not None:
            point = self._convertEventToPoint(event)
            self.points[self.selectedPoint] = point
            self.updateDisplay()

    def mouseUp(self, sender, event):
        if self.selectedLayer is not None:
            self.selectedLayer.setStrokeColor(None)
        self.selectedPoint = None
        self.selectedLayer = None

Demo()