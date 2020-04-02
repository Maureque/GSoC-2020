import gvsig
import sys

from gvsig import commonsdialog
from gvsig import geom
from org.gvsig.tools.dispose import DisposeUtils
from gvsig import commonsdialog

from gvsig import *
from gvsig.geom import *

def calcularArea(currentView, currentLayer):
    area = 0
    if currentView != None:
        if currentLayer != None:
            features = currentLayer.features() # Entidades
            message = ""
            if features != None:
                try:
                    polygonsLayer = currentLayer
                    polygonFeatures = polygonsLayer.features()
                    for polygonFeature in polygonFeatures:
                        area += polygonFeature.geometry().area()
                    area = area *10000 # area *10000 para obtener el area en kilometros cuadrados
                except:
                    ex = sys.exc_info()[1] # Captura de excepciones
                    message = ex.__class__.__name__ + " - " + str(ex)
                finally:
                    DisposeUtils.disposeQuietly(features) # Liberacion de recursos
            if message != "":
                title = "Error"
                messageType = commonsdialog.FORBIDEN
                root = None
                commonsdialog.msgbox(message, title, messageType, root)
        else:
            message = "En la vista actual no hay seleccionada ninguna capa, debe seleccionar una capa."
            title = "Error: se debe seleccionar una capa"
            messageType = commonsdialog.FORBIDEN
            root = None
            commonsdialog.msgbox(message, title, messageType, root)
    else:
        message = "No se encuentra ninguna vista para comenzar a trabajar"
        title = "Error: sin vista"
        messageType = commonsdialog.FORBIDEN
        root = None
        commonsdialog.msgbox(message, title, messageType, root)

    return area
    

def main(*args):
    currentProject = gvsig.currentProject() # Proyecto actual
    # Vista actual    
    currentView = gvsig.currentView()
    print "Vista actual:", currentView
    # Capas
    print "Capas de la vista actual:"
    if currentView != None:
        currentViewLayers = currentView.getLayers()
        for currentViewLayer in currentViewLayers:
            print " ", currentViewLayer
    # Capa actual
    currentLayer = gvsig.currentLayer()
    print "Sumatory of all of the areas in the polygon layer: ", currentLayer

    area = calcularArea(currentView, currentLayer)
    if area!= 0:
        message = str(float(area)) + " Km2" # https://es.wikipedia.org/wiki/Uruguay
        title = unichr(193)+"rea"  # https://es.wikipedia.org/wiki/ISO/IEC_8859-1
        messageType = commonsdialog.IDEA
        root = None
        commonsdialog.msgbox(message, title, messageType, root)
        