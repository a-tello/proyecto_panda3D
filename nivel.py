import random
from panda3d.core import NodePath, CollisionNode, CollisionBox, Point3
from PIL import Image

class Nivel():
    def __init__(self, juego):
        self.juego = juego

        # MAPA
        self.mapa = []
        self.cargar_matriz_imagen('assets/maps/lvl1.png')

        
    def cargar_matriz_imagen(self, imagen):
        mapa = Image.open(imagen).convert('L')
        ancho, alto = mapa.size
        
        matriz = []
        for y in range(alto):
            fila = []
            for x in range(ancho):
                pixel = mapa.getpixel((x, y))
                if pixel < 128: 
                    fila.append(1)
                else:  
                    fila.append(0)
            matriz.append(fila)
        
        self.crear_escenario(matriz)


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

        alto = len(matriz)
        ancho = len(matriz[0])

        for y in range(alto):
            for x in range(ancho):
                if matriz[y][x] == 1:
                    cubo_pared = pared.copyTo(mapa_np)
                    cubo_pared.setPos(x, y, 0)
                    self.agregar_colision(cubo_pared)
                else:
                    cubo_piso = piso.copyTo(mapa_np)
                    cubo_piso.setPos(x,y,-1)

        
    def agregar_colision(self, nodo):
        nodo_colision = CollisionNode('pared')
        nodo_colision.addSolid(CollisionBox(Point3(0.5, 0.5, 0.5), 0.5, 0.5, 0.5))
        nc_path = nodo.attachNewNode(nodo_colision)
        nc_path.show()








class Laberinto():
    def __init__(self, ancho=30, alto=30):
        self.ancho = ancho
        self.alto = alto
        self.laberinto = []
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
            self.matriz.append(fila)
        self.matriz[1][1] = 0
        self.generar_laberinto(1, 1)
        self.salida = (self.alto-2, self.ancho-1)

    def generar_laberinto(self, x, y):
        direcciones = [(2,0), (-2,0), (0,2), (0,-2)]
        random.shuffle(direcciones)
        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            if 0 < nx < self.ancho-1 and 0 < ny < self.alto-1:
                if self.matriz[ny][nx] == 1:
                    self.matriz[ny - dy//2][nx - dx//2] = 0
                    self.matriz[ny][nx] = 0
                    self.generar_laberinto(nx, ny)

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
