from menu import MenuPrincipal, MenuOpciones
from personaje import Personaje
from enemigo import Enemigo
from nivel import Laberinto, MapaImagen
from panda3d.core import WindowProperties, Vec3
import random

from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DirectLabel, DirectOptionMenu, DirectSlider, DirectRadioButton
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import CollisionTraverser, CollisionHandlerPusher,CollisionHandlerEvent
from direct.actor.Actor import Actor
from panda3d.core import CardMaker, NodePath, TexturePool, TransparencyAttrib


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
        self.mapa = MapaImagen(self, 'assets/maps/lvl1.png')
        #self.mapa = Laberinto(self)

        # ILUMINACION
        ambient = AmbientLight('ambient')
        ambient.setColor((0.5, 0.5, 0.5, 1))
        self.render.setLight(self.render.attachNewNode(ambient))

        dlight = DirectionalLight('dlight')
        dlight.setColor((1, 1, 1, 1))
        self.render.setLight(self.render.attachNewNode(dlight))

        # CAMARA
        self.disableMouse()


        # COLISIONES
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        
        self.cHandler = CollisionHandlerEvent()
        self.cHandler.addInPattern('%fn-into-%in')
        self.cTrav.setRespectPrevTransform(True)
        
        
        # JUGADOR
        self.jugador = Personaje(self)
        
        
        
        # ENEMIGOS
        self.enemigos = []
        self.enemigos_muertos = []
        self.spawn_points = []
        self.enemigos_max = 15
        self.intervalo_spawn = 2
        self.temporizador_spawn = 2
        
        # TEST CARDMAKER
#         cm = CardMaker("myCard")


#         self.card_np = render.attach_new_node(cm.generate())

#         tex = TexturePool.load_texture("z-Photoroom.png")

#         self.card_np.set_texture(tex)
#         self.card_np.setPos(7, 7, 0) 
#         self.card_np.setScale(2)
# #        self.card_np.reparentTo(render)
#         self.card_np.setTransparency(TransparencyAttrib.MAlpha)
#         #self.card_np.setBillboardPointEye()
#         self.card_np.setTwoSided(True)
        
                
        


    def actualizar(self, task):
        dt = self.clock.getDt()
        #self.card_np.lookAt(self.jugador.personaje)
        
        self.jugador.mover(dt)
        
        self.temporizador_spawn -= dt
        if self.temporizador_spawn <= 0:
            self.temporizador_spawn = self.intervalo_spawn
            self.spawnear_enemigo()
        
        for enemigo in self.enemigos:
            enemigo.mover(dt)
        
        self.cTrav.traverse(self.render)
        return task.cont

    def jugar(self):
        self.menu_principal.esconder_menu()
        self.pantalla.setCursorHidden(True)
        self.win.requestProperties(self.pantalla)
        self.buscar_spawns()
        self.taskMgr.add(self.actualizar, 'actualizar')

    def buscar_spawns(self):
        print(self.mapa.mapa)
        alto = len(self.mapa.mapa)
        ancho = len(self.mapa.mapa[0])

        for y in range(alto):
            for x in range(ancho):
                if self.mapa.mapa[y][x] == 0:
                    self.spawn_points.append(Vec3(x, y, 1))
    
    def spawnear_enemigo(self):
        if len(self.enemigos) < self.enemigos_max:
            spawn = random.choice(self.spawn_points)
            enemigo = Enemigo(spawn, self)

            self.enemigos.append(enemigo)
          
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