from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode
from gestor_niveles import Nivel
from menu import *
from panda3d.core import WindowProperties, Point3

from direct.showbase.ShowBase import ShowBase

from panda3d.core import CollisionTraverser, CollisionHandlerPusher,CollisionHandlerEvent, CollisionNode, CollisionBox


class Juego(ShowBase):
    def __init__(self):
        super().__init__()
        
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
                        {'nivel': 'Nivel 2\nUn poco de suerte', 'enemigos': 20, 'vecinos': 1,'mapa': 'assets/maps/lvl2.png', 'musica': 'assets/sounds/lvl2_music.ogg'},
                        {'nivel': 'Nivel 3\n¡SALVA A TODOS!', 'enemigos': 30, 'vecinos': 12, 'mapa': 'assets/maps/lvl3.png', 'musica': 'assets/sounds/lvl3_music.ogg'}]
        
        self.jugador = None
        
                 
    def impacto(self, a):
        enemigos = self.gestor_nivel.enemigos
        enemigos_muertos = self.gestor_nivel.enemigos_muertos
        id_enemigo = a.getIntoNode().getName().split('_')[-1]
        bala_np = a.getFromNodePath().get_parent()
        bala_np.removeNode()
        for enemigo in enemigos:
            if id_enemigo == str(enemigo.id):
                enemigo.actualizar_vida(-self.jugador.ataque)
                if enemigo.vida < 1:
                    enemigos.remove(enemigo)
                    enemigos_muertos.append(enemigo)
                    enemigo.morir()

    def actualizar(self, task):
        print(self.nivel)
        dt = self.clock.getDt()
        
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

        self.musica_menu.stop()
        self.gestor_nivel = Nivel(self)
        nivel = self.niveles[self.nivel]
        self.gestor_nivel.cargar(nivel)

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
            puerta = self.loader.loadModel('models/box')
            puerta.reparentTo(self.render)
            x, y, z = self.gestor_nivel.jugador_spawn
            puerta.setPos(x,y,z)
            puerta.setScale(2,2,2)
            puerta.lookAt(self.jugador.personaje)
            puerta.setColor(1, 1, 1, 1)

            cn_puerta = CollisionNode('puerta')
            cn_puerta.addSolid(CollisionBox(Point3(.5, .5, .5), .5, .5, .5))
            colisionador_puerta = puerta.attachNewNode(cn_puerta)
            colisionador_puerta.show()

            self.pusher.addCollider(colisionador_puerta, puerta)
            self.cTrav.addCollider(colisionador_puerta, self.cHandler)
            self.accept(f'personaje_obj-into-puerta', self.gestor_nivel.pasar_nivel)



        
            
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
        volumen = self.menu_opciones.volumen['value'] / 1000
        self.musica_menu.setVolume(volumen)

    def salir(self):
        self.userExit()


juego = Juego()
juego.run()