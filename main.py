from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode

from menu import MenuPrincipal, MenuOpciones
from personaje import Personaje
from enemigo import Enemigo
from vecino import Vecino
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
        self.cHandler_2 = CollisionHandlerEvent()
        self.cHandler.addInPattern('%fn-into-%in')
        self.cHandler_2.addInPattern('%fn-into-%in')
        self.cTrav.setRespectPrevTransform(True)
        
        
        # JUGADOR
        self.sp_jugador = Vec3()
        
        
        
        # ENEMIGOS
        self.enemigos = []
        self.enemigos_muertos = []
        self.sp_enemigos = []
        self.enemigos_max = 15
        self.intervalo_spawn = 2
        self.temporizador_spawn = 2
        self.zombie_pusher = CollisionHandlerPusher()
        
        
        # VECINOS
        self.vecinos = []
        self.cantidad_vecinos = 5
        self.sp_vecinos = []
        
        # ENTORNO
        self.mapa = MapaImagen(self, 'assets/maps/lvl1_1.png')
        #self.mapa = Laberinto(self)
        
        self.jugador = Personaje(self)
        
        
        self.accept(f'bala-into-enemigo_balas', self.impacto)
                 
    def impacto(self, a):
        nombre = a.getIntoNode().getName()
        bullet_np = a.getFromNodePath().get_parent()
        enemy_np = a.getIntoNodePath().get_parent()
        bullet_np.removeNode()
        for enemigo in self.enemigos:
            if nombre == enemigo.nombre:
                print('por favor')
                self.enemigos.remove(enemy_np)
                enemy_np.removeNode()

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
        self.spawnear_vecinos()
        
        OnscreenText(text = '+', pos = (0,0,0), mayChange = True, scale=.1, fg=(255,255,255,255), align = TextNode.ALeft)

        #self.buscar_spawns()
        self.taskMgr.add(self.actualizar, 'actualizar')

    # def buscar_spawns(self):
    #     print(self.mapa.mapa)
    #     alto = len(self.mapa.mapa)
    #     ancho = len(self.mapa.mapa[0])

    #     for y in range(alto):
    #         for x in range(ancho):
    #             if self.mapa.mapa[y][x] == 0:
    #                 self.sp_enemigos.append(Vec3(x, y, 1))
    
    def spawnear_enemigo(self):
        if len(self.enemigos) < self.enemigos_max:
            spawn = random.choice(self.sp_enemigos)
            enemigo = Enemigo(self, f'enemigo_{len(self.enemigos)}', spawn)
            self.enemigos.append(enemigo)
            
    def spawnear_vecinos(self):
        for i in range(self.cantidad_vecinos):
            spawn = random.choice(self.sp_vecinos)
            modelo = random.randint(1,5)
            nombre = f'vecino_{i}'
            vecino = Vecino(self, str(modelo), spawn, nombre)
            self.vecinos.append(vecino)
            self.sp_vecinos.remove(spawn)
            self.accept(f'personaje_obj-into-{nombre}', self.limpiar)
            
    def limpiar(self, colision):
        nombre = colision.getIntoNode().getName()
        self.jugador.actualizar_puntos(self.vecinos[0].puntos)
        for vecino in self.vecinos:
            if vecino.nombre == nombre:
                vecino.eliminar()
                self.vecinos.remove(vecino)
                break
            
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