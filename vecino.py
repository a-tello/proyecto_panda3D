from direct.actor.Actor import Actor
from panda3d.core import CollisionSphere, CollisionNode

class Vecino():
    def __init__(self, juego, tipo, pos, nombre):
        self.modelos = {'1':'assets/models/boss.glb', '2':'assets/models/peasant.glb', '3':'assets/models/AJ.glb', '4':'assets/models/Amy.glb', '5':'assets/models/Kaya.glb'}
        self.vecino = Actor(self.modelos[tipo], {'idle': self.modelos[tipo], 'action': self.modelos[tipo]})
        self.vecino.setPos(pos)
        self.vecino.reparentTo(juego.render)
        self.nombre = nombre
        self.vecino.loop('idle')
        self.vecino.get_parent().lookAt(juego.jugador.personaje)
        
        
        # COLISION
        cn_vecino = CollisionNode(nombre)
        cn_vecino.addSolid(CollisionSphere(0, 0, 1, .3))
        self.colisionador = self.vecino.attachNewNode(cn_vecino)

        juego.pusher.addCollider(self.colisionador, self.vecino)
        juego.cTrav.addCollider(self.colisionador, juego.cHandler)
        
        self.puntos = 1000

    def eliminar(self):
        self.vecino.cleanup()
        self.vecino.removeNode()
