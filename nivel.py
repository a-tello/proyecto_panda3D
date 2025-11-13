import random
from panda3d.core import NodePath, CollisionNode, CollisionBox, Point3, BitMask32
from PIL import Image
from constantes import *

class Nivel():
    def __init__(self, juego):
        self.juego = juego
        self.mapa = []
    
    def crear_escenario(self, matriz):
        
        # TODO funcion
        
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

        alto = len(matriz)
        ancho = len(matriz[0])

        for y in range(alto):
            for x in range(ancho):
                cubo_piso = piso.copyTo(mapa_np)
                cubo_piso.setPos(x,y,-1)
                if matriz[y][x] == 1:
                    cubo_pared = pared.copyTo(mapa_np)
                    self.agregar_colision(cubo_pared)
                    cubo_pared.setPos(x, y, 0)

    def agregar_colision(self, nodo):
        nodo_colision = CollisionNode('pared')
        nodo_colision.addSolid(CollisionBox(Point3(0.5, 0.5, 0.5), 0.5, 0.5, 0.5))
        nodo.attachNewNode(nodo_colision)


class MapaImagen(Nivel):
    def __init__(self, juego, imagen):
        super().__init__(juego)

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
                            self.juego.sp_jugador = (x,y,0)
                        elif pixel == self.mapeado['sp_vecino']:
                            self.juego.sp_vecinos.append((x,y,0))
                        elif pixel == self.mapeado['sp_enemigo']:
                            self.juego.sp_enemigos.append((x,y,1))
                            
                self.mapa.append(fila)
        
            self.crear_escenario(self.mapa)


class Laberinto(Nivel):
    def __init__(self, juego, ancho=10, alto=10):
        super().__init__(juego)
        self.ancho = ancho
        self.alto = alto
        self.spawn = (1, 1)
        self.salida = ()
        self.generar_matriz()

    def generar_matriz(self):
        ancho = self.ancho
        alto = self.alto
        
        if ancho % 2 == 0: 
            self.ancho += 1
        if alto % 2 == 0: 
            self.alto += 1

        for x in range(self.ancho):
            fila = []
            for y in range(self.alto):
                fila.append(1)
            self.mapa.append(fila)
        self.mapa[1][1] = 0
        self.generar_laberinto(1, 1)
        self.salida = (self.alto-2, self.ancho-1)

    def generar_laberinto(self, x, y):
        direcciones = [(2,0), (-2,0), (0,2), (0,-2)]
        random.shuffle(direcciones)
        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            if 0 < nx < self.ancho-1 and 0 < ny < self.alto-1:
                if self.mapa[ny][nx] == 1:
                    self.mapa[ny - dy//2][nx - dx//2] = 0
                    self.mapa[ny][nx] = 0
                    self.generar_laberinto(nx, ny)
        
        self.crear_escenario(self.mapa)

    # def mostrar(self):
    #     print('Entrada:', self.spawn)
    #     print('Salida:', self.salida)

    #     for y, fila in enumerate(self.matriz):
    #         linea = ''
    #         for x, c in enumerate(fila):
    #             if (y, x) == self.spawn:
    #                 linea += 'E'
    #             elif (y, x) == self.salida:
    #                 linea += 'S'
    #             else:
    #                 linea += '█' if c == 1 else ' '
    #         print(linea)
