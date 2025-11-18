from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode
from gestor_niveles import Nivel
from menu import *
from panda3d.core import WindowProperties, Point3
from objetos import Puerta
from direct.showbase.ShowBase import ShowBase

from panda3d.core import CollisionTraverser, CollisionHandlerPusher,CollisionHandlerEvent, CollisionNode, CollisionBox


class Juego(ShowBase):
    def __init__(self):
        super().__init__()
        
        # TEST RENDIMIENTO
        self.setFrameRateMeter(True)

        # PANTALLA
        self.pantalla = WindowProperties()
        self.pantalla.setSize(800,600)
        self.pantalla.set_fullscreen(False)
        self.win.requestProperties(self.pantalla)
        
        # MUSICA
        self.musica_menu = self.loader.loadMusic("assets/sounds/menu_music.ogg")
        self.musica_menu.setLoop(True)
        self.musica_menu.setVolume(0.075)
        self.musica_menu.play()

        # SONIDOS
        self.sonido_item = self.loader.loadSfx("assets/sounds/item.ogg")
        self.sonido_item.setVolume(0.03)

        # MENU
        self.menu_principal = MenuPrincipal(self)
        self.menu_opciones = MenuOpciones(self)
        self.menu_opciones.esconder_menu()
        self.menu_pausa = MenuPausa(self)
        self.menu_pausa.esconder_menu()
        self.pantalla_final = None

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
        self.niveles = [{'nivel': 'Nivel 1\nPánico en el vecindario', 'enemigos': 1, 'vecinos': 1, 'mapa': 'assets/maps/lvl1.png', 'musica': 'assets/sounds/lvl1_music.ogg'},
                        {'nivel': 'Nivel 2\nUn poco de suerte', 'enemigos': 0, 'vecinos': 1,'mapa': 'assets/maps/lvl2.png', 'musica': 'assets/sounds/lvl2_music.ogg'},
                        {'nivel': 'Nivel 3\n¡SALVA A TODOS!', 'enemigos': 30, 'vecinos': 12, 'mapa': 'assets/maps/lvl3.png', 'musica': 'assets/sounds/lvl3_music.ogg'}]
        
        self.estado = 0
        self.jugador = None
        self.accept('escape', self.pausa)
        
        
                 
    def impacto(self, colision):
        # enemigos = self.gestor_nivel.enemigos
        # enemigos_muertos = self.gestor_nivel.enemigos_muertos
        id_enemigo = colision.getIntoNode().getName().split('_')[-1]
        bala_np = colision.getFromNodePath().get_parent()
        bala_np.removeNode()
        
        
        self.gestor_nivel.impacto_enemigos(id_enemigo)
        # for enemigo in enemigos:
        #     if id_enemigo == str(enemigo.id):
        #         enemigo.actualizar_vida(-self.jugador.ataque)
        #         if enemigo.vida < 1:
        #             enemigos.remove(enemigo)
        #             enemigos_muertos.append(enemigo)
        #             enemigo.morir()

    def actualizar(self, task):
        print(self.estado)
        dt = self.clock.getDt()
        
        self.jugador.mover(dt)
        self.gestor_nivel.actualizar_enemigos(dt)
        self.cTrav.traverse(self.render)

        if self.jugador.vida < 1:
            self.taskMgr.remove('actualizar')
            self.gestor_nivel.limpiar_nivel()
            self.jugador.personaje.removeNode()
            self.pantalla_final = PantallaFinal(juego, self.jugador.puntaje)
            self.jugador = None
            self.pantalla.setCursorHidden(False)
            self.win.requestProperties(self.pantalla)


        return task.cont

    def jugar(self):
        self.menu_principal.esconder_menu()
        self.pantalla.setCursorHidden(True)
        self.win.requestProperties(self.pantalla)
        if self.pantalla_final is not None:
            self.pantalla_final.esconder_menu()

        OnscreenText(text = '+', pos = (0,0,0), mayChange = True, scale=.1, fg=(255,255,255,255), align = TextNode.ALeft)

        self.musica_menu.stop()
        self.gestor_nivel = Nivel(self)
        nivel = self.niveles[self.nivel]
        self.gestor_nivel.cargar(nivel)
        self.estado = 1
        self.taskMgr.add(self.actualizar, 'actualizar')
            
    def salvar_vecino(self, colision):
        self.sonido_item.play()
        vecinos = self.gestor_nivel.vecinos

        nombre = colision.getIntoNode().getName()
        self.jugador.actualizar_puntos(vecinos[0].puntos)
        for vecino in vecinos:
            if vecino.nombre == nombre:
                vecino.eliminar()
                vecinos.remove(vecino)
                break

        if not vecinos:
            self.gestor_nivel.crear_final()

    def pausa(self):
        if self.estado == 1:
            self.pantalla.setCursorHidden(False)
            self.win.requestProperties(self.pantalla)
            self.taskMgr.remove('actualizar')
            self.menu_pausa.mostrar_menu()
            self.estado = 2
        elif self.estado == 2:
            self.pantalla.setCursorHidden(True)
            self.win.requestProperties(self.pantalla)
            self.taskMgr.add(self.actualizar, 'actualizar')
            self.menu_pausa.esconder_menu()
            self.estado = 1
        elif self.estado == 3:
            self.menu_pausa.mostrar_menu()
            self.menu_opciones.esconder_menu()
            self.estado = 2
            
        
    def menu(self):
        self.estado = 0
        self.menu_opciones.esconder_menu()
        self.menu_pausa.esconder_menu()
        if self.pantalla_final is not None:
            self.pantalla_final.esconder_menu()
        self.menu_principal.mostrar_menu()
        
    def opciones(self):
        self.estado = 3
        self.menu_principal.esconder_menu()
        self.menu_pausa.esconder_menu()
        self.menu_opciones.mostrar_menu()
        
    def cambiar_pantalla(self, op):
        ancho, alto = op.split(' x ')
        self.pantalla.setSize(int(ancho), int(alto))
        self.win.requestProperties(self.pantalla)
        
    def modo_pantalla(self, opcion):
        self.pantalla.set_fullscreen(opcion)
        self.win.requestProperties(self.pantalla)

    def musica(self):
        volumen = self.menu_opciones.volumen['value'] / 1000
        self.musica_menu.setVolume(volumen)

    def salir(self):
        self.userExit()


juego = Juego()
juego.run()