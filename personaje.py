import math
from objetos import Bala
from constantes import *
from direct.actor.Actor import Actor
from panda3d.core import Vec3
from panda3d.core import CollisionNode, CollisionBox, Point3, Vec3, BitMask32


class Personaje():
    def __init__(self, juego, spawn):
        
        self.juego = juego
        
        # MODELO
        self.personaje = Actor('assets/models/remy_idle.glb', {
                            'idle' : 'assets/models/remy_idle.glb',
                            'run' : 'assets/models/remy_run.glb'
                        })
        self.personaje.setPos(spawn)
        self.personaje.getChild(0).setH(180)
        self.personaje.reparentTo(self.juego.render)
        self.personaje.setScale(0.5)
        pos = self.personaje.getPos()
        self.personaje.setPos(pos.x, pos.y, 0)
        self.personaje.loop('idle')

        # Modelo raygun
        self.raygun = juego.loader.loadModel('assets/objects/raygun.glb')
        self.raygun.reparentTo(self.personaje)
        x, y, z = juego.gestor_nivel.jugador_spawn
        self.raygun.setPos(0,3,2)
        self.raygun.setScale(2,2,2)
        self.raygun.setColor(1, 1, 1, 1)

        # ATRIBUTOS
        self.vida = 10
        self.vida_max = 10
        self.velocidad = 5
        self.ataque = 3

        # TECLAS
        self.teclas = {'adelante': False, 'atras': False, 'izquierda': False, 'derecha': False, 'usar': False, 'disparar': False}

        self.juego.accept('w', self.actualizar_tecla, ['adelante', True])
        self.juego.accept('w-up', self.actualizar_tecla, ['adelante', False])
        self.juego.accept('s', self.actualizar_tecla, ['atras', True])
        self.juego.accept('s-up', self.actualizar_tecla, ['atras', False])
        self.juego.accept('a', self.actualizar_tecla, ['izquierda', True])
        self.juego.accept('a-up', self.actualizar_tecla, ['izquierda', False])
        self.juego.accept('d', self.actualizar_tecla, ['derecha', True])
        self.juego.accept('d-up', self.actualizar_tecla, ['derecha', False])
        self.juego.accept('e', self.actualizar_tecla, ['usar', True])
        self.juego.accept('e-up', self.actualizar_tecla, ['usar', False])
        self.juego.accept('mouse1', self.actualizar_tecla, ['disparar', True])
        self.juego.accept('mouse1-up', self.actualizar_tecla, ['disparar', False])


        # CAMARA 
        juego.cam.setPos(0, 0, .5)  
        juego.cam.node().getLens().setFov(80)
        self.angulo_horizontal = 0  
        self.angulo_vertical = 0  
        self.ultimo_x = self.juego.win.getPointer(0).getX()
        self.ultimo_Y = self.juego.win.getPointer(0).getY()
        self.velocidad_rotacion = 120.0
        self.sensibilidad_mouse = 0.3
        self.puntaje = 0

        # COLISION (con paredes y enemigos)
        cn_jugador = CollisionNode('personaje')
        cn_jugador.addSolid(CollisionBox(Point3(0, 0.2, 2), 0.3, 0.3, 1))
        self.colisionador = self.personaje.attachNewNode(cn_jugador)
        self.colisionador.setPythonTag('owner', self)
        cn_jugador.setFromCollideMask(BitMask32.bit(1) | BitMask32.bit(2) )
        cn_jugador.setIntoCollideMask(BitMask32.bit(1))

        self.juego.pusher.addCollider(self.colisionador, self.personaje)
        self.juego.cTrav.addCollider(self.colisionador, self.juego.pusher)

        
        # COLISION (con NPCs y objetos)
        cn_jugador_obj = CollisionNode('personaje_obj')
        cn_jugador_obj.addSolid(CollisionBox(Point3(0, 0.2, 1.5), 0.4, 0.4, 1))
        self.colisionador_obj = self.personaje.attachNewNode(cn_jugador_obj)
        self.colisionador_obj.setPythonTag('owner', self)
        cn_jugador_obj.setFromCollideMask(BitMask32.bit(2))
        cn_jugador_obj.setIntoCollideMask(BitMask32.allOff())
        self.colisionador.show()
        self.juego.cTrav.addCollider(self.colisionador_obj, self.juego.cHandler)
        
        # DISPAROS
        self.cooldown = 0
        self.municion = 30
        self.municion_maxima = 30
        self.cargador = 90
                
        self.sonido_disparo = juego.loader.loadSfx("assets/sounds/disparo.ogg")
        self.sonido_disparo.setVolume(.02)

    def actualizar_tecla(self, tecla, estado):
        self.teclas[tecla] = estado

    def actualizar_vida(self, danio):
        self.vida += danio
        self.juego.gestor_nivel.gui.actualizar_vida(self.vida)

    def actualizar_puntos(self, puntos):
        self.puntaje += puntos
        self.juego.gestor_nivel.gui.actualizar_puntos(self.puntaje)

    def mover(self, dt):
        # MOVIMIENTO CAMARA
        if self.juego.mouseWatcherNode.hasMouse():
            x = self.juego.win.getPointer(0).getX()
            y = self.juego.win.getPointer(0).getY()

            delta_x = x - self.ultimo_x
            delta_y = y - self.ultimo_Y

            self.angulo_horizontal = self.personaje.getH() - delta_x * self.sensibilidad_mouse
            self.angulo_vertical += -delta_y * self.sensibilidad_mouse * self.sensibilidad_mouse
            self.angulo_vertical = max(-90, min(90, self.angulo_vertical))
            self.juego.win.movePointer(0, self.juego.win.getXSize()//2, self.juego.win.getYSize()//2)

            winX = int(self.juego.win.getXSize() / 2)
            winY = int(self.juego.win.getYSize() / 2)
            self.juego.win.movePointer(0, winX, winY)

            self.ultimo_x = self.juego.win.getPointer(0).getX()
            self.ultimo_Y = self.juego.win.getPointer(0).getY()


        # MOVIMIENTO PERSONAJE
        rad = math.radians(self.angulo_horizontal)
        movimiento_adelante = Vec3(-math.sin(rad), math.cos(rad), 0)
        movimiento_derecha = Vec3(math.cos(rad), math.sin(rad), 0)
        
        distancia = Vec3(0, 0, 0)
        self.movimiento = False

        if self.teclas['adelante']: 
            distancia += movimiento_adelante
            self.movimiento = True
        if self.teclas['atras']: 
            distancia -= movimiento_adelante
            self.movimiento = True
        if self.teclas['izquierda']: 
            distancia -= movimiento_derecha
            self.movimiento = True
        if self.teclas['derecha']: 
            distancia += movimiento_derecha
            self.movimiento = True

        if distancia.length() > 0:
            distancia.normalize()
            self.personaje.setPos(self.personaje.getPos() + distancia * dt * self.velocidad)

        # GIRAR PERSONAJE Y CAMARA
        self.personaje.setH(self.angulo_horizontal)
        self.movimiento_camara()

        # ANIMACION
        if self.movimiento:
            animacion_quieto = self.personaje.getAnimControl('idle')
            animacion_caminar = self.personaje.getAnimControl('run')

            if animacion_quieto and animacion_quieto.isPlaying():
                animacion_quieto.stop()

            if animacion_caminar and not animacion_caminar.isPlaying():
                self.personaje.loop('run')
        else:
            animacion_quieto = self.personaje.getAnimControl('idle')
            if animacion_quieto and not animacion_quieto.isPlaying():
                self.personaje.stop('run')
                self.personaje.loop('idle')  
                
                
        if self.teclas['disparar']:
            self.disparar()
        
        self.juego.gestor_nivel.actualizar_balas(dt)
            
        if self.cooldown > 0:
            self.cooldown -= dt
                        
    def movimiento_camara(self):
        personaje_pos = self.personaje.getPos()
        self.juego.camera.setPos(personaje_pos + Vec3(0, 0, 1.2))
        self.juego.camera.setHpr(self.angulo_horizontal, self.angulo_vertical, 0)

    def disparar(self):
        if self.cooldown <= 0:                         
            if self.municion == 0:
                self.cooldown = 2

                if self.municion == 0:
                    if self.cargador >= self.municion_maxima:
                        self.municion += self.municion_maxima
                        self.cargador -= self.municion_maxima
                    else:
                        self.municion = self.cargador
                        self.cargador = 0
                
            else:
                self.sonido_disparo.play()
                bala = Bala(self)
                self.juego.gestor_nivel.balas_activas.append({'modelo': bala, 'velocidad': 100})
                self.cooldown = 0.2
                self.municion -= 1
            self.juego.gestor_nivel.gui.actualizar_balas(self.municion, self.cargador)
            
    def eliminar(self):
        self.personaje.cleanup()
        self.personaje.removeNode()
            
        
        
        




        


