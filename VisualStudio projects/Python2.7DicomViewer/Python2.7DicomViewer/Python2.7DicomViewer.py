# -*- coding: utf-8 -*-
"""
This module allows the displaying DICOM images in a frame and adding rectangular annotations with a label to the image.
The annotations can then be exported as a JSON text file or the full canvas can be exported as a ghostscrip (.ps) file to be viewed indepentendly.
The annotations for a file can be imported back to vizualize them again.

"""

from __future__ import division
from Tkinter import *
import tkFileDialog
import tkMessageBox

from pydicom import dicomio
import pydicom.contrib.pydicom_Tkinter as pydicom_Tkinter # from https://github.com/darcymason/pydicom/blob/dev/pydicom/contrib/pydicom_Tkinter.py
import json

from AnnotationObject import AnnotationObject
from HelperFunctions import HelperFunctions

class DicomViewer(Frame):
    """
    DicomViewer is the class containing the Tkinter window with menu, the canvas, the buttons and mouse events.

    Attributes:
        Frame (Tkinter): Tkinter Frame widget which may contain other frames and canvases

    """

    def __init__(self, master):
        Frame.__init__(self, master, relief=SUNKEN, bd=2)
        self.createWindow()
        self.addMenuBar()
        self.addCanvasAndMouseEvents()
        self.addLabelButton()
        self.initializeValues()
        
    def initializeValues(self):
        """
        Initializes default values for the DICOM viewer
        
        Note: This is called to reset the viewer

        Args: none

        Returns: nothing

        """
        self.isDrawingRectangle = False
        self.scaledImageWidth = 0
        self.scaledImageHeight = 0
        self.zoomScale = 0
        self.rect = None
        self.annotationNumber = 0
        self.annotationList = []
        self.lastRectangle = None
        self.lastLabel = None
        self.isDicomLoaded = False

    def createWindow(self):
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        w = 1024
        h = 768
        x = (sw - w) / 2
        y = (sh - h) / 2
        self.master.title("DICOM Viewer")
        self.pack(fill=BOTH, expand=1)
        self.master.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def addMenuBar(self):
        self.menubar = Menu(self)
        # File Menu
        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=menu)
        menu.add_command(label="Open DICOM File", command=self.loadFile)
        menu.add_command(label="Import annotations", command=self.importAnnotations)
        menu.add_command(label="Export annotations to JSON", command=self.exportAnnotations)
        menu.add_command(label="Save as PostScript", command=self.saveCanvasAsPS)
        # Edit Menu
        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=menu)
        menu.add_command(label="Remove All", command=self.removeAllWidgets)
        menu.add_command(label="Undo Last Annotation", command=self.removeLastWidget)
        # Quit Menu
        menu = Menu(self.menubar, tearoff=0)
        self.menubar.add_command(label="Quit Viewer", command=quit)

        self.master.config(menu=self.menubar)

    def addCanvasAndMouseEvents(self):
        self.x = self.y = 0
        self.canvas = Canvas(self, width=0, height=0, cursor="cross")
        self.canvas.pack(side="top", fill="both", expand=True)
        self.canvas.bind("<ButtonPress-1>", self.on_mouseLeftClick)
        self.canvas.bind("<B1-Motion>", self.on_mouseMove)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouseLeftClickRelease)
    
    def addLabelButton(self):
        L1 = Label(text="Label")
        L1.pack(side = LEFT)
        self.labelEntry = Entry(bd = 5)
        self.labelEntry.pack()
        button = Button(self, text='Change Last Label', command=self.on_labelButtonClick)
        button.pack()

    def on_labelButtonClick(self):
        if self.lastLabel is None:
            return

        newLabel = self.labelEntry.get()
        self.lastLabel['text'] = newLabel
        # update the list of labels accordingly
        self.annotationList[-1].title = newLabel

    def on_mouseLeftClick(self, event):
        # draw rectangle on canvas only when clicking a pixel on the image
        mouseInsideImage = event.x <= self.scaledImageWidth and event.y < self.scaledImageHeight
        if mouseInsideImage:
            # save mouse drag start position
            self.start_x = event.x
            self.start_y = event.y
            self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1)

    def on_mouseMove(self, event):
        curX, curY = (event.x, event.y)

        # draw triangle as mouse is dragged only if a triangle was created at
        # mouse press i.e.  on the image, not the canvas
        if self.rect != None:
            self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)
            self.isDrawingRectangle = True

    def on_mouseLeftClickRelease(self, event):
        # save mouse drag start position only when drawing rectangle
        if self.isDrawingRectangle == True:
            # get rectangle coords
            self.lastRectangle = self.rect
            scaledRectangleCoords = self.canvas.coords(self.lastRectangle)
            realRectangleCoords = [int(x * self.zoomScale) for x in scaledRectangleCoords]
             
            # draw annotation label at top of rectangle
            annotationLabelText = 'Annotation ' + str(self.annotationNumber)
            annotationLabel = Label(self.canvas, text=annotationLabelText, fg='white', bg='black')
            self.lastLabel = annotationLabel
            xDiff = int(abs(scaledRectangleCoords[2] - scaledRectangleCoords[0]) / 2)
            labelX = scaledRectangleCoords[0] + xDiff if scaledRectangleCoords[0] < scaledRectangleCoords[2] else scaledRectangleCoords[2] + xDiff
            labelY = scaledRectangleCoords[1] if scaledRectangleCoords[1] < scaledRectangleCoords[3] else scaledRectangleCoords[3]
            self.canvas.create_window(labelX - 40, labelY - 20, window=annotationLabel, anchor=NW)

            # save coordinates of rectangle in list with the position on the
            # canvas as well as scale of shown image
            newAnnotation = AnnotationObject(realRectangleCoords[0], realRectangleCoords[1], realRectangleCoords[2], realRectangleCoords[3], annotationLabelText)
            self.annotationList.append(newAnnotation)

            # reset and increment
            self.rect = None
            self.annotationNumber += 1

        self.isDrawingRectangle = False
        pass

    def quit():
        global root
        root.quit()

    def removeAllWidgets(self):
        self.canvas.delete("all")
        self.initializeValues()

    def removeLastWidget(self):
        if len(self.annotationList) == 0 or self.lastRectangle is None or self.lastLabel is None:
            return

        # remove last from list
        self.annotationList.pop(-1)
        # remove rectangle and label widget from image
        self.canvas.delete(self.lastRectangle)
        self.lastLabel.destroy()

    def loadFile(self):
        """
        Loads single DICOM image into the Tkinter python GUI, Zooms the image according to the space in the canvas
        
        Note: cannot load a stack of DICOM images

        Args: none

        Returns: nothing

        """

        self.removeAllWidgets()

        # Open file with dialog
        dicomImage = tkFileDialog.askopenfilename(initialdir = "C:\"", title = "choose DICOM file", filetypes = (("DICOM files","*.dcm"),("all files","*.*")))
        
        # Read file into pydicom
        dFile = dicomio.read_file(dicomImage)

        # Get the Tkinter photo image with pydicom_Tkinter
        dicomImage = pydicom_Tkinter.get_tkinter_photoimage_from_pydicom_image(dFile)
        
        # Zoom the photo image to match the window by rescaling for the longest side
        helperFunctions = HelperFunctions()
        self.zoomScale = helperFunctions.getZoomScale(dicomImage.width(), dicomImage.height(), self.canvas.winfo_width(), self.canvas.winfo_height())
        displayImage = dicomImage.subsample(self.zoomScale, self.zoomScale)
        self.scaledImageWidth = dicomImage.width() / self.zoomScale
        self.scaledImageHeight = dicomImage.height() / self.zoomScale

        # Update DICOM loaded property
        self.isDicomLoaded = True

        # Display image in canvas
        image1 = self.canvas.create_image(0, 0, image = displayImage, anchor=NW)
        self.mainloop()

    def exportAnnotations(self):
        """
        Exports annotations to JSON file
        Args: none

        Returns:
            a JSON file containing the arguments in the following form: 
            [
                {
                    "endX": 1300, 
                    "endY": 592, 
                    "startX": 1222, 
                    "startY": 416, 
                    "title": "bone"
                }
            ]

       """
        json_string = json.dumps([ob.__dict__ for ob in self.annotationList], indent=4, sort_keys=True)
        f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".json")
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        f.write(json_string)
        f.close()

    def importAnnotations(self):
        """
        Imports annotations to a DICOM image if loaded. The annotations will scale according to the zoom factor
        
        Note: annotations can be loaded for a different image, a system should be implemented to restrict the annotations to a specific image. Perhaps a hash of the image in the JSON export.

        Args: none

        Returns: nothing

        """
        # Check that image is loaded
        if not self.isDicomLoaded:
            tkMessageBox.showwarning("Open file","Must load DICOM image first")
            return

        # Open file with dialog
        file = tkFileDialog.askopenfile(initialdir = "C:\"", title = "choose JSON file", filetypes = (("JSON files","*.json"),("all files","*.*")))
        jsonString = file.read()

        helperFunctions = HelperFunctions()

        # convert the json dictionary object to an array of annotation objects
        # and load into the saved annotation list
        self.annotationList = json.loads(jsonString, object_hook=helperFunctions.JsonDictToAnnotationObject)

        # scale the annotations to match the current object
        #scaledAnnotationList = map(helperFunctions.scaleAnnotationObject, self.annotationList)
        scaledAnnotationList = [helperFunctions.scaleAnnotationObject(item, self.zoomScale) for item in self.annotationList]

        # Add annotations to canvas
        for annotationItem in scaledAnnotationList:
            # make a rectangle and add to canvas
            newRectangle = self.canvas.create_rectangle(annotationItem.startX, annotationItem.startY, annotationItem.endX, annotationItem.endY)
            # add the label
            xDiff = int(abs(annotationItem.endX - annotationItem.startX) / 2)
            labelX = annotationItem.startX + xDiff if annotationItem.startX < annotationItem.endX else annotationItem.endX + xDiff
            labelY = annotationItem.startY if annotationItem.startY < annotationItem.endY else annotationItem.endY
            annotationLabel = Label(self.canvas, text=annotationItem.title, fg='white', bg='black')
            self.canvas.create_window(labelX - 40, labelY - 20, window=annotationLabel, anchor=NW)

    def saveCanvasAsPS(self):
        f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".ps")
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return

        postcript = self.canvas.postscript()
        f.write(postcript)
        f.close()

def main():
    """
    Entry point for the application, loads the Dicom viewer with Tkinter GUI tools

    """
    root = Tk()
    app = DicomViewer(root)
    app.pack()
    root.mainloop()

if __name__ == '__main__':
    main()

