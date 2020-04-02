import gvsig
import sys

from gvsig import commonsdialog
from gvsig import geom
from org.gvsig.tools.dispose import DisposeUtils
from gvsig import commonsdialog
from gvsig import *


def mensajeCartel(mensaje, titulo, tipoMensaje):
    message = mensaje
    title = titulo
    messageType = tipoMensaje
    root = None
    commonsdialog.msgbox(message, title, messageType, root)


def calcularArea(currentView, currentLayer):

     # Ejemplo de inputbox
    message = "Ingrese el valor del "+ unichr(225) + "rea de referencia en km2"
    title = "Ingreso de datos"
    messageType = commonsdialog.QUESTION
    root = None

    currentProject = gvsig.currentProject() # Proyecto actual
    # Vista actual
    print "Vista actual:", currentView
    # Capas
    print "Capas de la vista actual:"
    if currentView != None:
        currentViewLayers = currentView.getLayers()
        for currentViewLayer in currentViewLayers:
            print " ", currentViewLayer
    # Capa actual
    print "Sumatory of all of the areas in the polygon layer: ", currentLayer
    
    valorReferencia = float(commonsdialog.inputbox(message, title, messageType, root))
    print "valor Referencia: ", valorReferencia

    area = 0
    if currentView != None:
        if currentLayer != None:
            polygonsLayer = currentLayer
            # Creamos esquema con el tipo de geometria correspondiente
            schema = polygonsLayer.getSchema()
            newSchema = createSchema(schema)
            # Creamos la capa nueva con el nuevo esquema
            newPolygonsLayer = createShape(newSchema)
            newPolygonsLayer.edit()
            
            features = currentLayer.features() # Entidades
            message = ""
            if features != None:
                try:
                    polygonFeatures = polygonsLayer.features()
                    contador = 0
                    for polygonFeature in polygonFeatures:
                        area += polygonFeature.geometry().area()
                        #print("area: ",area)
                        polygon = dict()
                        for field in schema:
                            #print "prueba: "+str(field.getDataTypeName())
                            if str(field.getDataTypeName()) != "Double":
                                polygon[field.getName()] = polygonFeature.get(field.getName())
                            else:
                                polygon[field.getName()] = long(polygonFeature.get(field.getName()))
                        
                        tempArea = polygonFeature.geometry().area() * 1000
                        
                        if tempArea > valorReferencia:
                            newPolygonsLayer.append(polygon)
                            contador= contador +1
                            #newfeature = self.createNewFeature(output_store, polygonFeature)
                            #newfeature["GEOMETRY"] = polygon
                            #output_store.insert(newfeature)
                            
                            
                    area = area *10000 # area *10000 para obtener el area en kilometros cuadrados
                    #self.addOutputText("OutputText", "Area: ")
                    #self.addOutputNumericalValue("OutputNumerical", "area")
                    newPolygonsLayer.commit()
                    newPolygonsLayer.setName("Capa de poligonos mayores")
                    currentView.addLayer(newPolygonsLayer)
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
            mensajeCartel("En la vista actual no hay seleccionada ninguna capa, debe seleccionar una capa.", "Error: se debe seleccionar una capa", commonsdialog.FORBIDEN)
    else:
        mensajeCartel("No se encuentra ninguna vista para comenzar a trabajar", "Error: sin vista", commonsdialog.FORBIDEN)
    
    return area
    

def main(*args):
    currentView = gvsig.currentView()
    currentLayer = gvsig.currentLayer()
    area = calcularArea(currentView, currentLayer)
    if area!= 0:
        message = str(float(area)) + " Km2" # https://es.wikipedia.org/wiki/Uruguay
        title = unichr(193)+"rea"  # https://es.wikipedia.org/wiki/ISO/IEC_8859-1
        mensajeCartel(message, title, commonsdialog.IDEA)
        