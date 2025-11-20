from direct.gui.DirectGui import DirectFrame, DirectButton, DirectLabel, DirectOptionMenu, DirectSlider, DirectRadioButton, DirectEntry
from panda3d.core import TextNode
from direct.gui.OnscreenText import OnscreenText
from direct.task import Task


class Menu():
    def __init__(self, juego):
        self.menu_fondo = DirectFrame(frameColor = (0, 0, 0, 1), frameSize = (-1, 1, -1, 1), parent = juego.render2d)
        self.menu = DirectFrame(frameColor = (0, 0, 0, 1))
        
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
        
    def crear_boton(self, texto, comando, pos):
        return DirectButton(text = texto, 
                            command = comando, 
                            pos = pos, 
                            parent = self.menu, 
                            scale = 0.1, 
                            frameColor=self.color,
                            frameSize = (-3, 3, -1, 1),
                            text_scale = 1.5, 
                            text_pos = (-0.2, -0.4), 
                            clickSound = self.sonido_boton, 
                            text_font = self.fuente,
                            frameTexture = self.boton_imagenes, 
                            text_fg = (1,1,1,1))
    
    def crear_etiqueta(self, texto, pos):
        return DirectLabel(text = texto, 
                            scale = 0.12,
                            pos = pos,
                            parent = self.menu,
                            text_fg = (1, 1, 1, 1), 
                            frameColor=(0,0,0,0),
                            frameSize = (-4, 4, -1, 1),
                            text_pos = (0, -0.2),
                            text_font = self.fuente)

class MenuPrincipal(Menu):
    def __init__(self, juego):
        super().__init__(juego)
                
        btn_jugar = self.crear_boton('Jugar', juego.jugar, (self.aspect-0.5, 0, 0.1))
        btn_jugar.setTransparency(True)
        btn_opc = self.crear_boton('Opciones', juego.opciones, (self.aspect-0.5, 0, -0.2))
        btn_opc.setTransparency(True)
        btn_pts = self.crear_boton('Puntos', juego.puntuaciones, (self.aspect-0.5, 0, -0.5))
        btn_pts.setTransparency(True)
        btn_salir = self.crear_boton('Salir', juego.salir, (self.aspect-0.5, 0, -0.8))
        btn_salir.setTransparency(True)
        

class MenuOpciones(Menu):
    def __init__(self, juego):
        super().__init__(juego)      

        self.crear_etiqueta('Resolución', (-.5, 0, 0.6))

        btn = DirectOptionMenu(text='Resolución de pantalla', pos = (.5, 0, 0.6), parent = self.menu, scale=0.1, initialitem=0,
                                frameSize = (-4, 4, -1, 1), text_scale = 1.1, text_pos = (0, -0.2), command=juego.cambiar_pantalla, text_align=TextNode.ACenter, items=['800 x 600','1280 x 960', '1280 x 1024', '1920 x 1080'], 
                                highlightColor=(0.65, 0.65, 0.65, 1), textMayChange=1, clickSound = self.sonido_boton,                      frameTexture = self.boton_imagenes)
        btn.setTransparency(True)

        self.crear_etiqueta('Modo de pantalla', (-.5, 0, 0.2))
        
        botones = [
            DirectRadioButton(text='Pantalla Completa', variable=[1], value=[0], indicatorValue=False ,scale=0.08, pos=(0.5, 0, .23), 
                                command=juego.modo_pantalla, 
                                parent=self.menu, extraArgs=[True], clickSound = self.sonido_boton, text_font = self.fuente,
                                frameTexture = self.boton_imagenes),
            DirectRadioButton(text='Modo ventana', variable=[1], value=[1], indicatorValue=False, scale=0.08, pos=(0.43, 0, .10), 
                                command=juego.modo_pantalla, 
                                parent=self.menu, extraArgs=[False], clickSound = self.sonido_boton, text_font = self.fuente,
                                frameTexture = self.boton_imagenes)
        ]

        for boton in botones:
            boton.setOthers(botones)

        self.crear_etiqueta('Musica', (-.5, 0, -0.2))
        self.volumen = DirectSlider(range=(0,100), 
                                    value=100, 
                                    pos = (.5, 0, -0.2), 
                                    pageSize=3, 
                                    command=juego.musica, 
                                    scale=0.4, 
                                    parent=self.menu, 
                                    frameTexture = self.boton_imagenes)

        btn_volver = self.crear_boton('Volver', juego.volver, (0, 0, -0.6))
        btn_volver.setTransparency(True)


