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

    def actualizar_tecla(self, tecla, estado):
        self.teclas[tecla] = estado

    def mover(self, dt):
        distancia = Vec3(0, 0, 0)
        self.movimiento = False

        if self.teclas['adelante']: 
            distancia.y += 1
            self.movimiento = True
        if self.teclas['atras']: 
            distancia.y -= 1
            self.movimiento = True
        if self.teclas['izquierda']: 
            distancia.x -= 1
            self.movimiento = True
        if self.teclas['derecha']: 
            distancia.x += 1
            self.movimiento = True

        if distancia.length() > 0:
            distancia.normalize()
            self.personaje.setPos(self.personaje.getPos() + distancia * dt * self.velocidad)

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