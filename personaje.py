import math
import random
from constantes import *
from direct.actor.Actor import Actor
from panda3d.core import Vec3
from panda3d.core import CollisionSphere, CollisionNode, CollisionHandlerPusher, CollisionHandlerQueue
from panda3d.core import BitMask32
from panda3d.core import Point2, Point3, Vec3
from direct.gui.OnscreenImage import OnscreenImage
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode

class Personaje():
    def __init__(self, juego):
        
        self.juego = juego
        
        
        self.personaje = Actor('assets/models/act_p3d_chan', {
                            'stand' : 'assets/models/a_p3d_chan_idle',
                            'run' : 'assets/models/a_p3d_chan_run'
                        })
        self.personaje.setPos(juego.sp_jugador)
        self.personaje.getChild(0).setH(180)
        self.personaje.reparentTo(self.juego.render)
        self.personaje.loop('stand')

        # ATRIBUTOS
        self.vida = 10
        self.velocidad = 5
        self.ataque = 3

        # TECLAS
        self.teclas = {'adelante': False, 'atras': False, 'izquierda': False, 'derecha': False, 'usar': False, 'disparar': False}

        self.juego.accept('w', self.actualizar_tecla, ['adelante', True])
        self.juego.accept('w-up', self.actualizar_tecla, ['adelante', False])
        self.juego.accept('s', self.actualizar_tecla, ['atras', True])
        self.juego.accept('s-up', self.actualizar_tecla, ['atras', False])
        self.juego.accept('a', self.actualizar_tecla, ['izquierda', True])
        self.juego.accept('a-up', self.actualizar_tecla, ['izquierda', False])
        self.juego.accept('d', self.actualizar_tecla, ['derecha', True])
        self.juego.accept('d-up', self.actualizar_tecla, ['derecha', False])
        self.juego.accept('e', self.actualizar_tecla, ['usar', True])
        self.juego.accept('e-up', self.actualizar_tecla, ['usar', False])
        self.juego.accept('mouse1', self.actualizar_tecla, ['disparar', True])
        self.juego.accept('mouse1-up', self.actualizar_tecla, ['disparar', False])


        # CAMARA 
        # juego.cam.setPos(0, -2, 20)
        # juego.cam.setP(-90)
        juego.cam.setPos(0, -2, 1)  
        juego.cam.node().getLens().setFov(80)
        self.angulo_horizontal = 0  
        self.angulo_vertical = 0  
        self.ultimo_x = self.juego.win.getPointer(0).getX()
        self.ultimo_Y = self.juego.win.getPointer(0).getY()
        self.velocidad = 5
        self.velocidad_rotacion = 120.0
        self.sensibilidad_mouse = 0.3
        self.puntaje = 0

        # COLISION (con paredes y enemigos)
        cn_jugador = CollisionNode('personaje')
        cn_jugador.addSolid(CollisionSphere(0, 0, 1, .3))
        self.colisionador = self.personaje.attachNewNode(cn_jugador)
        self.colisionador.setPythonTag('owner', self)

        #  MASCARA DE COLIISON (contra enemigos y paredes)
        self.colisionador.node().setFromCollideMask(BIT_PAREDES | BIT_ENEMIGOS)
        self.colisionador.node().setIntoCollideMask(BIT_JUGADOR)
