import math
import random
from constantes import *
from direct.actor.Actor import Actor
from panda3d.core import Vec3
from panda3d.core import CollisionSphere, CollisionNode, CollisionSegment, CollisionHandlerQueue
from panda3d.core import BitMask32
from panda3d.core import Point2, Point3, Vec3
from direct.gui.OnscreenImage import OnscreenImage

class Vecino():
    def __init__(self, juego, tipo, pos, nombre):
        self.modelos = {'1':'assets/models/boss.glb', '2':'assets/models/boss.glb', '3':'assets/models/boss.glb', '4':'assets/models/boss.glb', '5':'assets/models/boss.glb'}
        self.vecino = Actor(self.modelos[tipo], {'idle': self.modelos[tipo], 'action': self.modelos[tipo]})
        self.vecino.setPos(pos)
        self.vecino.reparentTo(juego.render)
        self.nombre = nombre
        self.vecino.loop('idle')
        
        
        # COLISION
        cn_vecino = CollisionNode(nombre)
        cn_vecino.addSolid(CollisionSphere(0, 0, 1, .3))
        self.colisionador = self.vecino.attachNewNode(cn_vecino)

        juego.pusher.addCollider(self.colisionador, self.vecino)
        juego.cTrav.addCollider(self.colisionador, juego.cHandler)
        
        self.puntos = 1000

    def actualizar(self):
        self.vecino.lookAt(self.juego.jugador.personaje.getPos())
        animacion_especial = self.vecino.getAnimControl('action')
        if not animacion_especial and not animacion_especial.isPlaying():
            self.vecino.loop('idle')

    def eliminar(self):
        self.vecino.cleanup()
        self.vecino.removeNode()

    def accion(self):
        if random.random() < 0.01:  
            self.vecino.stop('idle')
            self.vecino.play('action')
