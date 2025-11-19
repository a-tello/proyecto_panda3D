from direct.gui.OnscreenImage import OnscreenImage, TextNode
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode
from direct.gui.DirectGui import DirectFrame



class Interfaz():
    def __init__(self, juego):
        #self.fondo = DirectFrame(frameColor = (0, 0, 0, 0), frameSize = (-1, 1, -1, 1), parent = juego.render2d)
        self.juego = juego
        self.vida = juego.jugador.vida_max
        self.nivel = juego.nivel
        self.vecinos_total = juego.niveles[self.nivel]['vecinos']
        self.vecinos_salvados = 0
        self.iconos_vida_true = []
        self.iconos_vida_false = []

    def crear_GUI(self):
        self.cargar_iconos_vida()
        self.puntos_gui = OnscreenText(text = '0', pos = (-1.25, 0.75), mayChange = True, scale=.1, fg=(255,255,255,255), align=TextNode.ALeft)
        self.objetivo_gui = OnscreenText(text = f'0/{self.vecinos_total}', pos = (1.20, 0.8), mayChange = True, scale=0.1, fg=(255,255,255,255))
        self.objetivo_img_activo = OnscreenImage(image = 'assets/GUI/Level/Star/Active.png', pos = (1.05, 0, 0.82), scale = 0.09)
        self.objetivo_img_inactivo = OnscreenImage(image = 'assets/GUI/Level/Star/Unactive.png', pos = (1.05, 0, 0.82), scale = 0.09)
        self.objetivo_img_activo.setTransparency(True)
        self.objetivo_img_inactivo.setTransparency(True)
        self.objetivo_img_activo.hide()
        self.mira = OnscreenText(text = '+', pos = (0,0,0), mayChange = True, scale=.1, fg=(255,255,255,255), align = TextNode.ALeft)

    def actualizar_vida(self, vida):
        self.vida = vida
        for i, icono in enumerate(self.iconos_vida_true):
            if i < self.vida:
                icono.show()
                self.iconos_vida_false[i].hide()
            else:
                self.iconos_vida_false[i].show()

    def actualizar_puntos(self, puntos):
        self.puntos_gui.setText(str(puntos))

    def actualizar_objetivo(self):
        self.vecinos_salvados += 1
        self.objetivo_gui.setText(str(f'{self.vecinos_salvados}/{self.vecinos_total}'))
        if self.vecinos_salvados == self.vecinos_total:
            self.objetivo_img_inactivo.hide()
            self.objetivo_img_activo.show()

    def cargar_iconos_vida(self):
        for i in range(self.vida):
            vida_img_true = OnscreenImage(image = 'assets/objects/vida_completa.png',
                                pos = (-1.25 + i * .06, 0, 0.9), scale=(.04,1,.07))
                                
            vida_img_false = OnscreenImage(image = 'assets/objects/vida_vacia.png',
                                pos=(-1.25 + i * .06, 0, 0.9), scale=(.04,1,.07))
            
            vida_img_true.setTransparency(True)
            vida_img_false.setTransparency(True)
            vida_img_true.hide()
            vida_img_false.hide()
            self.iconos_vida_true.append(vida_img_true)
            self.iconos_vida_false.append(vida_img_false)
    
    def inicializar(self):
        self.objetivo_img_inactivo.hide()
        self.objetivo_img_activo.hide()
        self.vida = self.juego.jugador.vida_max
        self.actualizar_vida(10)
        self.vecinos_salvados = 0
        self.vecinos_total = self.juego.niveles[self.juego.nivel]['vecinos']
        self.objetivo_gui.setText(str(f'{self.vecinos_salvados}/{self.vecinos_total}'))