from panda3d.core import BitMask32

BIT_JUGADOR = BitMask32.bit(1)
BIT_PAREDES = BitMask32.bit(2)
BIT_ENEMIGOS = BitMask32.bit(3)
BIT_NPCs = BitMask32.bit(4)
BIT_OBJETOS = BitMask32.bit(5)

ESTADO = {'MENU': 0, 'CARGANDO': 1, 'JUGANDO': 2, 'PAUSA': 3, 'PAUSA_OPC': 4, 'FINALIZADO': 5}

