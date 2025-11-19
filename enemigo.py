import math
import random
from constantes import *
from direct.actor.Actor import Actor
from panda3d.core import Vec3, AudioSound
from panda3d.core import CollisionSphere, CollisionNode, CollisionSegment, CollisionHandlerQueue, CollisionBox
from panda3d.core import BitMask32
from panda3d.core import Point2, Point3, Vec3, VBase4
from direct.interval.IntervalGlobal import LerpColorScaleInterval,Sequence

from direct.gui.OnscreenImage import OnscreenImage

class Enemigo():
    def __init__(self, juego, nombre, spawn, identificador, nivel):
        self.juego = juego
        self.nombre = nombre
        self.id = identificador
        self.objetivo = self.juego.jugador.personaje
        self.zombie = Actor('assets/models/zombie1.glb', {'run': 'assets/models/zombie1.glb'})
        self.zombie.getChild(0).setH(180)

        self.zombie.loop('run')
        self.sonido_zombie = juego.loader.loadSfx("assets/sounds/zombie.ogg")
        self.sonido_zombie.setVolume(0.02)
        self.sonido_zombie.setLoop(True)


        self.zombie.reparentTo(juego.render)
        self.zombie.setPos(spawn)
        self.zombie.setScale(1.2)
        self.zombie.setTransparency(True)

        # ATRIBUTOS
        self.vida = 10
        self.velocidad = 2
        self.danio = -1 * (nivel + 1)
        
        self.distancia_ataque = 1.2
        self.delay_ataque = 0.5

        self.puntos = 100

        # MOVIMIENTO RANDOM
        self.direccion_random = Vec3(random.uniform(-1, 1), random.uniform(-1, 1), 0)
        self.direccion_random.normalize()
        
        # COLISION
        zombie_cn = CollisionNode(nombre)
        #zombie_cn.addSolid(CollisionSphere(0, 0, 1, 1))
        zombie_cn.addSolid(CollisionBox(Point3(0, 0, 1), .3, .3, 1))
        self.colisionador = self.zombie.attachNewNode(zombie_cn)
        self.colisionador.node().setIntoCollideMask(BitMask32.bit(2))
        zombie_cn.setFromCollideMask(BitMask32.bit(1) | BitMask32.bit(2))


        self.juego.pusher.addCollider(self.colisionador, self.zombie)
        self.juego.cTrav.addCollider(self.colisionador, self.juego.pusher)
        
        # COLISION (balas)
        zombie_balas_cn = CollisionNode(f'enemigo_balas_{identificador}')
        #zombie_balas_cn.addSolid(CollisionSphere(0, 0, 0, 1))
        zombie_balas_cn.addSolid(CollisionBox(Point3(0, .2, 1), .3, .3, 1))
        self.colisionador_balas = self.zombie.attachNewNode(zombie_balas_cn)
        zombie_balas_cn.setFromCollideMask(BitMask32.allOff())
        zombie_balas_cn.setIntoCollideMask(BitMask32.bit(3))

        self.juego.cTrav.addCollider(self.colisionador_balas, juego.cHandler)

        # COLISION DE ATAQUE (nodo)
        self.ataque = CollisionSegment(0,0.5,1.2,0,3,1.2)
        ataque_cn = CollisionNode('ataque')
        ataque_cn.addSolid(self.ataque)
        self.ataque_np = self.zombie.attachNewNode(ataque_cn)
        #self.ataque_np = juego.render.attachNewNode(ataque_cn)
        # MASCARA DE COLISION (para no atacar a otros enemigos)
        ataque_cn.setFromCollideMask(BitMask32().bit(1))
        ataque_cn.setIntoCollideMask(BitMask32().allOff())

        self.lista_ataques = CollisionHandlerQueue()

        juego.cTrav.addCollider(self.ataque_np, self.lista_ataques)



    def actualizar_vida(self, danio):
        self.vida += danio
        self.zombie.setColorScale(1, 0, 0, 1)  
        color = LerpColorScaleInterval(self.zombie, 0.3, (1, 1, 1, 1)) 
        color.start()
    

    def morir(self):
        self.sonido_zombie.stop()
        self.zombie.stop()
        morir = LerpColorScaleInterval(self.zombie, 2.0, VBase4(1, 1, 1, 0))
        morir.start()
        morir.setDoneEvent("morir_")
        self.juego.accept("morir_", self.eliminar)

    def eliminar(self):
        self.sonido_zombie.stop()
        self.zombie.cleanup()
        self.zombie.removeNode()


    def mover(self, dt):
        self.zombie.lookAt(self.juego.jugador.personaje.getPos())
        direccion_objetivo = self.objetivo.getPos() - self.zombie.getPos()
        direccion_objetivo.setZ(0)
        distancia = direccion_objetivo.length()

        avance = self.zombie.getPos() + self.direccion_random * self.velocidad * dt

        if distancia < 20:
            if self.sonido_zombie.status() != AudioSound.PLAYING:
                self.sonido_zombie.play()
            direccion_objetivo.normalize()
            velocidad = 3
            avance = self.zombie.getPos() + direccion_objetivo * velocidad * dt

            #self.ataque.setPointA(self.zombie.getPos() + Point3(0,0,2))
            #self.ataque.setPointB(Point3(0,0,2) + direccion_objetivo * self.distancia_ataque)
        
            if distancia < self.distancia_ataque:
                self.delay_ataque -= dt
                if self.delay_ataque <= 0:
                    if self.lista_ataques.getNumEntries() > 0:
                        self.lista_ataques.sortEntries()
                        impacto = self.lista_ataques.getEntry(0)
                        nodo_impacto = impacto.getIntoNodePath()
                        if nodo_impacto.hasPythonTag('owner'):
                            objetivo = nodo_impacto.getPythonTag('owner')
                            objetivo.actualizar_vida(self.danio)
                            self.delay_ataque = 0.5
    
        else:
            if self.sonido_zombie.status() == AudioSound.PLAYING:
                self.sonido_zombie.stop()
            if random.random() < 0.01:  
                self.direccion_random = Vec3(random.uniform(-1, 1), random.uniform(-1, 1), 0)
                self.direccion_random.normalize()

        self.zombie.setPos(avance)
        h, p, r = self.zombie.getHpr()  
        self.zombie.setHpr(h, 0, r)