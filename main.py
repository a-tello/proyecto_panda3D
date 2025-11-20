from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode
from gestor_niveles import Nivel
from menu import *
from panda3d.core import WindowProperties, Point3
from panda3d.core import TransparencyAttrib
from direct.interval.LerpInterval import LerpColorScaleInterval
from objetos import Puerta
from direct.showbase.ShowBase import ShowBase
from constantes import ESTADO
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
        #self.musica_volumen = 0.075
        self.musica_volumen = 0.0
        self.musica_menu.setVolume(self.musica_volumen)
        self.musica_menu.play()

        # SONIDOS
        self.sonido_item = self.loader.loadSfx("assets/sounds/item.ogg")
        self.sonido_item.setVolume(0.03)


        # FONDO
        # aspectRatio = self.getAspectRatio()
        # self.fondo = OnscreenImage("fondo.jpg", pos=(-.2, -1, 0), scale=(aspectRatio, 1, 1) )
        # self.fondo.reparentTo(self.render2d)
        # self.fondo.setTransparency(TransparencyAttrib.M_alpha)
        # self.fondo.setDepthWrite(False)
        # self.fondo.setDepthTest(False)
        # self.fondo.setColorScale(1, 1, 1, 0)
        # self.aparcer(self.fondo, 6)

        # MENU
        self.menu_principal = MenuPrincipal(self)
        # self.menu_principal.menu.setColorScale(1, 1, 1, 0)   
        # self.menu_principal.esconder_menu()
        self.menu_opciones = MenuOpciones(self)
        self.menu_opciones.esconder_menu()
        self.menu_pausa = MenuPausa(self)
        self.menu_pausa.esconder_menu()
        self.pantalla_final = None
        # self.aparcer(self.menu_principal.menu, 8)
        # self.taskMgr.doMethodLater(6, self.inicio, "show_menu_task")

        # COLISIONES
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        self.cHandler = CollisionHandlerEvent()
        self.cHandler_2 = CollisionHandlerEvent()
        self.cHandler.addInPattern('%fn-into-%in')
        self.cHandler_2.addInPattern('%fn-into-%in')
        self.cTrav.setRespectPrevTransform(True)

        # CAMARA
        #self.disableMouse()

        self.nivel = 0
        self.niveles = [
            #{'nivel': 'Nivel 1\nPánico en el vecindario', 'enemigos': 0, 'vecinos': 1, 'mapa': 'test.png', 'musica': 'assets/sounds/lvl1_music.ogg', 'powerups': 5},
            {'nivel': 'Nivel 1\nPánico en el vecindario', 'enemigos': 2, 'vecinos': 1, 'mapa': 'assets/maps/lvl1.png', 'musica': 'assets/sounds/lvl1_music.ogg', 'powerups': 3},
                        {'nivel': 'Nivel 2\nUn poco de suerte', 'enemigos': 10, 'vecinos': 2,'mapa': 'assets/maps/lvl2.png', 'musica': 'assets/sounds/lvl2_music.ogg', 'powerups': 5},
                        {'nivel': 'Nivel 3\n¡SALVA A TODOS!', 'enemigos': 30, 'vecinos': 12, 'mapa': 'assets/maps/lvl3.png', 'musica': 'assets/sounds/lvl3_music.ogg', 'powerups': 7}]
        
        self.estado = ESTADO['MENU']
        self.jugador = None
        self.gestor_nivel = None
        self.accept('escape', self.pausa)

    

    def actualizar(self, task):
        dt = self.clock.getDt()
        
        self.jugador.mover(dt)
        self.gestor_nivel.actualizar_enemigos(dt)
        self.cTrav.traverse(self.render)

        if self.jugador.vida < 1:
            self.terminar_partida()
        #     self.taskMgr.remove('actualizar')
        #     self.pantalla_final = PantallaFinal(juego, self.jugador.puntaje)
        #     self.pantalla.setCursorHidden(False)
        #     self.win.requestProperties(self.pantalla)

        return task.cont
            

    def jugar(self):
        if self.jugador is not None:
            self.terminar_partida()
        if self.pantalla_final is not None:
            self.pantalla_final.esconder_menu()
        #if self.estado == ESTADO['MENU']:
        #self.fondo.hide()
        self.menu_principal.esconder_menu()
        self.pantalla.setCursorHidden(True)
        self.win.requestProperties(self.pantalla)
    # if self.pantalla_final is not None:
    #     self.pantalla_final.esconder_menu()
        self.musica_menu.stop()

        self.gestor_nivel = Nivel(self)
        nivel = self.niveles[self.nivel]
        self.gestor_nivel.cargar(nivel)
        self.estado = ESTADO['JUGANDO']
        self.taskMgr.add(self.actualizar, 'actualizar')
        self.cargar_pantalla_de_carga()

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

    def salvar_vecino(self, colision):
        self.sonido_item.play()
        vecinos = self.gestor_nivel.vecinos

        nombre = colision.getIntoNode().getName()
        self.jugador.actualizar_puntos(vecinos[0].puntos)
        self.gestor_nivel.gui.actualizar_objetivo()
        for vecino in vecinos:
            if vecino.nombre == nombre:
                vecino.eliminar()
                vecinos.remove(vecino)
                break

        if not vecinos:
            self.gestor_nivel.crear_final()

    def pausa(self):
        if self.estado == ESTADO['JUGANDO']:
            self.gestor_nivel.gui.esconder()
            self.pantalla.setCursorHidden(False)
            self.win.requestProperties(self.pantalla)
            self.taskMgr.remove('actualizar')
            self.gestor_nivel.mutear_zombies()
            self.menu_pausa.mostrar_menu()
            self.estado = ESTADO['PAUSA']
            
        elif self.estado == ESTADO['PAUSA']:
            self.pantalla.setCursorHidden(True)
            self.win.requestProperties(self.pantalla)
            self.gestor_nivel.gui.mostrar()
            self.taskMgr.add(self.actualizar, 'actualizar')
            self.menu_pausa.esconder_menu()
            self.estado = ESTADO['JUGANDO']
            
        # elif self.estado == ESTADO['PAUSA_OPC']:
        #     self.ignore('escape')       

    def volver(self):
        if self.estado == ESTADO['PAUSA']:
            self.menu_opciones.esconder_menu()
            self.menu_pausa.mostrar_menu()
            self.accept('escape', self.pausa)
        else:
            self.menu()
    
    def aparcer(self, objeto, tiempo):
        LerpColorScaleInterval(objeto, tiempo, (1, 1, 1, 1), startColorScale=(1, 1, 1, 0)).start()

    def inicio(self,_):
        self.menu_principal.mostrar_menu()
        self.aparcer(self.menu_principal.menu, 3)

    def menu(self):
        self.estado = ESTADO['MENU']
        self.menu_opciones.esconder_menu()
        self.menu_pausa.esconder_menu()
        if self.pantalla_final is not None:
            self.pantalla_final.esconder_menu()
        self.menu_principal.mostrar_menu()
        
    def opciones(self):
        if self.estado == ESTADO['PAUSA']:
            self.ignore('escape')
        
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
        self.musica_volumen = volumen
        

    def reiniciar(self):
        if self.pantalla_final is not None:
            self.pantalla_final.esconder_menu()
        #self.jugar()

    def terminar_partida(self):
        nodos_hijos = render.get_children()
        print(len(nodos_hijos))

        self.taskMgr.remove('actualizar')
        self.pantalla_final = PantallaFinal(juego, self.jugador.puntaje)
        self.pantalla.setCursorHidden(False)
        self.win.requestProperties(self.pantalla)
        self.jugador.eliminar()
        self.jugador = None
        self.gestor_nivel.limpiar_nivel()
        self.gestor_nivel.gui.menu.removeNode()
        self.gestor_nivel = None
        self.nivel = 0

    def salir(self):
        self.userExit()

    def cargar_pantalla_de_carga(self):
        self.task_mgr.remove('actualizar')
        self.menu_fondo = DirectFrame(frameColor = (0, 0, 0, 1), frameSize = (-1, 1, -1, 1), parent = juego.render2d)

        self.pantalla_carga = DirectFrame(frameColor = (1, 1, 1, 1), parent = self.render2d)
        texto_obj = TextNode('texto')
        texto_obj.setText(self.niveles[self.nivel]['nivel'])
        texto_node = self.render2d.attachNewNode(texto_obj)
        texto_node.setScale(0.1)
        texto_node.setPos(0, 0, 0.5) 
        self.mensaje = texto_node
        
        self.taskMgr.doMethodLater(5.0, self.cargar_nivel, 'cargar-nivel')  

    
    def cargar_nivel(self, task):
        self.pantalla_carga.destroy()
        self.menu_fondo.destroy()
        self.mensaje.removeNode()

        self.task_mgr.add(self.actualizar, 'actualizar')
        
        return task.done

juego = Juego()
juego.run()

# Obtener los nodos hijos de render
# nodos_hijos = render.get_children()

# for nodo in nodos_hijos:
#     print(nodo)