from panda3d.core import WindowProperties
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DirectLabel, DirectOptionMenu
from direct.actor.Actor import Actor

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

        self.personaje = Actor('assets/models/act_p3d_chan')
        self.personaje.setPos(0, 5, 0)
        self.personaje.reparentTo(self.render) 


        # MENU
        self.menu_fondo = DirectFrame(frameColor = (0, 0, 0, 1), frameSize = (-1, 1, -1, 1), parent = self.render2d)
        self.menu_inicio = DirectFrame(frameColor = (1, 1, 1, 0))

        title = DirectLabel(text = 'Zombies \n\nAte My \n\nNeighbors 3D', scale = 0.1, pos = (0, 0, 0.9), parent = self.menu_inicio, 
                        text_fg = (1, 1, 1, 1))
        
        btn = DirectButton(text = 'Jugar', command = self.jugar, pos = (0, 0, 0.2), parent = self.menu_inicio, scale = 0.1,
                        frameSize = (-4, 4, -1, 1), text_scale = 0.75, text_pos = (0, -0.2))
        btn.setTransparency(True)

        btn = DirectButton(text = 'Opciones', command = self.opciones, pos = (0, 0, -0.2), parent = self.menu_inicio, scale = 0.1, 
                        frameSize = (-4, 4, -1, 1), text_scale = 0.75, text_pos = (0, -0.2))
        btn.setTransparency(True)

        btn = DirectButton(text = 'Salir', command = self.salir, pos = (0, 0, -0.6), parent = self.menu_inicio, scale = 0.1, 
                        frameSize = (-4, 4, -1, 1), text_scale = 0.75, text_pos = (0, -0.2))
        btn.setTransparency(True)



        self.menu_opciones = DirectFrame(frameColor = (1, 1, 1, 0))

        title = DirectLabel(text = 'Opciones', scale = 0.1, pos = (0, 0, 0.9), parent = self.menu_opciones, 
                        relief = None,  text_fg = (1, 1, 1, 1))
        
        # btn = DirectButton(text = 'Resolución de pantalla', command = self.menu, pos = (0, 0, 0.2), parent = self.menu_opciones, scale = 0.1,
        #                 frameSize = (-4, 4, -1, 1), text_scale = 0.75, text_pos = (0, -0.2))
        # btn.setTransparency(True)

        btn = DirectOptionMenu(text="Resolución de pantalla", pos = (0, 0, 0.2), parent = self.menu_opciones, scale=0.1, initialitem=2,
                        frameSize = (-4, 4, -1, 1), text_scale = 1, text_pos = (-2, -0.2),
                        items=["1280 x 960", "1280 x 1024", "800 x 600", 'Fullscreen'], highlightColor=(0.65, 0.65, 0.65, 1), textMayChange=1)
        btn.setTransparency(True)
        
        
        btn = DirectButton(text = 'Musica', command = self.menu, pos = (0, 0, -0.2), parent = self.menu_opciones, scale = 0.1, 
                        frameSize = (-4, 4, -1, 1), text_scale = 0.75, text_pos = (0, -0.2))
        btn.setTransparency(True)

        btn = DirectButton(text = 'Volver al menú', command = self.menu, pos = (0, 0, -0.6), parent = self.menu_opciones, scale = 0.1, 
                        frameSize = (-4, 4, -1, 1), text_scale = 0.75, text_pos = (0, -0.2))
        btn.setTransparency(True)

        self.menu_opciones.hide()

    def jugar(self):
        self.menu_fondo.hide()
        self.menu_inicio.hide()
    def menu(self):
        self.menu_opciones.hide()
        self.menu_inicio.show()
    def opciones(self):
        self.menu_inicio.hide()
        self.menu_opciones.show()
    def salir(self):
        self.userExit()


juego = Juego()
juego.run()