import sys
import pygame
from pygame.locals import *

# importar nuestras clases
from clases import jugador
from clases import asteroide
from random import randint
from time import time


# variables
ANCHO=480
ALTO=700
listaAsteroide = []
puntos = 0
colorFuente = (120, 200, 40)

# booleano juego
jugando = True

# función principal
# carga asteroides
def cargarAsteroides(x,y):
    meteoro = asteroide.Asteroide(x,y)
    listaAsteroide.append(meteoro)

def gameOver():
    global jugando
    jugando = False
    for meteoritos in listaAsteroide:
        listaAsteroide.remove(meteoritos)

def meteoritos():
    pygame.init()
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    #Imagen fondo
    fondo = pygame.image.load("./imagenes/fondo.png")
    
    #Título
    pygame.display.set_caption("Meteoritos")
    
    # crea objeto jugador
    nave = jugador.Nave()
    contador = 0
    
    # sonidos
    pygame.mixer.music.load("K:\OneDrive\Programación\Tutoriales\pygames\meteorito\sonidos/meteoritos_sonidos_fondo.wav")
    pygame.mixer.music.play(3)
    sonidoColision = pygame.mixer.Sound("K:\OneDrive\Programación\Tutoriales\pygames\meteorito\sonidos/meteoritos_sonidos_colision.aiff")

    #fuente marcador
    fuenteMarcador = pygame.font.SysFont("Arial", 10)


    #ciclo del juego
    while True:

        ventana.blit(fondo, (0,0))
        nave.dibujar(ventana)
        # tiempo
        tiempo = time()
        # marcador
        global puntos
        textoMarcador = fuenteMarcador.render("Puntos: "+str(puntos), 0, colorFuente )
        ventana.blit(textoMarcador, (0,0))
        # creamos asteroides
        if tiempo - contador >1:
            contador = tiempo
            posX = randint(2, 478)
            cargarAsteroides(posX, 0)
        
        #comprobar lista asteroide
        if len(listaAsteroide)>0:
            for x in listaAsteroide:
                if jugando == True:
                    x.dibujar(ventana)
                    x.recorrido()
                    if x.rect.top > ALTO:
                        listaAsteroide.remove(x)
                    else:
                        if x.rect.colliderect(nave.rect):
                            listaAsteroide.remove(x)
                            sonidoColision.play()
                            # print("colisión nave / meteorito")
                            nave.vida = False
                            gameOver()
        # Disparo de proyectil
        if len(nave.listaDisparo)>0:
            for x in nave.listaDisparo:
                x.dibujar(ventana)
                x.recorrido()
                if x.rect.top<-10:
                    nave.listaDisparo.remove(x)
                else:
                    for meteoritos in listaAsteroide:
                        if x.rect.colliderect(meteoritos.rect):
                            listaAsteroide.remove(meteoritos)
                            nave.listaDisparo.remove(x)
                            puntos +=1
                            # print("Colisión Disparo / meteorito")
        nave.mover()

        for evento in pygame.event.get():
            if jugando == True:
                if evento.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == K_LEFT:
                        nave.rect.left -= nave.velocidad
                    elif evento.key == K_RIGHT:
                        nave.rect.right += nave.velocidad
                    elif evento.key == K_SPACE:
                        x, y = nave.rect.center
                        nave.disparar(x, y)
        if jugando == False:
            FuenteGameOver = pygame.font.SysFont("Arial", 40)
            textoGameOver = FuenteGameOver.render("Game Over", 0, colorFuente)
            ventana.blit(textoGameOver, (140,350))
            pygame.mixer.music.fadeout(3000)

        pygame.display.update()

# llamada a función principal
meteoritos()