from direct.gui.DirectGui import DirectFrame, DirectButton, DirectLabel, DirectOptionMenu, DirectSlider, DirectRadioButton, DirectEntry
from panda3d.core import TextNode
from direct.gui.OnscreenText import OnscreenText
from direct.task import Task


class Menu():
    def __init__(self, juego):
        self.menu_fondo = DirectFrame(frameColor = (0, 0, 0, 1), frameSize = (-1, 1, -1, 1), parent = juego.render2d)
        self.menu = DirectFrame(frameColor = (1, 1, 1, 0))
        
        self.aspect = juego.getAspectRatio()
        self.color = (11/255.0, 96/255.0, 13/255.0, 1)
        self.sonido_boton = juego.loader.loadSfx('assets/sounds/boton.ogg')
        self.sonido_boton.setVolume(0.5)
        self.fuente = juego.fuente
        self.boton_imagenes = [juego.loader.loadTexture('assets/GUI/Button/Rect/Default.png'),
                               juego.loader.loadTexture('assets/GUI/Button/Rect/Default.png')]

    def esconder_menu(self):
        self.menu.hide()
        self.menu_fondo.hide()

    def mostrar_menu(self):
        self.menu_fondo.show()
        self.menu.show()
        
    def eliminar_menu(self):
        self.menu.removeNode()

class MenuPrincipal(Menu):
    def __init__(self, juego):
        super().__init__(juego)
                
        btn = DirectButton(text = 'Jugar', command = juego.jugar, pos = (self.aspect-0.5, 0, 0.1), parent = self.menu, scale = 0.1, frameColor=self.color,
                        frameSize = (-3, 3, -1, 1), text_scale = 1.5, text_pos = (-0.2, -0.4), clickSound = self.sonido_boton, text_font = self.fuente,
                        frameTexture = self.boton_imagenes, text_fg = (1,1,1,1))
        btn.setTransparency(True)

        btn = DirectButton(text = 'Opciones', command = juego.opciones, pos = (self.aspect-0.5, 0, -0.2), parent = self.menu, scale = 0.1, frameColor=self.color,
                        frameSize = (-3, 3, -1, 1), text_scale = 1.5, text_pos = (-0.2, -0.4), clickSound = self.sonido_boton, text_font = self.fuente,
                        frameTexture = self.boton_imagenes, text_fg = (1,1,1,1))
        btn.setTransparency(True)
        btn = DirectButton(text = 'Puntos', command = juego.puntuaciones, pos = (self.aspect-0.5, 0, -0.5), parent = self.menu, scale = 0.1, frameColor=self.color,
                        frameSize = (-3, 3, -1, 1), text_scale = 1.5, text_pos = (-0.2, -0.4), clickSound = self.sonido_boton, text_font = self.fuente,
                        frameTexture = self.boton_imagenes, text_fg = (1,1,1,1))
        btn.setTransparency(True)

        btn = DirectButton(text = 'Salir', command = juego.salir, pos = (self.aspect-0.5, 0, -0.8), parent = self.menu, scale = 0.1, frameColor=self.color,
                        frameSize = (-3, 3, -1, 1), text_scale = 1.5, text_pos = (-0.2, -0.4), clickSound = self.sonido_boton, text_font = self.fuente,
                        frameTexture = self.boton_imagenes, text_fg = (1,1,1,1))
        btn.setTransparency(True)


