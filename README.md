
# Zombies Ate My Neighbors 3D



## Descripción

Juego basado en el título Zombies Ate My Neighbors, desarrollado en Panda3D y con jugabilidad en primera persona. 

## Objetivo
Deberás salvar a todos tus vecinos de la llegada de los zombies. 
En cada nivel encontrarás una cantidad de vecinos a salvar mientras luchas por sobrevivir. Una vez que los hayas encontrado, se abrirá un portal en el spawn del personaje para poder avanzar.

## Características

### Puntuación
- **+100** puntos por cada zombie derrotado
- **+500** puntos por cada item recogido
- **+1000** puntos por cada vecino salvado

### Interfaz de usuario

- **Menú principal**: se despliegan los botones para jugar, ir a opciones, ver puntuaciones o salir del juego
- **Menú pausa**: pausa el juego y permite entrar a las opciones, volver al menú o continuar jugando
- **HUD**: información en pantalla del jugador. (Vida, puntos, vecinos salvados, balas)
- **Pantalla final**: permite guardar la puntuación obtenida al terminar la partida, y reiniciar el juego o volver al menú principal


### Controles

- **W/A/S/D**: Moverse
- **Mouse**: Apuntar
- **Click izquierdo**: Disparar
- **ESC**: Pausa/Reanudar
## Instalación

### 1) Clonar repositorio

```bash
  git clone https://github.com/a-tello/proyecto_panda3D.git
```
    
### 2) Crear entorno virtual

```bash
  python -m venv venv_juego
```

### 3)  Activar entorno virtual

```bash
  .\venv_juego\Scripts\activate
```

### 4) Instalar dependencias

```bash
  pip install -r requirements.txt
```

### 5) Correr el juego

```bash
  python main.py
```
    