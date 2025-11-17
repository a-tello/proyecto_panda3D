import random
from panda3d.core import NodePath, CollisionNode, CollisionBox, Point3, CollisionPlane
from PIL import Image
from constantes import *

class Mapa():
    def __init__(self, juego):
        self.juego = juego
        self.mapa = []
        self.mapa_nodo = None

    
    def crear_escenario(self, matriz):        
        pared = self.juego.loader.loadModel('models/box')
        pared.setScale(1, 1, 3)
        textura_pared = self.juego.loader.loadTexture('assets/Environment/tex/pared.jpg')
        textura_pared.setWrapU(textura_pared.WM_repeat)
        textura_pared.setWrapV(textura_pared.WM_repeat)
        pared.setTexture(textura_pared, 1)

        piso = self.juego.loader.loadModel('models/box')        
        textura_piso = self.juego.loader.loadTexture('assets/Environment/tex/tierra.jpg')
        textura_piso.setWrapU(textura_piso.WM_repeat)
        textura_piso.setWrapV(textura_piso.WM_repeat)
        piso.setTexture(textura_piso, 1)
        
        mapa_np = NodePath('mapa')
        mapa_np.reparentTo(self.juego.render)
        self.mapa_nodo = mapa_np

        alto = len(matriz)
        ancho = len(matriz[0])

        for y in range(alto):
            for x in range(ancho):
                cubo_piso = piso.copyTo(mapa_np)
                cubo_piso.setPos(x,y,-1)
                if matriz[y][x] == 1:
                    cubo_pared = pared.copyTo(mapa_np)
                    self.agregar_colision_pared(cubo_pared)
                    cubo_pared.setPos(x, y, 0)

    def agregar_colision_pared(self, nodo):
        nodo_colision = CollisionNode('pared')
        nodo_colision.addSolid(CollisionBox(Point3(0.5, 0.5, 0.5), 0.5, 0.5, 0.5))
        nodo.attachNewNode(nodo_colision)


class MapaImagen(Mapa):
    def __init__(self, juego, imagen, nivel):
        super().__init__(juego)

        self.nivel = nivel
        self.mapeado = {'sp_jugador': (0,0,255), 
                        'sp_vecino': (0,255,0), 
                        'sp_enemigo': (255,0,0),
                        'pared': (0,0,0),
                        'piso': (255,255,255)}

        self.cargar_matriz_imagen(imagen)

    def cargar_matriz_imagen(self, imagen):
        with Image.open(imagen) as im:
            ancho, alto = im.size
            
            for y in range(alto):
                fila = []
                for x in range(ancho):
                    pixel = im.getpixel((x, y))[:3]
                    if pixel == self.mapeado['pared']: 
                        fila.append(1)
                    else:                          
                        fila.append(0)
                        if pixel == self.mapeado['sp_jugador']:                            
                            self.nivel.jugador_spawn = (x,y,0)
                        elif pixel == self.mapeado['sp_vecino']:
                            self.nivel.vecinos_spawn.append((x,y,0))
                        elif pixel == self.mapeado['sp_enemigo']:
                            self.nivel.enemigos_spawn.append((x,y,0))
                            
                self.mapa.append(fila)
        
            self.crear_escenario(self.mapa)