class MenuOpciones(Menu):
    def __init__(self, juego):
        super().__init__(juego)      

        DirectLabel(text = 'Resolución', scale = 0.1, pos = (-.5, 0, 0.6), parent = self.menu, text_fg = (1, 1, 1, 1), frameColor=(0,0,0,0),
                    frameSize = (-4, 4, -1, 1), text_pos = (0, -0.2), text_font = self.fuente)

        btn = DirectOptionMenu(text='Resolución de pantalla', pos = (.5, 0, 0.6), parent = self.menu, scale=0.1, initialitem=0,
                        frameSize = (-4, 4, -1, 1), text_scale = 1.1, text_pos = (0, -0.2), command=juego.cambiar_pantalla, text_align=TextNode.ACenter,
                        items=['800 x 600','1280 x 960', '1280 x 1024', '1920 x 1080'], highlightColor=(0.65, 0.65, 0.65, 1), textMayChange=1, clickSound = self.sonido_boton,
                        frameTexture = self.boton_imagenes)
        btn.setTransparency(True)


        DirectLabel(text = 'Modo de pantalla', scale = 0.1, pos = (-.5, 0, 0.2), parent = self.menu, text_fg = (1, 1, 1, 1), frameColor=(0,0,0,0),
                    frameSize = (-4, 4, -1, 1), text_pos = (0, -0.2), text_font = self.fuente)
        
        botones = [
        DirectRadioButton(text='Pantalla Completa', variable=[1], value=[0], indicatorValue=False ,scale=0.08, pos=(0.5, 0, .23), command=juego.modo_pantalla, 
                          parent=self.menu, extraArgs=[True], clickSound = self.sonido_boton, text_font = self.fuente,frameTexture = self.boton_imagenes),
        DirectRadioButton(text='Modo ventana', variable=[1], value=[1], indicatorValue=False, scale=0.08, pos=(0.43, 0, .10), command=juego.modo_pantalla, 
                          parent=self.menu, extraArgs=[False], clickSound = self.sonido_boton, text_font = self.fuente,frameTexture = self.boton_imagenes)
        ]

        for boton in botones:
            boton.setOthers(botones)

        
        DirectLabel(text = 'Musica', scale = 0.1, pos = (-.5, 0, -0.2), parent = self.menu, frameColor=(0,0,0,0),
                        text_fg = (1, 1, 1, 1),frameSize = (-4, 4, -1, 1), text_pos = (0, -0.2), text_font = self.fuente)
        self.volumen = DirectSlider(range=(0,100), value=0, pos = (.5, 0, -0.2), pageSize=3, command=juego.musica, scale=0.5, parent=self.menu, frameTexture = self.boton_imagenes)


        btn = DirectButton(text = 'Volver', command = juego.volver, pos = (0, 0, -0.6), parent = self.menu, scale = 0.1, text_fg = (1, 1, 1, 1),
                        frameSize = (-4, 4, -1, 1), text_scale = 0.75, text_pos = (0, -0.2), clickSound = self.sonido_boton, text_font = self.fuente, frameTexture = self.boton_imagenes)
        btn.setTransparency(True)


class MenuPausa(Menu):
    def __init__(self, juego):
        super().__init__(juego)
        

        title = DirectLabel(text = 'Pausa', scale = 0.1, pos = (0, 0, 0.9), parent = self.menu, 
                        relief = None,  text_fg = (1, 1, 1, 1))
        
        btn = DirectButton(text = 'Continuar', command = juego.pausa, pos = (0, 0, 0.2), parent = self.menu, scale = 0.1,
                        frameSize = (-4, 4, -1, 1), text_scale = 0.75, text_pos = (0, -0.2))
        btn.setTransparency(True)

        btn = DirectButton(text = 'Opciones', command = juego.opciones, pos = (0, 0, -0.2), parent = self.menu, scale = 0.1, 
                        frameSize = (-4, 4, -1, 1), text_scale = 0.75, text_pos = (0, -0.2))
        btn.setTransparency(True)

        btn = DirectButton(text = 'Volver al menú', command = juego.menu, pos = (0, 0, -0.6), parent = self.menu, scale = 0.1, 
                        frameSize = (-4, 4, -1, 1), text_scale = 0.75, text_pos = (0, -0.2))
        btn.setTransparency(True)


