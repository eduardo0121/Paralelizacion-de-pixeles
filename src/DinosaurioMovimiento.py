import matplotlib.pyplot as plt
import matplotlib.animation as animacion
import numpy as np
import threading
import random

N_FRAMES = 60
ANCHO = 50
ALTO = 20
N_HILOS = 4

frames = [np.zeros((ALTO, ANCHO)) for _ in range(N_FRAMES)]
lock = threading.Lock()


OBJETOS = {
    'nube': np.array([
        [0,0,0,1,1,0,0],
        [0,1,1,1,1,1,0],
        [1,1,1,1,1,1,1],
        [0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0]
    ]),
    'piedra': np.array([
        [0,0,0,0,0,0],
        [0,0,1,1,1,0],
        [1,1,1,1,1,1],
        [1,1,1,1,1,1]
    ]),
    'arbol': np.array([
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0],
        [0,0,1,1,1,1,0,0],
        [0,0,1,1,1,1,0,0],
        [0,1,1,1,1,1,1,0],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0],
        [0,0,0,1,1,0,0,0]
    ])
}

def crear_fondo():
    fondo = np.zeros((ALTO, ANCHO))
    fondo[-1:, :] = 1  # Piso del recorrido

    for x in range(0, ANCHO, 15):
        tipo = random.choice(list(OBJETOS.keys()))
        obj = OBJETOS[tipo]
        alt, anc = obj.shape  # variables de altura y ancho
        
        pos_x = min(x, ANCHO - anc)
        pos_y = 0 if tipo == 'nube' else ALTO - alt - 1
        
        if pos_y + alt <= ALTO:
            fondo[pos_y:pos_y+alt, pos_x:pos_x+anc] = np.maximum(
                fondo[pos_y:pos_y+alt, pos_x:pos_x+anc], obj)

    return fondo

FONDO = crear_fondo()

def crear_dino(pie_izq=True):
    dino = np.array([
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,1,1,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,1,1,0,0,0,0],
        [0,0,0,1,1,1,1,1,0,1,1,1,0,0],
        [0,0,0,1,1,1,1,1,1,1,1,1,0,0],
        [0,0,0,0,1,1,1,1,1,1,0,0,0,0],
        [0,0,0,0,0,1,1,1,1,0,0,0,0,0],
        [0,1,0,0,0,1,1,1,1,0,0,0,0,0],
        [0,1,1,0,1,1,1,1,1,1,0,0,0,0],
        [0,1,1,0,1,1,1,1,1,1,1,1,0,0],
        [0,0,1,1,1,1,1,1,1,1,0,1,0,0],
        [0,0,1,1,1,1,1,1,1,1,0,0,0,0],
        [0,0,0,1,1,1,1,1,1,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,1,0,0,0,0,0,0],
        [0,0,0,0,1,1,0,1,1,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ])
    #animacion de pies
    if pie_izq:
        dino[14:16, 4:6] = 0
    else:
        dino[14:16, 7:9] = 0

    return dino

def generar_frames(inicio, fin):
    for i in range(inicio, fin):
        escena = np.copy(FONDO)
        dino = crear_dino(i % 2 == 0)
        
        x = (i * 2) % (ANCHO - dino.shape[1])
        y = 3
        
        escena[y:y+dino.shape[0], x:x+dino.shape[1]] = np.maximum(
            escena[y:y+dino.shape[0], x:x+dino.shape[1]], dino)

        with lock:
            frames[i] = escena

# Paralelismo
hilos = []
por_hilo = N_FRAMES // N_HILOS

for i in range(N_HILOS):
    ini = i * por_hilo
    fin = (i + 1) * por_hilo if i != N_HILOS - 1 else N_FRAMES
    h = threading.Thread(target=generar_frames, args=(ini, fin))
    hilos.append(h)
    h.start()

for h in hilos:
    h.join()

#Parte de la animacion 
fig, ax = plt.subplots(figsize=(10, 5))
img = ax.imshow(frames[0], cmap='binary')
plt.axis('off')

def actualizar(i):
    img.set_array(frames[i % N_FRAMES])
    return img,

ani = animacion.FuncAnimation(
    fig, actualizar, frames=N_FRAMES, interval=100, blit=True
)
plt.tight_layout()
plt.show()