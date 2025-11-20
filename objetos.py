from panda3d.core import CollisionSphere, CollisionNode, CollisionBox, Point3
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
        
class Puerta():
    def __init__(self, juego):
        self.puerta = juego.loader.loadModel('models/box')
        self.puerta.reparentTo(juego.render)
        x, y, z = juego.gestor_nivel.jugador_spawn
        self.puerta.setPos(x,y,z)
        self.puerta.setScale(2,2,2)
        self.puerta.lookAt(juego.jugador.personaje)
        self.puerta.setColor(1, 1, 1, 1)

        cn_puerta = CollisionNode('puerta')
        cn_puerta.addSolid(CollisionBox(Point3(.5, .5, .5), .5, .5, .5))
        colisionador_puerta = self.puerta.attachNewNode(cn_puerta)
        colisionador_puerta.show()
        
        juego.pusher.addCollider(colisionador_puerta, self.puerta)
        juego.cTrav.addCollider(colisionador_puerta, juego.cHandler)

class Item():
    def __init__(self, juego, spawn, modelo, nombre):

        self.item = juego.loader.loadModel(modelo)
        self.item.setPos(spawn)
        self.item.reparentTo(juego.render)
        print(spawn)
        cn_item = CollisionNode(nombre)
        cn_item.addSolid(CollisionBox(Point3(.5, .5, .5), 1, 1, 1))
        self.colisionador_item = self.item.attachNewNode(cn_item)
        self.colisionador_item.show()
        juego.pusher.addCollider(self.colisionador_item, self.item)
        juego.cTrav.addCollider(self.colisionador_item, juego.cHandler)
        self.puntos = 100

    def eliminar(self):
        self.item.removeNode()

class Bebida(Item):
    def __init__(self, juego, spawn):
        super().__init__(juego,
                         spawn,
                        'assets/drink.glb',
                        'bebida')
        
        self.nombre = 'bebida'
        self.colisionador_item.setScale(2,2,4)
        self.item.setScale(0.1)
        self.velocidad = 5

class Botiquin(Item):
    def __init__(self, juego, spawn):
        super().__init__(juego, 
                         spawn,
                         'assets/medical_kit.glb', 
                         'botiquin')
        
        self.nombre = 'botiquin'
        self.item.setScale(0.5)
        self.puntos = 500
        self.vida = 3

class Dron(Item):
    def __init__(self, juego, spawn):
        super().__init__(juego, 
                         spawn,
                         'assets/dron.glb', 
                         'dron')
        
        self.nombre = 'dron'
        self.puntos = 500

        



        