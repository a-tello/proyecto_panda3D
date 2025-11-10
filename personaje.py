import math
from direct.actor.Actor import Actor
from panda3d.core import Vec3

class Personaje():
    def __init__(self, juego):
        self.juego = juego
        self.personaje = Actor('assets/models/act_p3d_chan', {
                            'stand' : 'assets/models/a_p3d_chan_idle',
                            'walk' : 'assets/models/a_p3d_chan_walk'
                        })
        self.personaje.setPos(0, 5, 0)
        self.personaje.getChild(0).setH(180)
        self.personaje.reparentTo(self.juego.render) 
        self.personaje.loop("stand")

        self.velocidad = 5

        # Teclas
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



        juego.cam.setPos(0, -2, 1)  # Posiciona la cámara por encima del suelo
        juego.cam.node().getLens().setFov(80)
        self.angulo_horizontal = 0  # Rotación izquierda/derecha
        self.angulo_vertical = 0  # Rotación izquierda/derecha
        self.ultimo_mouse_x = 0
        self.ultimo_mouse_y = 0
        self.velocidad = 5.0
        self.velocidad_rotacion = 120.0
        self.sensibilidad_mouse = 0.3



    def actualizar_tecla(self, tecla, estado):
        self.teclas[tecla] = estado

    def mover(self, dt):
        if self.juego.mouseWatcherNode.hasMouse():
            mouse_x = self.juego.mouseWatcherNode.getMouseX()
            mouse_y = self.juego.mouseWatcherNode.getMouseY()

            # if self.ultimo_mouse_x != 0:
            #     delta_x = mouse_x - self.ultimo_mouse_x
            #     delta_y = mouse_y - self.ultimo_mouse_y
            if mouse_x or mouse_y:


                # Rotar tanto cámara como actor
                self.angulo_horizontal -= mouse_x * self.sensibilidad_mouse * 100
                self.angulo_vertical += mouse_y * self.sensibilidad_mouse * 100
                
                # Limitar ángulo vertical
                self.angulo_vertical = max(-90, min(90, self.angulo_vertical))
                self.juego.win.movePointer(0, self.juego.win.getXSize()//2, self.juego.win.getYSize()//2)

            self.ultimo_mouse_x = mouse_x
            self.ultimo_mouse_y = mouse_y


        # ===== MOVIMIENTO DEL ACTOR =====
        # Calcular vectores de dirección basados en el ángulo horizontal
        rad = math.radians(self.angulo_horizontal)
        movimiento_adelante = Vec3(-math.sin(rad), math.cos(rad), 0)
        movimiento_derecha = Vec3(math.cos(rad), math.sin(rad), 0)
        
        # Calcular dirección de movimiento
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
            # vel_actual = self.velocidad * (2 if teclas['shift'] else 1) CORRER
            self.personaje.setPos(self.personaje.getPos() + distancia * dt * self.velocidad)

            self.personaje.setH(math.degrees(math.atan2(-distancia.x, distancia.y)))
        else:
            # Si no se mueve, el actor mira hacia donde mira la cámara
            self.personaje.setH(self.angulo_horizontal)

        self.movimiento_camara()

        if self.movimiento:
            animacion_quieto = self.personaje.getAnimControl('stand')
            animacion_caminar = self.personaje.getAnimControl('walk')

            if animacion_quieto and animacion_quieto.isPlaying():
                animacion_quieto.stop()

            if animacion_caminar and not animacion_caminar.isPlaying():
                self.personaje.loop('walk')
        else:
            animacion_quieto = self.personaje.getAnimControl('stand')
            if animacion_quieto and not animacion_quieto.isPlaying():
                self.personaje.stop('walk')
                self.personaje.loop('stand')
        


    def movimiento_camara(self):
        personaje_pos = self.personaje.getPos()
        self.juego.camera.setPos(personaje_pos + Vec3(0, 0, 1.2))
        self.juego.camera.setHpr(self.angulo_horizontal, self.angulo_vertical, 0)