class MenuPausa(Menu):
    def __init__(self, juego):
        super().__init__(juego)
        
        titulo = self.crear_etiqueta('Pausa', (0, 0, 0.8))
        titulo['text_scale'] = 2
      
        btn_continuar = self.crear_boton('Continuar', juego.pausa, (0, 0, 0.4))
        btn_continuar['text_scale'] = 1.4
        btn_continuar.setTransparency(True)
        btn_opc = self.crear_boton('Opciones', juego.opciones, (0, 0, 0))
        btn_opc.setTransparency(True)
        btn_menu = self.crear_boton('Menu', juego.menu, (0, 0, -0.4))
        btn_menu.setTransparency(True)
        

class PantallaFinal(Menu):
    def __init__(self, juego, puntos, texto):
        super().__init__(juego)
        
        self.juego = juego
        self.puntos = puntos
        titulo = self.crear_etiqueta('JUEGO TEMRINADO', (0, 0, 0.75))
        titulo['text_scale'] = 2
        titulo = self.crear_etiqueta(texto, (0, 0, 0.50))
        titulo['scale'] = 1
        titulo = self.crear_etiqueta(f'Puntos: {puntos}', (0, 0, 0.30))
        titulo['scale'] = 0.8

        self.ingreso = DirectEntry( text="", 
                                    scale=0.2, 
                                    width=5, 
                                    pos=(0, 0, 0), 
                                    initialText="Nombre", 
                                    numLines=1, 
                                    focusInCommand=self.limpiar_texto,
                                    frameColor=(1,1,1,1), 
                                    cursorKeys=1, 
                                    command=self.guardar_puntos, 
                                    text_fg = (0,0,0,0.2),
                                    text_font=self.fuente,
                                    parent=self.menu,
                                    text_align=TextNode.ACenter)
        
        self.btn_guardar = self.crear_boton('Guardar', self.guardar_puntos, (0, 0, -0.3))

        self.btn_guardar.setTransparency(True)
        
        self.mensaje_guardado = OnscreenText(text = f'Guardado', 
                                            pos = (0, -0.25), 
                                            scale=.12, 
                                            fg=(255,255,255,255), 
                                            align = TextNode.ACenter, 
                                            parent = self.menu,
                                            font = self.fuente)
        self.mensaje_guardado.hide()
        
        
        self.btn_r = self.crear_boton('Reiniciar', juego.jugar, (-0.5, 0, -0.5))
        self.btn_r.setTransparency(True)
        self.btn_r.hide()
        self.btn_m = self.crear_boton('Menu', juego.menu, (0.5, 0, -0.5))
        self.btn_m.setTransparency(True)
        self.btn_m.hide()
        
        self.nombre_len = 10
        juego.taskMgr.add(self.limitar_texto, "limitarEntradas")

    def limpiar_texto(self):
        self.ingreso.enterText('')
        self.ingreso['text_fg']=(0,0,0,1)
        
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
            
        if len(nombre) > 2:
            puntos = self.puntos
            puntaje = {'nombre': nombre.upper(), 'puntos': puntos}
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
            puesto = OnscreenText(text = f'{i+1}.', pos = (-1, 0.5 - i * 0.15), mayChange = True, scale=.2, fg=(1,.5,0,255), align = TextNode.ARight, parent = self.menu
                            ,font = self.fuente)
            nombre = OnscreenText(text = jugador['nombre'], pos = (-0.9, 0.5 - i * 0.15), scale=.2, fg=(1,.5,0,255), align = TextNode.ALeft, parent = self.menu
                            ,font = self.fuente)
            pts = OnscreenText(text = str(jugador['puntos']), pos = (1, 0.5 - i * 0.15), scale=.2, fg=(1,.5,0,255), align = TextNode.ARight, parent = self.menu
                            ,font = self.fuente)
        
        btn_menu = self.crear_boton('Menu', juego.menu, (0, 0, -0.6))
        btn_menu.setTransparency(True)
