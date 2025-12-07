#tudo que foi necessário importar
import pygame
import sys
import random
import os
import json #salvar o placar dos jogadores 
from pygame.locals import *

#para começar a usar o pygame
pygame.init()
pygame.mixer.init()

#cores
BRANCO = (255, 255, 255)  #escrita
AZUL_CLARO = (135, 206, 250) #fundo de tela
VERDE = (0, 255, 0) #jogador 1
LARANJA = (255, 165, 0) #jogador 2

#tamanho e velocidade
TAMANHO_JOGADOR=20
TAMANHO_MACA=10
FPS=30
TEMPO = 120  # Duração do jogo em segundos

#controle do tempo
inicio=pygame.time.get_ticks()
tempo_passado=0
tempo_falta=TEMPO

#iniciar o jogo 
ativar_jogo=True

# Configurações da tela
tela=pygame.display.set_mode((800,800)) #tamanho da tela
pygame.display.set_caption("Jogo da cobrinha para dois jogadores") #titulo da janela
relogio=pygame.time.Clock()
letra=pygame.font.SysFont("arial", 15) #fonte dos textos
largura, altura = tela.get_size() 


#função do movimento dos jogadores
def movimento(jogador, teclas): 
    if teclas[jogador['controles']['cima']]:jogador['vertical'] -= jogador['velocidade'] #move para cima 
    if teclas[jogador['controles']['baixo']]:jogador['vertical'] += jogador['velocidade'] #move para baixo 
    if teclas[jogador['controles']['esquerda']]:jogador['horizontal'] -= jogador['velocidade'] #move para esquerda 
    if teclas[jogador['controles']['direita']]:jogador['horizontal'] += jogador['velocidade'] #move para direita 
    jogador['cobrinha'] = pygame.Rect(jogador['horizontal'], jogador['vertical'], jogador['tamanho'], jogador['tamanho']) #atualiza a posição do jogador

'''Essa parte da colisão encontrei muita dificuldade,nessa parte tive auxilio do GIMINI,pois antes a colisão não ocorria'''
#"pegar" as maçãs
def colisao(jogador, maca):
    if jogador['cobrinha'].colliderect(maca['maca']):
        jogador['pontuação'] += 1
        return True
    return False

#coloca o maçã em  posição aleatória da tela
def aleatorio(maca, largura, altura):
    maca['horizontal'] = random.randint(30, largura - 30)
    maca['vertical'] = random.randint(30, altura - 30)
    maca['maca'] = pygame.Rect(maca['horizontal'] - maca['tamanho'], maca['vertical'] - maca['tamanho'], maca['tamanho'] * 2, maca['tamanho'] * 2)


#Para mover os jogadores pelas teclas
controles_1 = {'cima': K_w, 'baixo': K_s, 'esquerda': K_a, 'direita': K_d} #teclas do jogador 1 (WASD)
jogador1={'cor': VERDE,'tamanho': TAMANHO_JOGADOR,'horizontal': 100, 'vertical': 100,'retangulo': None,'velocidade': 10,'pontuação': 0,'controles': controles_1}
jogador1['cobrinha'] = pygame.Rect(jogador1['horizontal'], jogador1['vertical'], jogador1['tamanho'], jogador1['tamanho'])
controles_2 = {'cima': K_UP, 'baixo': K_DOWN, 'esquerda': K_LEFT, 'direita': K_RIGHT} #teclas do jogador 2(setas do teclado)
jogador2={'cor': LARANJA,'tamanho': TAMANHO_JOGADOR,'horizontal': 700, 'vertical': 700,'retangulo': None,'velocidade': 10,'pontuação': 0,'controles': controles_2}
jogador2['cobrinha'] = pygame.Rect(jogador2['horizontal'], jogador2['vertical'], jogador2['tamanho'], jogador2['tamanho'])

#Maçãs (coletáveis)
laranja = {'cor': LARANJA,'tamanho': TAMANHO_MACA,'horizontal': 0, 'vertical': 0,'rect': None}
aleatorio(laranja, largura, altura) #coloca a maçã em uma posição aleatória
limao = {'cor': VERDE,'tamanho': TAMANHO_MACA,'horizontal': 0, 'vertical': 0,'rect': None}
aleatorio(limao, largura, altura)

#Loop principal do jogo
while True:
    tela.fill(AZUL_CLARO) #fundo de tela
    teclas=pygame.key.get_pressed() #pega as teclas pressionadas

   
    if ativar_jogo:
         #controle do tempo
        tempo_passado=(pygame.time.get_ticks()-inicio)//1000
        tempo_falta=TEMPO-tempo_passado
        if tempo_falta <=0:
            ativar_jogo=False
    tempo_texto=letra.render(f"Tempo restante: {tempo_falta}",True,BRANCO)
    tela.blit(tempo_texto, (largura - 150, 10))

    for evento in pygame.event.get(): #processa os eventos
        if evento.type == QUIT: #se clicar no X da janela
                pygame.quit()
                sys.exit()
        if ativar_jogo:
            movimento(jogador1, teclas)
            movimento(jogador2, teclas)
        if colisao(jogador1, limao):
            aleatorio(limao, largura, altura)
        if colisao(jogador2, laranja):
            aleatorio(laranja, largura, altura)

#desenha os jogadores e as maçãs na tela
    pygame.draw.rect(tela, jogador1['cor'], jogador1['cobrinha'])
    pygame.draw.rect(tela, jogador2['cor'], jogador2['cobrinha'])
    pygame.draw.circle(tela, laranja['cor'], (laranja['horizontal'], laranja['vertical']), laranja['tamanho'])
    pygame.draw.circle(tela, limao['cor'], (limao['horizontal'], limao['vertical']), limao['tamanho'])

    pontuação_texto = letra.render(f"JOGADOR VERDE: {jogador1['pontuação']}         JOGADOR LARANJA: {jogador2['pontuação']}", True, BRANCO)
    if jogador1['pontuação'] == jogador2['pontuação']:
        resultado_texto = letra.render("EMPATE!", True, BRANCO)
    elif jogador1['pontuação'] > jogador2['pontuação']:
        resultado_texto = letra.render("JOGADOR 1 VENCE!", True, VERDE)
    else:
        resultado_texto = letra.render("JOGADOR 2 VENCE!", True, LARANJA)
    tela.blit(pontuação_texto, (10, 10))
    pygame.display.update() #atualiza a tela
    relogio.tick(FPS) 


'''COISAS QUE QUERIA TER COLOCADO,IDEIAS PARA MELHORAR O JOGO:
-Queria colocar uma música para tocar ao fundo
-Um som diferente pra quando cada jogador fazer 
-Tela inicial e de fim de jogo
-Guardar o placar para e comparar com outras rodadas
-Colocar a calda da "cobrinha",a cada ponto ir colocando dentro de uma lista 
-Se os jogadores colidirem entre si a rodada acaba (mesmo se ainda tiver tempo)
-Tela circular,como se os jogadores saíssem de um lado e conseguissem aparecer do outro
'''