#        self.colisionador.node().setFromCollideMask(BitMask32.allOff())

        self.personaje_pusher = CollisionHandlerPusher()
        self.personaje_pusher.addCollider(self.colisionador, self.personaje)
        #juego.pusher.addCollider(self.colisionador, self.personaje)
        #juego.cTrav.addCollider(self.colisionador, juego.pusher)
        juego.cTrav.addCollider(self.colisionador, self.personaje_pusher)
        
        
        # COLISION (con NPCs y objetos)
        cn_jugador_obj = CollisionNode('personaje_obj')
        cn_jugador_obj.addSolid(CollisionSphere(0, 0, 1, .3))
        self.colisionador_obj = self.personaje.attachNewNode(cn_jugador_obj)
        self.colisionador_obj.node().setFromCollideMask(BIT_NPCs | BIT_OBJETOS)
        self.colisionador_obj.node().setIntoCollideMask(BIT_ENEMIGOS)

        juego.cTrav.addCollider(self.colisionador_obj, juego.cHandler)
        
        # PUNTAJE
        self.scoreUI = OnscreenText(text = '0',
                            pos = (-1.28, .75),
                            mayChange = True,
                            scale=.1,
                            fg=(255,255,255,255),
                            align = TextNode.ALeft)

        
        # DISPAROS
        # self.bala = CollisionRay(0, 0, 0, 0, 1, 0)
        # bala_nodo = CollisionNode('bala')
        # bala_nodo.addSolid(self.bala)
        
        # self.bala_np = juego.render.attachNewNode(bala_nodo)
        # self.bala_np.setPos(self.juego.cam, 0, 0, 1.5)
        # self.bala_np.setQuat(self.juego.cam.getQuat(render))
        # self.bala_lista = CollisionHandlerQueue()
        
        # self.juego.cTrav.addCollider(self.bala_np, self.bala_lista)
        
        
        
        
        
        # mask = BitMask32()
        # mask.setBit(1)

        # self.colision.node().setIntoCollideMask(mask)

        # mask = BitMask32()
        # mask.setBit(1)

        # self.colision.node().setFromCollideMask(mask)

        # mask = BitMask32()
        # mask.setBit(2)
        # bala_nodo.setFromCollideMask(mask)

        # mask = BitMask32()
        # bala_nodo.setIntoCollideMask(mask)
        
        
        # self.bala_modelo = self.juego.loader.loadModel('assets/laser/bambooLaser')
        # self.bala_modelo.reparentTo(self.personaje)
        # self.bala_modelo.setZ(1.5)
        # self.bala_modelo.setLightOff()
        # self.bala_modelo.hide()
        self.balas_activas = []
        self.cooldown = 0
        


        self.iconos_vida_true = []
        self.iconos_vida_false = []
        for i in range(self.vida):
            vida_img_true = OnscreenImage(image = 'vida_completa.png',
                                pos = (-1.25 + i * .06, 0, .9), scale=(.04,1,.07))
                                
            vida_img_false = OnscreenImage(image = 'vida_vacia.png',
                                pos=(-1.25 + i * .06, 0, .9), scale=(.04,1,.07))
            
            vida_img_true.setTransparency(True)
            vida_img_false.setTransparency(True)
            vida_img_true.hide()
            vida_img_false.hide()
            self.iconos_vida_true.append(vida_img_true)
            self.iconos_vida_false.append(vida_img_false)
                

    def actualizar_tecla(self, tecla, estado):
        self.teclas[tecla] = estado

    def actualizar_vida(self, danio):
        print(self.vida)
        self.vida += danio
        for i, icono in enumerate(self.iconos_vida_true):
            if i < self.vida:
                icono.show()
            else:
                self.iconos_vida_false[i].show()

    def mover(self, dt):
        self.actualizar_vida(0)
        # MOVIMIENTO CAMARA
        if self.juego.mouseWatcherNode.hasMouse():
            x = self.juego.win.getPointer(0).getX()
            y = self.juego.win.getPointer(0).getY()

            delta_x = x - self.ultimo_x
            delta_y = y - self.ultimo_Y

            self.angulo_horizontal = self.personaje.getH() - delta_x * self.sensibilidad_mouse
            self.angulo_vertical += -delta_y * self.sensibilidad_mouse * self.sensibilidad_mouse
            self.angulo_vertical = max(-90, min(90, self.angulo_vertical))
            self.juego.win.movePointer(0, self.juego.win.getXSize()//2, self.juego.win.getYSize()//2)

            winX = int(self.juego.win.getXSize() / 2)
            winY = int(self.juego.win.getYSize() / 2)
            self.juego.win.movePointer(0, winX, winY)

            self.ultimo_x = self.juego.win.getPointer(0).getX()
            self.ultimo_Y = self.juego.win.getPointer(0).getY()


        # MOVIMIENTO PERSONAJE
        rad = math.radians(self.angulo_horizontal)
        movimiento_adelante = Vec3(-math.sin(rad), math.cos(rad), 0)
        movimiento_derecha = Vec3(math.cos(rad), math.sin(rad), 0)
        
        distancia = Vec3(0, 0, 0)
        self.movimiento = False

        if self.teclas['adelante']: 
            distancia += movimiento_adelante
            self.movimiento = True
        if self.teclas['atras']: 
            distancia -= movimiento_adelante
            self.movimiento = True
        if self.teclas['izquierda']: 
            distancia -= movimiento_derecha
            self.movimiento = True
        if self.teclas['derecha']: 
            distancia += movimiento_derecha
            self.movimiento = True

        if distancia.length() > 0:
            distancia.normalize()
            self.personaje.setPos(self.personaje.getPos() + distancia * dt * self.velocidad)

        # GIRAR PERSONAJE Y CAMARA
        self.personaje.setH(self.angulo_horizontal)
        self.movimiento_camara()

        # ANIMACION
        if self.movimiento:
            animacion_quieto = self.personaje.getAnimControl('stand')
            animacion_caminar = self.personaje.getAnimControl('run')

            if animacion_quieto and animacion_quieto.isPlaying():
                animacion_quieto.stop()

            if animacion_caminar and not animacion_caminar.isPlaying():
                self.personaje.loop('run')
        else:
            animacion_quieto = self.personaje.getAnimControl('stand')
            if animacion_quieto and not animacion_quieto.isPlaying():
                self.personaje.stop('run')
                self.personaje.loop('stand')  
                
                
        if self.teclas['disparar'] and self.cooldown <= 0:                              
        #     if self.bala_lista.getNumEntries() > 0:
        #         self.bala_lista.sortEntries()
        #         impacto = self.bala_lista.getEntry(0)
        #         hitPos = impacto.getSurfacePoint(self.juego.render)

        #         hitNodePath = impacto.getIntoNodePath()
        #         print (hitNodePath)
        #         if hitNodePath.hasPythonTag('owner'):
        #             hitObject = hitNodePath.getPythonTag('owner')
        #             hitObject.alterHealth(5*dt)

                
        #         beamLength = (hitPos - self.personaje.getPos()).length()
        #         self.bala_modelo.setSy(beamLength)

        #         self.bala_modelo.show()
        # else:
        #     self.bala_modelo.hide()
        
            bala = loader.loadModel('assets/laser/bambooLaser')   
            bala.setScale(2)
            bala.reparentTo(self.juego.render)
            bala.setPos(self.personaje.getPos())     
            bala.setHpr(self.personaje.getHpr())    

            self.balas_activas.append({'modelo': bala, 'velocidad': 50})
            print(self.balas_activas,'\n')
            self.cooldown = 0.3  
        
        for bala in self.balas_activas:
            modelo = bala['modelo']
            modelo.setY(modelo, bala['velocidad'] * dt)  

            bala_nodo = modelo.attachNewNode(CollisionNode('bala'))
            bala_nodo.node().addSolid(CollisionSphere(0, 0, 0, 0.2))
            bala_nodo.node().setFromCollideMask(BitMask32.bit(1))
            bala_nodo.node().setIntoCollideMask(BitMask32.allOff())
            self.juego.cTrav.traverse(self.juego.render)
            
        for bala in self.balas_activas[:]:
            modelo = bala['modelo']
            modelo.setY(modelo, bala['velocidad'] * dt)

            if (modelo.getPos() - self.personaje.getPos()).length() > 200:
                modelo.removeNode()
                self.balas_activas.remove(bala)
            
        if self.cooldown > 0:
            self.cooldown -= dt
                    
    
    def movimiento_camara(self):
        personaje_pos = self.personaje.getPos()
        self.juego.camera.setPos(personaje_pos + Vec3(0, 0, 1.2))
        self.juego.camera.setHpr(self.angulo_horizontal, self.angulo_vertical, 0)




        


