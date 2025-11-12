from direct.gui.DirectGui import DirectFrame, DirectButton, DirectLabel, DirectOptionMenu, DirectSlider, DirectRadioButton
from panda3d.core import TextNode

class Menu():
    def __init__(self, juego):
        self.menu_fondo = DirectFrame(frameColor = (0, 0, 0, 1), frameSize = (-1, 1, -1, 1), parent = juego.render2d)
        self.menu = DirectFrame(frameColor = (1, 1, 1, 0))

    def esconder_menu(self):
        self.menu.hide()
        self.menu_fondo.hide()

    def mostrar_menu(self):
        self.menu_fondo.show()
        self.menu.show()

class MenuPrincipal(Menu):
    def __init__(self, juego):
        super().__init__(juego)
        
        title = DirectLabel(text = 'Zombies \n\nAte My \n\nNeighbors 3D', scale = 0.1, pos = (0, 0, 0.9), parent = self.menu, 
                        text_fg = (1, 1, 1, 1))
        
        btn = DirectButton(text = 'Jugar', command = juego.jugar, pos = (0, 0, 0.2), parent = self.menu, scale = 0.1,
                        frameSize = (-4, 4, -1, 1), text_scale = 0.75, text_pos = (0, -0.2))
        btn.setTransparency(True)

        btn = DirectButton(text = 'Opciones', command = juego.opciones, pos = (0, 0, -0.2), parent = self.menu, scale = 0.1, 
                        frameSize = (-4, 4, -1, 1), text_scale = 0.75, text_pos = (0, -0.2))
        btn.setTransparency(True)

        btn = DirectButton(text = 'Salir', command = juego.salir, pos = (0, 0, -0.6), parent = self.menu, scale = 0.1, 
                        frameSize = (-4, 4, -1, 1), text_scale = 0.75, text_pos = (0, -0.2))
        btn.setTransparency(True)


class MenuOpciones(Menu):
    def __init__(self, juego):
        super().__init__(juego)
        

        title = DirectLabel(text = 'Opciones', scale = 0.1, pos = (0, 0, 0.9), parent = self.menu, 
                        relief = None,  text_fg = (1, 1, 1, 1))
        

        DirectLabel(text = 'Resolución', scale = 0.1, pos = (-.5, 0, 0.6), parent = self.menu, text_fg = (1, 1, 1, 1), 
                    frameSize = (-4, 4, -1, 1), text_pos = (0, -0.2))

        btn = DirectOptionMenu(text="Resolución de pantalla", pos = (.5, 0, 0.6), parent = self.menu, scale=0.1, initialitem=0,
                        frameSize = (-4, 4, -1, 1), text_scale = 1.1, text_pos = (0, -0.2), command=juego.cambiar_pantalla, text_align=TextNode.ACenter,
                        items=['800 x 600','1280 x 960', '1280 x 1024', '1920 x 1080'], highlightColor=(0.65, 0.65, 0.65, 1), textMayChange=1)
        btn.setTransparency(True)


        DirectLabel(text = 'Modo de pantalla', scale = 0.1, pos = (-.5, 0, 0.2), parent = self.menu, text_fg = (1, 1, 1, 1), 
                    frameSize = (-4, 4, -1, 1), text_pos = (0, -0.2))
        
        buttons = [
        DirectRadioButton(text='Pantalla Completa', variable=[1], value=[0], indicatorValue=False ,scale=0.08, pos=(0.5, 0, .23), command=juego.modo_pantalla, 
                          parent=self.menu, extraArgs=[True]),
        DirectRadioButton(text='Modo ventana', variable=[1], value=[1], indicatorValue=False, scale=0.08, pos=(0.43, 0, .10), command=juego.modo_pantalla, 
                          parent=self.menu, extraArgs=[False])
        ]

        for button in buttons:
            button.setOthers(buttons)

        
        DirectLabel(text = 'Musica', scale = 0.1, pos = (-.5, 0, -0.2), parent = self.menu, 
                        text_fg = (1, 1, 1, 1),frameSize = (-4, 4, -1, 1), text_pos = (0, -0.2))
        self.volumen = DirectSlider(range=(0,100), value=100, pos = (.5, 0, -0.2), pageSize=3, command=juego.musica, scale=0.5, parent=self.menu)


        btn = DirectButton(text = 'Volver al menú', command = juego.menu, pos = (0, 0, -0.6), parent = self.menu, scale = 0.1, 
                        frameSize = (-4, 4, -1, 1), text_scale = 0.75, text_pos = (0, -0.2))
        btn.setTransparency(True)
