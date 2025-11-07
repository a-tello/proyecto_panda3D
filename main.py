from panda3d.core import WindowProperties
from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DirectLabel, DirectOptionMenu, DirectSlider
from direct.actor.Actor import Actor
from panda3d.core import TextNode
class Juego(ShowBase):
    def __init__(self):
        super().__init__()
        
        self.disableMouse()
        
        # PANTALLA
        prop_pantalla = WindowProperties()
        prop_pantalla.setSize(800,600)
        prop_pantalla.set_fullscreen(False)
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


        DirectLabel(text = 'Pantalla', scale = 0.1, pos = (-.5, 0, 0.2), parent = self.menu_opciones, 
                        text_fg = (1, 1, 1, 1), frameSize = (-4, 4, -1, 1), text_pos = (0, -0.2))

        btn = DirectOptionMenu(text="Resolución de pantalla", pos = (.5, 0, 0.2), parent = self.menu_opciones, scale=0.1, initialitem=0,
                        frameSize = (-4, 4, -1, 1), text_scale = 1.1, text_pos = (0, -0.2), command=self.cambiar_pantalla, text_align=TextNode.ACenter,
                        items=['800 x 600','1280 x 960', '1280 x 1024', '1920 x 1080'], highlightColor=(0.65, 0.65, 0.65, 1), textMayChange=1)
        btn.setTransparency(True)
        
        
        DirectLabel(text = 'Musica', scale = 0.1, pos = (-.5, 0, -0.2), parent = self.menu_opciones, 
                        text_fg = (1, 1, 1, 1),frameSize = (-4, 4, -1, 1), text_pos = (0, -0.2))
        self.volumen = DirectSlider(range=(0,100), value=100, pos = (.5, 0, -0.2), pageSize=3, command=self.musica, scale=0.5, parent=self.menu_opciones)
        # btn = DirectButton(text = 'Musica', command = self.menu, pos = (.5, 0, -0.2), parent = self.menu_opciones, scale = 0.1, 
        #                 frameSize = (-4, 4, -1, 1), text_scale = 0.75, text_pos = (0, -0.2))
        # btn.setTransparency(True)

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
        
    def cambiar_pantalla(self, op):
        ancho, alto = op.split(' x ')
        prop_pantalla = WindowProperties()
        prop_pantalla.setSize(int(ancho), int(alto))
        self.win.requestProperties(prop_pantalla)
        
    def salir(self):
        self.userExit()

    def musica(self):
        print(self.volumen['value'])
juego = Juego()
juego.run()