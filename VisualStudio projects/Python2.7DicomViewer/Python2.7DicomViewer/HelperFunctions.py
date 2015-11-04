"""
HelperFunctions contains utility methods for the DICOM viewer application

Example:
    newAnnotation = AnnotationObject(12, 12, 24, 24, "this is the title")
    
"""

from AnnotationObject import AnnotationObject

class HelperFunctions():

   def JsonDictToAnnotationObject(self, dct):
       """
        Note:
            This should include a try/catch for bad files
        Args:
            dct: The dictionary object coming for an imported JSON file

        Returns:
            An annotation object from the properties

       """
       return AnnotationObject(dct['startX'], dct['startY'], dct['endX'], dct['endY'], dct['title'])

   def getZoomScale(self, imageWidth, imageHeight, frameWidth, frameHeight):
        """
        Zoom the photo image to match the window by rescaling for the longest side
        Args:
            startX (int): The X parameter of the first corner of the rectangle.
            startX (int): The Y parameter of the first corner of the rectangle.
            startX (int): The X parameter of the second corner of the rectangle.
            startX (int): The Y parameter of the second corner of the rectangle.

        Returns:
            An zoom scale(int) used to subsample the image

       """

        zoomScale = imageWidth / frameWidth if imageWidth > imageHeight else imageHeight / frameHeight
        zoomScale = int(zoomScale)

        if zoomScale < 1:
            zoomScale = 1

        return zoomScale

   def scaleAnnotationObject(self, annotationObject, zoomScale):
        """

        Args:
            annotationObject: The annotation to be scaled

        Returns:
            An scaled annotation object to show in the frame

       """
        return AnnotationObject(int(annotationObject.startX / zoomScale), int(annotationObject.startY / zoomScale), 
                                int(annotationObject.endX / zoomScale), int(annotationObject.endY / zoomScale), annotationObject.title)