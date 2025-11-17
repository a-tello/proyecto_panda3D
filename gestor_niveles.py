import random
from panda3d.core import AmbientLight, DirectionalLight
from nivel import *
from enemigo import Enemigo
from panda3d.core import Vec3, Point3
from vecino import Vecino
from personaje import Personaje

class Nivel():
    def __init__(self, juego):
        self.juego = juego
        self.jugador_spawn = Vec3()
        self.vecinos = []
        self.vecinos_spawn = []
        self.jugador = None

        self.enemigos = []
        self.enemigos_spawn = []
        self.enemigos_muertos = []
        self.enemigos_id = 0
        self.enemigos_max = juego.niveles[juego.nivel]['enemigos']
        self.intervalo_spawn = 2
        self.temporizador_spawn = 2
        #self.level_guardado = []

        self.musica_nivel = None

    def cargar(self, info_nivel):

        self.musica_nivel = self.juego.loader.loadSfx(info_nivel['musica'])
        self.musica_nivel.setLoop(True)
        self.musica_nivel.setVolume(0.075)
        self.musica_nivel.play()
        self.cargar_mapa(info_nivel['mapa'])
        self.juego.jugador = Personaje(self.juego, self.jugador_spawn)
        self.spawnear_enemigos(info_nivel['enemigos'])
        self.spawnear_vecinos(info_nivel['vecinos'])

    def cargar_mapa(self, img_mapa):
        # ENTORNO
        skybox = self.juego.loader.loadModel("models/misc/sphere")
        skybox.reparentTo(self.juego.render)
        skybox.setScale(500)
        skybox.setTwoSided(True)
        textura = self.juego.loader.loadTexture("assets/Environment/cielo2.jpg")
        skybox.setTexture(textura)
        skybox.setPos(-10, -10, 0)

        mapa = MapaImagen(self.juego, img_mapa, self)

        #ILUMINACION
        ambient = AmbientLight('ambient_light')
        ambient.setColor((0.5, 0.5, 0.5, 1))
        self.juego.render.setLight(self.juego.render.attachNewNode(ambient))

        dlight = DirectionalLight('directional_light')
        dlight.setColor((1, 1, 1, 1))
        dlight.setDirection(Point3(1, -1, -1))
        self.juego.render.setLight(self.juego.render.attachNewNode(dlight))


    def spawnear_enemigos(self, cantidad):
        if len(self.enemigos) < cantidad:
            spawn = random.choice(self.enemigos_spawn)
            enemigo = Enemigo(self.juego, f'enemigo_{self.enemigos_id}', spawn, self.enemigos_id)
            self.enemigos.append(enemigo)
            self.juego.accept(f'bala-into-enemigo_balas_{self.enemigos_id}', self.juego.impacto)
            self.enemigos_id += 1

    def spawnear_vecinos(self, cantidad):
        for i in range(cantidad):
            spawn = random.choice(self.vecinos_spawn)
            modelo = random.randint(1,5)
            nombre = f'vecino_{i}'
            vecino = Vecino(self.juego, str(modelo), spawn, nombre)
            self.vecinos.append(vecino)
            self.vecinos_spawn.remove(spawn)
            self.juego.accept(f'personaje_obj-into-{nombre}', self.juego.limpiar)
        
    def actualizar_enemigos(self, dt):
        self.temporizador_spawn -= dt
        
        if self.temporizador_spawn <= 0:
            self.temporizador_spawn = self.intervalo_spawn
            self.spawnear_enemigos(self.enemigos_max)

        for enemigo in self.enemigos:
            enemigo.mover(dt)

        for enemigo in self.enemigos_muertos:
            enemigo.morir()
            self.enemigos_muertos.remove(enemigo) 
