from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode
from gestor_niveles import Nivel
from menu import *
from personaje import Personaje
from enemigo import Enemigo
from vecino import Vecino
from nivel import Laberinto, MapaImagen
from panda3d.core import WindowProperties, Vec3, Point3
import random

from direct.showbase.ShowBase import ShowBase
from direct.gui.DirectGui import DirectFrame, DirectButton, DirectLabel, DirectOptionMenu, DirectSlider, DirectRadioButton

from panda3d.core import CollisionTraverser, CollisionHandlerPusher,CollisionHandlerEvent, CollisionNode, CollisionBox
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

        # COLISIONES
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        self.cHandler = CollisionHandlerEvent()
        self.cHandler_2 = CollisionHandlerEvent()
        self.cHandler.addInPattern('%fn-into-%in')
        self.cHandler_2.addInPattern('%fn-into-%in')
        self.cTrav.setRespectPrevTransform(True)

        # CAMARA
        self.disableMouse()

        self.nivel = 0
        self.niveles = [{'nivel': 'Nivel 1\nPánico en el vecindario', 'enemigos': 10, 'vecinos': 5, 'mapa': 'assets/maps/lvl1.png'},
                        {'nivel': 'Nivel 2\nUn poco de suerte', 'enemigos': 20, 'vecinos': 1,'mapa': 'assets/maps/lvl2.png'},
                        {'nivel': 'Nivel 3\n¡SALVA A TODOS!', 'enemigos': 30, 'vecinos': 15, 'mapa': 'assets/maps/lvl3.png'}]
        
        self.jugador = None
                 
    def impacto(self, a):
        enemigos = self.gestor_nivel.enemigos
        enemigos_muertos = self.gestor_nivel.enemigos_muertos
        id_enemigo = a.getIntoNode().getName().split('_')[-1]
        bala_np = a.getFromNodePath().get_parent()
        #enemigo_np = a.getIntoNodePath().get_parent()
        bala_np.removeNode()
        for enemigo in enemigos:
            if id_enemigo == str(enemigo.id):
                enemigo.actualizar_vida(-self.jugador.ataque)
                if enemigo.vida < 1:
                    enemigos.remove(enemigo)
                    enemigos_muertos.append(enemigo)
                    enemigo.morir()
                    #enemigo.eliminar()
                    #enemigo_np.removeNode()

    def actualizar(self, task):
        dt = self.clock.getDt()
        #self.card_np.lookAt(self.jugador.personaje)
        
        self.jugador.mover(dt)
        
        
        
        self.gestor_nivel.actualizar_enemigos(dt)
        

        self.cTrav.traverse(self.render)

        if self.jugador.vida < 1:
            self.taskMgr.remove('actualizar')
            pantalla_final = PantallaFinal(juego, self.jugador.puntaje)


        return task.cont

    def jugar(self):
        self.menu_principal.esconder_menu()
        self.pantalla.setCursorHidden(True)
        self.win.requestProperties(self.pantalla)

        OnscreenText(text = '+', pos = (0,0,0), mayChange = True, scale=.1, fg=(255,255,255,255), align = TextNode.ALeft)

        self.gestor_nivel = Nivel(self)
        nivel = self.niveles[self.nivel]
        self.gestor_nivel.cargar(nivel)

        self.taskMgr.add(self.actualizar, 'actualizar')

    
    # def spawnear_enemigo(self):
    #     if len(self.enemigos) < self.enemigos_max:
    #         spawn = random.choice(self.sp_enemigos)
    #         enemigo = Enemigo(self, f'enemigo_{self.enemigos_id}', spawn, self.enemigos_id)
    #         self.enemigos.append(enemigo)
    #         self.accept(f'bala-into-enemigo_balas_{self.enemigos_id}', self.impacto)
    #         self.enemigos_id += 1


    # def spawnear_vecinos(self):
    #     for i in range(self.cantidad_vecinos):
    #         spawn = random.choice(self.vecinos_spawn)
    #         modelo = random.randint(1,5)
    #         nombre = f'vecino_{i}'
    #         vecino = Vecino(self, str(modelo), spawn, nombre)
    #         self.vecinos.append(vecino)
    #         self.vecinos_spawn.remove(spawn)
    #         self.accept(f'personaje_obj-into-{nombre}', self.limpiar)
            
    def limpiar(self, colision):
        vecinos = self.gestor_nivel.vecinos

        nombre = colision.getIntoNode().getName()
        self.jugador.actualizar_puntos(vecinos[0].puntos)
        for vecino in vecinos:
            if vecino.nombre == nombre:
                vecino.eliminar()
                vecinos.remove(vecino)
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