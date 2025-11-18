from panda3d.core import CollisionSphere, CollisionNode
from panda3d.core import BitMask32



class Bala():
    def __init__(self, gestor):
        self.bala = gestor.juego.loader.loadModel("models/misc/sphere")
        self.bala.setScale(0.1, 0.5, 0.1)
        self.bala.setColor(0,255,0)
        self.bala.reparentTo(gestor.juego.render)
        self.bala.setPos(gestor.juego.jugador.personaje.getPos()+(0,0,1.5))     
        self.bala.setHpr(gestor.juego.camera.getHpr())    

        bala_nodo = self.bala.attachNewNode(CollisionNode('bala'))
        bala_nodo.node().addSolid(CollisionSphere(0, 0, 0, 0.3))
        bala_nodo.node().setFromCollideMask(BitMask32.bit(3))
        bala_nodo.node().setIntoCollideMask(BitMask32.allOff())
        gestor.juego.cTrav.addCollider(bala_nodo, gestor.juego.cHandler)

        