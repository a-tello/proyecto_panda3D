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
        self.modelos = {'1':'untitled.glb', '2':'untitled.glb', '3':'untitled.glb', '4':'untitled.glb', '5':'untitled.glb'}
        self.vecino = Actor(self.modelos[tipo])
        self.vecino.setPos(pos)
        self.vecino.reparentTo(juego.render)
        self.nombre = nombre
        
        
        # COLISION
        cn_vecino = CollisionNode(nombre)
        cn_vecino.addSolid(CollisionSphere(0, 0, 1, .3))
        self.colisionador = self.vecino.attachNewNode(cn_vecino)

        juego.pusher.addCollider(self.colisionador, self.vecino)
        juego.cTrav.addCollider(self.colisionador, juego.cHandler)
        
        self.puntos = 1000
        
    def eliminar(self):
        self.vecino.removeNode()