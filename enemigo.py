import math
import random
from direct.actor.Actor import Actor
from panda3d.core import Vec3
from panda3d.core import CollisionSphere, CollisionNode, CollisionSegment, CollisionHandlerQueue
from panda3d.core import BitMask32
from panda3d.core import Point2, Point3, Vec3
from direct.gui.OnscreenImage import OnscreenImage

class Enemigo():
    def __init__(self, spawn, juego):
        self.juego = juego
        self.objetivo = self.juego.jugador.personaje
        self.zombie = Actor('assets/models/monkey')
        self.zombie.reparentTo(juego.render)
        self.zombie.setPos(spawn)
        self.zombie.setScale(.5)
        
        # ATRIBUTOS
        self.vida = 10
        self.velocidad = 2
        self.danio = -1
        
        self.distancia_ataque = 1
        self.delay_ataque = 0.5

        # MOVIMIENTO RANDOM
        self.direccion_random = Vec3(random.uniform(-1, 1), random.uniform(-1, 1), 0)
        self.direccion_random.normalize()
        
        # COLISION
        colliderNode = CollisionNode('enemigo')
        colliderNode.addSolid(CollisionSphere(0, 0, 0, 1))
        self.colisionador = self.zombie.attachNewNode(colliderNode)
        self.colisionador.setPythonTag('owner', self)
        mascara = BitMask32()
        mascara.setBit(2)
        self.colisionador.node().setIntoCollideMask(mascara)
        # self.colisionador.node().setFromCollideMask(BitMask32.bit(2))
        # self.colisionador.node().setIntoCollideMask(BitMask32.bit(1))
        
        juego.pusher.addCollider(self.colisionador, self.zombie)
        juego.cTrav.addCollider(self.colisionador, juego.pusher)

        # COLISION DE ATAQUE (nodo)
        self.ataque = CollisionSegment(0,0,0,1,0,0)
        ataque_nodo = CollisionNode('ataque')
        ataque_nodo.addSolid(self.ataque)
        # MASCARA DE COLISION (para no atacar a otros enemigos)
        mascara_ataque = BitMask32()
        mascara_ataque.setBit(1)
        ataque_nodo.setFromCollideMask(mascara_ataque)
        ataque_nodo.setIntoCollideMask(BitMask32().allOff())

        self.ataque_np = juego.render.attachNewNode(ataque_nodo)
        self.ataque_np.show()
        self.lista_ataques = CollisionHandlerQueue()

        juego.cTrav.addCollider(self.ataque_np, self.lista_ataques)



    def mover(self, dt):
        direccion_objetivo = self.objetivo.getPos() - self.zombie.getPos()
        direccion_objetivo.setZ(0)
        distancia = direccion_objetivo.length()

        avance = self.zombie.getPos() + self.direccion_random * self.velocidad * dt


        if distancia < 20:
            direccion_objetivo.normalize()
            velocidad = 3
            avance = self.zombie.getPos() + direccion_objetivo * velocidad * dt

            self.ataque.setPointA(self.zombie.getPos())
            self.ataque.setPointB(self.zombie.getPos() + direccion_objetivo * self.distancia_ataque)
        
            if distancia < self.distancia_ataque:
                self.delay_ataque -= dt
                if self.delay_ataque <= 0:
                    if self.lista_ataques.getNumEntries() > 0:
                        print('Ataque')
                        self.lista_ataques.sortEntries()
                        impacto = self.lista_ataques.getEntry(0)
                        nodo_impacto = impacto.getIntoNodePath()
                        if nodo_impacto.hasPythonTag('owner'):
                            objetivo = nodo_impacto.getPythonTag('owner')
                            objetivo.actualizar_vida(self.danio)
                            self.delay_ataque = 1
        
        else:
            if random.random() < 0.01:  
                self.direccion_random = Vec3(random.uniform(-1, 1), random.uniform(-1, 1), 0)
                self.direccion_random.normalize()

        self.zombie.setPos(avance)