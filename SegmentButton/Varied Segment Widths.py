"""
Set different widths for segments.

Note: The segmentDescriptions created from the text
description do not merge with the segmentDescriptions
given in the descriptionData, so the segment contents
have to be redefined.

Relevant Documentation:
    - SegmentButton: https://typesupply.github.io/ezui/items.html#segmentbutton
"""

import ezui

class Demo(ezui.WindowController):

    def build(self):
        content = """
        (( B | Hello | F )) @segmentButton
        """
        descriptionData = dict(
            segmentButton=dict(
                segmentDescriptions=[
                    dict(
                        width=20,
                        image=ezui.makeImage(symbolName="chevron.left")
                    ),
                    dict(
                        width=50,
                        text="Hello"
                    ),
                    dict(
                        width=20,
                        image=ezui.makeImage(symbolName="chevron.right")
                    ),
                ]
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

Demo()