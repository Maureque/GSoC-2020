import gvsig
import sys

from gvsig import *
from gvsig import geom
from gvsig.commonsdialog import *
from gvsig import commonsdialog

from gvsig.libs.toolbox import *
from es.unex.sextante.gui import core
from es.unex.sextante.gui.core import NameAndIcon

from es.unex.sextante.gui.core import SextanteGUI
from org.gvsig.geoprocess.lib.api import GeoProcessLocator

class PolygonsBiggerThan(ToolboxProcess):

  def defineCharacteristics(self):
        """Definir los parametros de entrada y salida de nuestro proceso. """
        # Nombre con el que se va a mostrar nuestro proceso
        self.setName("Polygons bigger than given value")

        # Grupo en el que aparecera
        self.setGroup("Vectorial")
        params = self.getParameters()

        # Indicamos que precisamos un parametro LAYER, del tipo poligono y que es obligatorio
        params.addInputVectorLayer("LAYER","Capa de entrada", SHAPE_TYPE_POLYGON, True)

        # Indicamos que precisamos un area de referencia para la comparacion
        params.addNumericalValue("AREA_VALOR", "Valor del area de referencia a comparar (m)",0, NUMERICAL_VALUE_INTEGER)

  def processAlgorithm(self):
          """ Operacion encargada de realizar nuestro proceso. """
          features=None
          try:
              """
              Recogemos los parametros y creamos el conjunto de entidades asociadas a la capa
              de entrada.
              Se obtendran dos capas en la vista con el mismo tipo de datos.
              ** Una capa es la generada por nosotros desde el script
              ** La otra capa es la gestionada a traves de la Toolbox creada en output_store
              """
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
              
              params = self.getParameters()
              inputLayer = params.getParameterValueAsVectorLayer("LAYER")
              valorReferencia = int(params.getParameterValueAsDouble("AREA_VALOR"))
              print "valor Referencia: ", valorReferencia
              store = inputLayer.getFeatureStore()
              features = store.features()
          
              area = 0
              # Creamos esquema con el tipo de geometria correspondiente
              schema = inputLayer.getBaseDataObject().getSchema()
              newSchema = createSchema(schema)
              # Creamos la capa nueva con el nuevo esquema
              newPolygonsLayer = createShape(newSchema)
              newPolygonsLayer.edit()
              
              features = inputLayer.getBaseDataObject().features() # Entidades
              message = ""
              if features != None:
                  try:
                      for feature in features:
                          area += feature.geometry().area()
                          polygon = dict()
                          for field in schema:
                              if str(field.getDataTypeName()) != "Double":
                                  polygon[field.getName()] = feature.get(field.getName())
                              else:
                                  polygon[field.getName()] = long(feature.get(field.getName()))
                          
                          tempArea = feature.geometry().area()
                          if not inputLayer.getBaseDataObject().getProjection().isProjected():
                              tempArea = 10000 * tempArea
                          
                          if tempArea > valorReferencia:
                              newPolygonsLayer.append(polygon)
                              
                      newPolygonsLayer.setName("Capa de poligonos mayores")
                      newPolygonsLayer.commit()
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
                    
          finally:
              DisposeUtils.disposeQuietly(features)
              print "Proceso terminado %s" % self.getCommandLineName()


def main(*args):
        # Creamos nuesto geoproceso
        process = PolygonsBiggerThan()
        # Lo registramos entre los procesos disponibles en el grupo de "Scripting"
        process.selfregister("Scripting")

        # Actualizamos el interface de usuario de la Toolbox
        process.updateToolbox()

        msgbox("Incorporado el script '%s/%s/%s' a la paleta de geoprocesos." % (
                "Scripting",
                process.getGroup(),
                process.getName()
        ),
        "Proceso registrado"
        )
