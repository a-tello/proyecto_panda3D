import random
from panda3d.core import AmbientLight, DirectionalLight
from nivel import *
from enemigo import Enemigo
from panda3d.core import Vec3, Point3
from vecino import Vecino
from personaje import Personaje
from objetos import *
from interfaz import Interfaz
class Nivel():
    def __init__(self, juego):
        self.juego = juego
        self.gui = None
        
        self.mapa = None
        self.jugador_spawn = Vec3()
        self.vecinos = []
        self.vecinos_spawn = []

        self.enemigos = []
        self.enemigos_spawn = []
        self.enemigos_muertos = []
        self.enemigos_id = 0
        self.enemigos_max = 0
        self.intervalo_spawn = 2
        self.temporizador_spawn = 2
        
        self.balas_activas = []
        self.puerta_final = None
        self.items = []

        self.musica_nivel = None
        self.sonido_final_nivel = self.juego.loader.loadSfx("assets/sounds/final.ogg")
        self.sonido_final_nivel.setVolume(0.05)


    def cargar(self, info_nivel):
        self.musica_nivel = self.juego.loader.loadSfx(info_nivel['musica'])
        self.musica_nivel.setLoop(True)
        self.musica_nivel.setVolume(self.juego.musica_volumen)
        self.musica_nivel.play()

        self.cargar_mapa(info_nivel['mapa'])
        
        if self.juego.jugador is None:
            self.juego.jugador = Personaje(self.juego, self.jugador_spawn)

        self.enemigos_max = self.juego.niveles[self.juego.nivel]['enemigos']
        self.spawnear_enemigos(info_nivel['enemigos'])
        self.spawnear_vecinos(info_nivel['vecinos'])
        self.spawnear_powerups(info_nivel['powerups'])
        
        if self.gui is None:
            self.gui = Interfaz(self.juego)
            self.gui.crear_GUI()
        
            

    def cargar_mapa(self, img_mapa):
        # ENTORNO
        self.skybox = self.juego.loader.loadModel("models/misc/sphere")
        self.skybox.reparentTo(self.juego.render)
        self.skybox.setScale(500)
        self.skybox.setTwoSided(True)
        textura = self.juego.loader.loadTexture("assets/Environment/cielo2.jpg")
        self.skybox.setTexture(textura)
        self.skybox.setPos(-10, -10, 0)

        self.mapa = MapaImagen(self.juego, img_mapa, self)
        
        #ILUMINACION
        ambient = AmbientLight('ambient_light')
        ambient.setColor((0.5, 0.5, 0.5, 1))
        self.luz_ambiente = self.juego.render.attachNewNode(ambient)
        self.juego.render.setLight(self.luz_ambiente)

        dlight = DirectionalLight('directional_light')
        dlight.setColor((1, 1, 1, 1))
        dlight.setDirection(Point3(1, -1, -1))
        self.luz_direccional = self.juego.render.attachNewNode(dlight)
        self.juego.render.setLight(self.luz_direccional)

    def spawnear_enemigos(self, cantidad):
        if len(self.enemigos) < cantidad:
            spawn = random.choice(self.enemigos_spawn)
            enemigo = Enemigo(self.juego, f'enemigo_{self.enemigos_id}', spawn, self.enemigos_id, self.juego.nivel)
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
            self.juego.accept(f'personaje_obj-into-{nombre}', self.juego.salvar_vecino)

    def spawnear_powerups(self, cantidad):
        for i in range(cantidad):
            spawn = random.choice(self.vecinos_spawn)
            item = random.choice([Bebida, Dron, Botiquin])
            powerup = item(self.juego, spawn)
            nombre = powerup.nombre
            print(nombre)
            self.items.append(powerup)
            self.vecinos_spawn.remove(spawn)
            self.juego.accept(f'personaje_obj-into-{nombre}', self.boost)

    def boost(self, colision):
        self.juego.sonido_item.play()
        nombre = colision.getIntoNode().getName()
        for powerup in self.items:
            if powerup.nombre == nombre:
                self.juego.jugador.actualizar_puntos(powerup.puntos)

                match(nombre):
                    case 'bebida':
                        self.juego.jugador.velocidad += powerup.velocidad
                        self.juego.taskMgr.doMethodLater(5, self.restaurar_velocidad, 'restaurar-velocidad')
                    case 'botiquin':
                        self.juego.jugador.actualizar_vida(5)
                    case 'dron':
                        pass

                powerup.eliminar()
                self.items.remove(powerup)
                break
        
    def restaurar_velocidad(self, _):    
        self.juego.jugador.velocidad = 5


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
    
    def impacto_enemigos(self, id_enemigo):
        for enemigo in self.enemigos:
            if id_enemigo == str(enemigo.id):
                enemigo.actualizar_vida(-self.juego.jugador.ataque)
                if enemigo.vida < 1:
                    self.enemigos.remove(enemigo)
                    self.enemigos_muertos.append(enemigo)
                    self.juego.jugador.actualizar_puntos(enemigo.puntos)
    
    def actualizar_balas(self, dt):
        for bala in self.balas_activas[:]:
            modelo = bala['modelo'].bala
            modelo.setY(modelo, bala['velocidad'] * dt)

            if (modelo.getPos() - self.juego.jugador.personaje.getPos()).length() > 50:
                modelo.removeNode()
                self.balas_activas.remove(bala)

    def limpiar_nivel(self):
        for vecino in self.vecinos[:]:
            vecino.eliminar()
            self.vecinos.remove(vecino)
        for zombie in self.enemigos[:]:
            zombie.eliminar()
            self.enemigos.remove(zombie)
        for item in self.items[:]:
            item.eliminar()
            self.items.remove(item)

        self.mapa.mapa_nodo.removeNode()
        self.enemigos_spawn = self.jugador_spawn = self.vecinos_spawn = []
        if self.puerta_final:
            self.puerta_final.puerta.removeNode()
        
        self.luz_ambiente.removeNode()
        self.luz_direccional.removeNode()
        self.skybox.removeNode()

    def pasar_nivel(self, _):
        self.juego.taskMgr.remove('actualizar')
        self.musica_nivel.stop()
        self.sonido_final_nivel.play()
        self.limpiar_nivel()
        self.juego.nivel += 1
        self.juego.jugador.vida = self.juego.jugador.vida_max
        self.juego.jugador.municion = self.juego.jugador.municion_maxima
        self.juego.jugador.cargador = 90
        self.gui.inicializar()
        self.gui.actualizar_balas(self.juego.jugador.municion, self.juego.jugador.cargador)
        self.cargar(self.juego.niveles[self.juego.nivel])
        print(self.gui)
        #self.gui.mostrar()
        self.juego.taskMgr.add(self.juego.actualizar, 'actualizar')

        # self.juego.jugar()
        
    def crear_final(self):
        self.puerta_final = Puerta(self.juego)
        self.juego.accept(f'personaje_obj-into-puerta', self.pasar_nivel)
        
    # def reiniciar(self):
        
    #     self.juego.taskMgr.remove('actualizar')
    #     self.musica_nivel.stop()
    #     self.limpiar_nivel()
    #     self.juego.nivel = 0
    #     self.gui.inicializar()
    #     self.juego.jugador.vida = self.juego.jugador.vida_max
    #     self.juego.jugador.municion = self.juego.jugador.municion_maxima
    #     self.juego.jugador.cargador = 90
    #     self.juego.jugador.puntaje = 0
    #     self.cargar(self.juego.niveles[self.juego.nivel])
    #     self.juego.taskMgr.add(self.juego.actualizar, 'actualizar')