class PantallaFinal(Menu):
    def __init__(self, juego, puntos, texto):
        super().__init__(juego)
        
        self.juego = juego
        self.puntos = puntos
        title = DirectLabel(text = 'JUEGO TEMRINADO', scale = 0.3, pos = (0, 0, 0.75), parent = self.menu, 
                        relief = None,  text_fg = (1, 1, 1, 1), text_font = self.fuente)
        
        title = DirectLabel(text = texto, scale = 0.2, pos = (0, 0, 0.50), parent = self.menu, 
                        relief = None,  text_fg = (1, 1, 1, 1), text_font = self.fuente)
        
        pts = OnscreenText(text = f'Puntos: {puntos}', pos = (0, 0.30), mayChange = True, scale=.12, fg=(255,255,255,255), align = TextNode.ACenter, parent = self.menu
                           ,font = self.fuente)


        self.ingreso = DirectEntry( text="", scale=0.2, width=5, pos=(0, 0, 0), initialText="Escribe aquí", numLines=1, focus=1, 
                            cursorKeys=1, command=self.guardar_puntos, text_font=self.fuente,parent=self.menu,text_align=TextNode.ACenter)
        
        self.btn_guardar = DirectButton(text = 'Guardar',  pos = (0, 0, -0.3), parent = self.menu, scale = 0.1,
                        frameSize = (-4, 4, -1, 1), text_scale = 1.5, text_pos = (0, -0.4),  text_font = self.fuente,text_align=TextNode.ACenter,
                        command=self.guardar_puntos)
        self.btn_guardar.setTransparency(True)
        
        self.mensaje_guardado = OnscreenText(text = f'Guardado', pos = (0, -0.25), scale=.12, fg=(255,255,255,255), align = TextNode.ACenter, parent = self.menu
                           ,font = self.fuente)
        self.mensaje_guardado.hide()
        
        self.btn_r = DirectButton(text = 'Reiniciar',  pos = (-0.5, 0, -0.5), parent = self.menu, scale = 0.1,
                        frameSize = (-4, 4, -1, 1), text_scale = 1.5, text_pos = (0, -0.4),  text_font = self.fuente,text_align=TextNode.ACenter, command = juego.jugar)
        self.btn_r.setTransparency(True)

        self.btn_m = DirectButton(text = 'Menú principal',  pos = (0.5, 0, -0.5), parent = self.menu, scale = 0.1, 
                        frameSize = (-4, 4, -1, 1), text_scale = 1.2, text_pos = (0, -0.4), text_font = self.fuente,text_align=TextNode.ACenter,command = juego.menu)
        self.btn_m.setTransparency(True)
        self.btn_r.hide()
        self.btn_m.hide()
        
        self.nombre_len = 10
        juego.taskMgr.add(self.limitar_texto, "limitarEntradas")

    def limitar_texto(self, _):
        texto = self.ingreso.get()
        texto_filtrado = ''.join(c for c in texto if c.isalpha())

        texto_filtrado = texto_filtrado[:self.nombre_len]

        if texto != texto_filtrado:
            self.ingreso.set(texto_filtrado)

        return Task.cont
    
    def guardar_puntos(self, nombre=None):
        if nombre is None:
            nombre = self.ingreso.get()
        puntos = self.puntos
        puntaje = {'nombre': nombre.upper(), 'puntos': puntos}
        print(puntaje)
        self.desbloquear_botones()
        self.juego.guardar_puntos(puntaje)
        
    def desbloquear_botones(self):
        self.btn_r.show()
        self.btn_m.show()
        self.mensaje_guardado.show()
        self.btn_guardar.hide()
        

class PantallaPuntajes(Menu):
    def __init__(self, juego):
        super().__init__(juego)
        
        self.puntajes = juego.puntajes
        
        title = DirectLabel(text = 'PUNTUACIONES', scale = 0.3, pos = (0, 0, 0.75), parent = self.menu, 
                        relief = None,  text_fg = (1, 1, 1, 1), text_font = self.fuente)
        
            
        for i, jugador in enumerate(self.puntajes):
            print(jugador)
            puesto = OnscreenText(text = f'{i+1}.', pos = (-1, 0.5 - i * 0.15), mayChange = True, scale=.2, fg=(1,.5,0,255), align = TextNode.ARight, parent = self.menu
                            ,font = self.fuente)
            nombre = OnscreenText(text = jugador['nombre'], pos = (-0.9, 0.5 - i * 0.15), scale=.2, fg=(1,.5,0,255), align = TextNode.ALeft, parent = self.menu
                            ,font = self.fuente)
            pts = OnscreenText(text = str(jugador['puntos']), pos = (1, 0.5 - i * 0.15), scale=.2, fg=(1,.5,0,255), align = TextNode.ARight, parent = self.menu
                            ,font = self.fuente)
        
        btn = DirectButton(text = 'Volver al menú', command = juego.menu, pos = (0, 0, -0.6), parent = self.menu, scale = 0.1, 
                        frameSize = (-4, 4, -1, 1), text_scale = 0.75, text_pos = (0, -0.2))
        btn.setTransparency(True)