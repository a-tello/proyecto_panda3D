from menu import MenuPrincipal, MenuOpciones
from personaje import Personaje

from panda3d.core import WindowProperties


from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DirectLabel, DirectOptionMenu, DirectSlider, DirectRadioButton
from direct.actor.Actor import Actor
class Juego(ShowBase):
    def __init__(self):
        super().__init__()
        
        # PANTALLA
        self.pantalla = WindowProperties()
        self.pantalla.setSize(800,600)
        self.pantalla.set_fullscreen(False)
        self.win.requestProperties(self.pantalla)
        
        # MENU
        self.menu_principal = MenuPrincipal(self)
        self.menu_opciones = MenuOpciones(self)
        self.menu_opciones.esconder_menu()

        # ENTORNO
        self.entorno = self.loader.loadModel('assets/Environment/environment')
        self.entorno.reparentTo(self.render) 

        # CAMARA
        self.disableMouse()


        # JUGADOR
        self.jugador = Personaje(self)

    def actualizar(self, task):
        dt = globalClock.getDt()
        self.jugador.mover(dt)

        return task.cont

    def jugar(self):
        self.menu_principal.esconder_menu()
        self.taskMgr.add(self.actualizar, 'actualizar')

        
    def menu(self):
        self.menu_opciones.esconder_menu()
        self.menu_principal.mostrar_menu()
        
    def opciones(self):
        self.menu_principal.esconder_menu()
        self.menu_opciones.mostrar_menu()
        
    def cambiar_pantalla(self, op):
        ancho, alto = op.split(' x ')
        self.pantalla.setSize(int(ancho), int(alto))
        self.win.requestProperties(self.pantalla)
        
    def modo_pantalla(self, opcion):
        self.pantalla.set_fullscreen(opcion)
        self.win.requestProperties(self.pantalla)

    def musica(self):
        print(self.menu_opciones.volumen['value'])

    def salir(self):
        self.userExit()


juego = Juego()
juego.run()