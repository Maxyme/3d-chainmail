"""
AnnotationObject is the annotation object used to show rectangle annotations on the image

Example:
    newAnnotation = AnnotationObject(12, 12, 24, 24, "this is the title")
    
"""

class AnnotationObject:

    def __init__(self, startX, startY, endX, endY, title):
        """
        Args:
            startX (int): The X parameter of the first corner of the rectangle.
            startX (int): The Y parameter of the first corner of the rectangle.
            startX (int): The X parameter of the second corner of the rectangle.
            startX (int): The Y parameter of the second corner of the rectangle.
            title (string): The title of the annotation.
        """

        self.startX = startX
        self.startY = startY
        self.endX = endX
        self.endY = endY
        self.title = title
