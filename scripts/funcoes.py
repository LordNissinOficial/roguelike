from scripts.config import *
from functools import cache
#DISPLAY_TAMANHO = 4

def telaParaDisplay(pos):
	
	return [int(pos[0]/TELA_TAMANHO[0]*DISPLAY_TAMANHO[0]), int(pos[1]/TELA_TAMANHO[1]*DISPLAY_TAMANHO[1])]

#@cache
def naVisaoDoJogador(entidade, jogo):
	
	jogador = jogo.entidades[0]
	yInicial = min(len(jogo.grid)-GRID_VISIVEL[1], max(0, jogador.y-GRID_VISIVEL[1]//2))
	xInicial = min(len(jogo.grid[0])-GRID_VISIVEL[0], max(0, jogador.x-GRID_VISIVEL[0]//2))
	yFinal = min(yInicial//16+GRID_VISIVEL[1], len(jogo.grid))
	xFinal = min(xInicial//16+GRID_VISIVEL[0], len(jogo.grid[0]))
	return xInicial>=entidade.x<=xFinal and yInicial>=entidade.y<=yFinal