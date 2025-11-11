from menu import MenuPrincipal, MenuOpciones
from personaje import Personaje, Enemigo
from nivel import Nivel
from panda3d.core import WindowProperties


from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DirectLabel, DirectOptionMenu, DirectSlider, DirectRadioButton
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
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
        self.mapa = Nivel(self)

        # ILUMINACION
        ambient = AmbientLight('ambient')
        ambient.setColor((0.5, 0.5, 0.5, 1))
        self.render.setLight(self.render.attachNewNode(ambient))

        dlight = DirectionalLight('dlight')
        dlight.setColor((1, 1, 1, 1))
        self.render.setLight(self.render.attachNewNode(dlight))

        # CAMARA
        self.disableMouse()

        # JUGADOR
        self.jugador = Personaje(self)
        self.enemigo = Enemigo(self)

        # COLISIONES
        self.traverser = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(self.jugador.colision, self.jugador.personaje)
        self.traverser.addCollider(self.jugador.colision, self.pusher)
        self.pusher.setHorizontal(True)

    def actualizar(self, task):
        dt = self.clock.getDt()
        self.jugador.mover(dt)
        self.enemigo.mover(dt)
        self.traverser.traverse(self.render)
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