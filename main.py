import json
from constantes import ESTADO
from gestor_niveles import Nivel
from menu import *
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenImage import OnscreenImage
from direct.interval.LerpInterval import LerpColorScaleInterval
from panda3d.core import WindowProperties, TransparencyAttrib, TextNode
from panda3d.core import CollisionTraverser, CollisionHandlerPusher,CollisionHandlerEvent


class Juego(ShowBase):
    def __init__(self):
        super().__init__()
        
        # FPS
        self.setFrameRateMeter(True)

        # PANTALLA
        self.pantalla = WindowProperties()
        self.pantalla.setSize(800,600)
        self.pantalla.set_fullscreen(False)
        self.pantalla.setTitle('Zombies Ate My Neighbors')
        self.win.requestProperties(self.pantalla)
        
        # MUSICA
        self.musica_menu = self.loader.loadMusic('assets/sounds/menu_music.ogg')
        self.musica_menu.setLoop(True)
        self.musica_volumen = 0.075
        self.musica_menu.setVolume(self.musica_volumen)
        self.musica_menu.play()
        self.musica_final = self.loader.loadMusic('assets/sounds/pantalla_final.ogg')
        self.musica_final.setLoop(True)
        self.musica_final.setVolume(self.musica_volumen)
        
        # SONIDOS
        self.sonido_item = self.loader.loadSfx('assets/sounds/item.ogg')
        self.sonido_item.setVolume(0.03)

        # FONDO
        aspectRatio = self.getAspectRatio()
        self.fondo = OnscreenImage('assets/fondo.jpg', pos=(-.2, -1, 0), scale=(aspectRatio, 1, 1) )
        self.fondo.reparentTo(self.render2d)
        self.fondo.setTransparency(TransparencyAttrib.M_alpha)
        self.fondo.setDepthWrite(False)
        self.fondo.setDepthTest(False)
        self.fondo.setColorScale(1, 1, 1, 0)
        self.aparcer(self.fondo, 6)
        
        self.puntajes = []
    
        # MENU
        self.fuente = self.loader.loadFont('assets/fonts/FEASFBI_.TTF')
        self.menu_principal = MenuPrincipal(self)
        self.menu_principal.menu.setColorScale(1, 1, 1, 0)   
        self.menu_principal.esconder_menu()
        self.menu_opciones = MenuOpciones(self)
        self.menu_opciones.esconder_menu()
        self.menu_pausa = MenuPausa(self)
        self.menu_pausa.esconder_menu()
        self.pantalla_final = None
        self.aparcer(self.menu_principal.menu, 6)
        self.taskMgr.doMethodLater(3, self.inicio, 'show_menu_task')
        self.pantalla_puntos = PantallaPuntajes(self)
        self.pantalla_puntos.esconder_menu()

        # COLISIONES
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        self.cHandler = CollisionHandlerEvent()
        self.cHandler.addInPattern('%fn-into-%in')
        self.cTrav.setRespectPrevTransform(True)

        # CAMARA
        self.disableMouse()

        self.nivel = 0
        self.niveles = [
                        {'nivel': 'Nivel 1\nPánico en el barrio', 'enemigos': 5, 'vecinos': 3, 'mapa': 'assets/maps/lvl1.png', 'musica': 'assets/sounds/lvl1_music.ogg', 'powerups': 3},
                        {'nivel': 'Nivel 2\nUn poco de suerte', 'enemigos': 10, 'vecinos': 1,'mapa': 'assets/maps/lvl2.png', 'musica': 'assets/sounds/lvl2_music.ogg', 'powerups': 7},
                        {'nivel': 'Nivel 3\n¡SALVA A TODOS!', 'enemigos': 20, 'vecinos': 10, 'mapa': 'assets/maps/lvl3.png', 'musica': 'assets/sounds/lvl3_music.ogg', 'powerups': 6}]
                
        self.estado = ESTADO['MENU']
        self.jugador = None
        self.gestor_nivel = None
        self.accept('escape', self.pausa)
        

    def actualizar(self, task):
        '''Actualizacion principal del juego'''
        
        dt = self.clock.getDt()
        
        self.jugador.mover(dt)
        self.gestor_nivel.actualizar_enemigos(dt)
        self.cTrav.traverse(self.render)

        if self.jugador.vida < 1:
            self.terminar_partida('Perdiste. No pudiste salvarlos')

        return task.cont
            

    def jugar(self):
        '''Empieza el juego. Esconde las pantallas y llama al gestor de niveles'''
        
        if self.jugador is not None:
            self.terminar_partida()
        if self.pantalla_final is not None:
            self.pantalla_final.esconder_menu()
        
        self.fondo.hide()
        self.menu_principal.esconder_menu()
        self.pantalla.setCursorHidden(True)
        self.win.requestProperties(self.pantalla)
        self.musica_menu.stop()
        self.musica_final.stop()

        self.gestor_nivel = Nivel(self)
        nivel = self.niveles[self.nivel]
        self.gestor_nivel.cargar(nivel)
        self.estado = ESTADO['JUGANDO']
        self.cargar_pantalla_de_carga()
        self.taskMgr.add(self.actualizar, 'actualizar')

    def impacto(self, colision):
        '''Detecta el impacto de las balas y las elimina'''

        id_enemigo = colision.getIntoNode().getName().split('_')[-1]
        bala_np = colision.getFromNodePath().get_parent()
        bala_np.removeNode()
        
        self.gestor_nivel.impacto_enemigos(id_enemigo)

    def salvar_vecino(self, colision):
        '''Detecta la colision con los vecinos'''

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
        '''Gestiona el menu de pausa'''

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
            
    def volver(self):
        '''Gestion de opcion volver'''

        if self.estado == ESTADO['PAUSA']:
            self.menu_opciones.esconder_menu()
            self.menu_pausa.mostrar_menu()
            self.accept('escape', self.pausa)
        else:
            self.menu()
    
    def aparcer(self, objeto, tiempo):
        '''Efecto para imagen de menu'''

        LerpColorScaleInterval(objeto, tiempo, (1, 1, 1, 1), startColorScale=(1, 1, 1, 0)).start()

    def inicio(self,_):
        '''Gestiona la imagen de inicio de juego'''

        self.menu_principal.mostrar_menu()
        self.aparcer(self.menu_principal.menu, 3)

    def menu(self):
        '''Gestion del menu principal'''

        self.musica_final.stop()
        self.musica_menu.play()
        if self.gestor_nivel is not None:
            self.gestor_nivel.musica_nivel.stop()
        self.fondo.show()
        self.estado = ESTADO['MENU']
        self.menu_opciones.esconder_menu()
        self.menu_pausa.esconder_menu()
        self.pantalla_puntos.esconder_menu()
        if self.pantalla_final is not None:
            self.pantalla_final.esconder_menu()
        self.menu_principal.mostrar_menu()
        
    def opciones(self):
        '''Gestion del menu de opciones'''

        self.fondo.hide()
        if self.estado == ESTADO['PAUSA']:
            self.ignore('escape')
        
        self.menu_principal.esconder_menu()
        self.menu_pausa.esconder_menu()
        self.menu_opciones.mostrar_menu()
        
    def puntuaciones(self):
        '''Gestiona el apartado de puntuaciones'''

        self.fondo.hide()
        self.pantalla_puntos.eliminar_menu()
        self.cargar_puntajes()
        self.pantalla_puntos = PantallaPuntajes(self)
        self.menu_principal.esconder_menu()
        self.pantalla_puntos.mostrar_menu()
        
        
    def cambiar_pantalla(self, op):
        '''Gestiona el cambio de tamaño de la pantalla'''

        ancho, alto = op.split(' x ')
        self.pantalla.setSize(int(ancho), int(alto))
        self.win.requestProperties(self.pantalla)
        
    def modo_pantalla(self, opcion):
        '''Gestiona el modo de pantalla'''

        self.pantalla.set_fullscreen(opcion)
        self.win.requestProperties(self.pantalla)

    def musica(self):
        '''Gestiona el volumen de la musica'''

        volumen = self.menu_opciones.volumen['value'] / 1000
        self.musica_menu.setVolume(volumen)
        self.musica_volumen = volumen
        if self.gestor_nivel is not None:
            self.gestor_nivel.musica_nivel.setVolume(volumen)
        

    # def reiniciar(self):


    #     if self.pantalla_final is not None:
    #         self.pantalla_final.esconder_menu()
    #     #self.jugar()

    def pantalla_fin(self, texto):
        '''Gestiona la pantalla de fin de juego'''

        self.musica_final.play()
        self.pantalla_final = PantallaFinal(juego, self.jugador.puntaje, texto)
        
    
    def terminar_partida(self, texto=''):
        '''Limpia el gestor de niveles y el personaje cuando la partida termina
        Tambien detiene la actualizacion'''

        if self.jugador is not None:
            self.gestor_nivel.musica_nivel.stop()
            self.pantalla_fin(texto)
        self.taskMgr.remove('restaurar-velocidad')
        self.taskMgr.remove('actualizar')
        self.pantalla.setCursorHidden(False)
        self.win.requestProperties(self.pantalla)
        self.jugador.eliminar()
        self.jugador = None
        self.gestor_nivel.limpiar_nivel()
        self.gestor_nivel.gui.menu.removeNode()
        self.gestor_nivel = None
        self.nivel = 0
        self.cargar_puntajes()

        

    def salir(self):
        self.userExit()

    def guardar_puntos(self, info):
        '''Guardado de puntos en un archivo .json'''
        self.puntajes.append(info)
        archivo_nombre = 'puntajes.json'

        with open(archivo_nombre, 'w', encoding='utf-8') as archivo:
            json.dump(self.puntajes, archivo)

        
    def cargar_pantalla_de_carga(self):
        '''Gestiona las pantallas al inicio de cada nivel'''

        self.task_mgr.remove('actualizar')
        self.menu_fondo = DirectFrame(frameColor = (0, 0, 0, 1), frameSize = (-1, 1, -1, 1), parent = juego.render2d)

        self.pantalla_carga = DirectFrame(frameColor = (1, 1, 1, 1), parent = self.render2d)
        texto = TextNode('texto')
        texto.setAlign(TextNode.ACenter)
        texto.setText(self.niveles[self.nivel]['nivel'])
        texto.setFont(self.fuente)
        texto_node = self.render2d.attachNewNode(texto)
        texto_node.setScale(.2)
        texto_node.setPos(0, 0, 0) 
        self.mensaje = texto_node
        
        self.taskMgr.doMethodLater(5.0, self.cargar_nivel, 'cargar-nivel')  

    
    def cargar_nivel(self, task):
        '''Elimina las pantallas al cargar cada nivel'''

        self.pantalla_carga.destroy()
        self.menu_fondo.destroy()
        self.mensaje.removeNode()
        self.gestor_nivel.gui.mostrar()
        
        return task.done

    def cargar_puntajes(self):
        '''Carga los puntajes desde un archivo .json'''
        nombre_archivo = 'puntajes.json'

        try:
            with open(nombre_archivo, 'r') as archivo:
                jugadores = json.load(archivo)
                if jugadores:
                    puntajes = sorted(jugadores, key=lambda x: x['puntos'], reverse=True)[:7]
                else: 
                    puntajes = []    
        except:
            puntajes = []
                       
        self.puntajes = puntajes

juego = Juego()
juego.run()