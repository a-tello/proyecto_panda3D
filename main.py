from panda3d.core import WindowProperties
from direct.showbase.ShowBase import ShowBase

class Juego(ShowBase):
    def __init__(self):
        super().__init__()
        
        self.disableMouse()
        
        # PANTALLA
        prop_pantalla = WindowProperties()
        prop_pantalla.setSize(1280,960)
        self.win.requestProperties(prop_pantalla)
        
        # ENTORNO
        self.entorno = self.loader.loadModel('assets/Environment/environment')
        self.entorno.reparentTo(self.render) 


juego = Juego()
juego.run()