from scripts.config import *
import pygame as pg
import random
from scripts.botao import Botao
from scripts.funcoes import *
from scripts.entidades import *
from scripts.quarto import Quarto
from scripts.console import Console

#print(DISPLAY_TAMANHO)
class Jogo:
	def __init__(self):
		self.botoes = [
			Botao(48, DISPLAY_TAMANHO[1]-48, lambda: self.mover(0, 1)       ),#cima
			Botao(80, DISPLAY_TAMANHO[1]-48, lambda: self.mover(1, 1)       ),#cima direita
			Botao(16, DISPLAY_TAMANHO[1]-48, lambda: self.mover(-1, 1)     ),#cima esquerda
			Botao(48, DISPLAY_TAMANHO[1]-112, lambda: self.mover(0, -1)   ),#baixo
			Botao(80, DISPLAY_TAMANHO[1]-112, lambda: self.mover(1, -1)   ),#baixo direita
			Botao(16, DISPLAY_TAMANHO[1]-112, lambda: self.mover(-1, -1)),#baixo esquerda
			Botao(16, DISPLAY_TAMANHO[1]-80, lambda: self.mover(-1, 0)     ),#esquerda
			Botao(80, DISPLAY_TAMANHO[1]-80, lambda: self.mover(1, 0)       )#direita
		]
		self.display = pg.Surface(DISPLAY_TAMANHO).convert()
		self.fonte = pg.font.Font("recursos/PerfectDOSVGA437.ttf", 16)
		self.grid = [[" " for _ in range(64)] for _ in range(64)]
		self.entidades = [Jogador(1, 1, self)]
		self.console = Console()
		self.xPos = DISPLAY_TAMANHO[0]//2-GRID_VISIVEL[0]*16//2
		self.yPos = DISPLAY_TAMANHO[1]//2-GRID_VISIVEL[1]*16//2
		self.consoleXPos = self.xPos+GRID_VISIVEL[0]*16+2
		self.consoleYPos = self.yPos
		self.setUpGrid()
	
	def reiniciar(self):
		self.grid = [[" " for _ in range(64)] for _ in range(64)]
		self.console = Console()
		self.entidades = [Jogador(1, 1, self)]
		self.setUpGrid()
		
	def setUpGrid(self):
		quartos = []#Quarto(0, 0, 10, 9)]
		for i in range(random.choice([4, 8, 16])):
			largura = random.randint(5, 18)
			altura = random.randint(5, 18)
			quarto = Quarto(random.randint(0, len(self.grid[0])-largura-1), random.randint(0, len(self.grid)-altura-1), largura, altura)
			colidindo = False
			for outroQuarto in quartos:
				if outroQuarto.colidindo(quarto):
					colidindo = True
					break
			if not colidindo:
				if len(quartos)==0:
					self.entidades[0].x = random.randint(quarto.x+1, quarto.x+quarto.largura-2)
					self.entidades[0].y = random.randint(quarto.y+1, quarto.y+quarto.altura-2)
				##cria tuneis##
				
				#if len(quartos)>0:
					
				###########
				quartos.append(quarto)
				self.entidades.append(random.choice([HobGoblin, Morcego])(random.randint(quarto.x+1, quarto.x+quarto.largura-2), random.randint(quarto.y+1, quarto.y+quarto.altura-2), self))
		for index, quarto in enumerate(quartos):
			centro = quartos[-1].centro()
			quartoCentro = quarto.centro()
			if random.randint(0, 1)==1:
				self.criarTunelHorizontal(centro[0], quartoCentro[0], centro[1])
				self.criarTunelVertical(centro[1], quartoCentro[1], quartoCentro[0])
			else:
				self.criarTunelVertical(centro[1], quartoCentro[1], centro[0])
				self.criarTunelHorizontal(centro[0], quartoCentro[0], quartoCentro[1])
						
			quarto.criar(self.grid)
		self.entidades.append(Escada(random.randint(quartos[-1].x+1, quartos[-1].x+quartos[-1].largura-2), random.randint(quartos[-1].y+1, quartos[-1].y+quartos[-1].altura-2), self))
	
	def criarTunelHorizontal(self, x1, x2, y):
		for x in range(min(x1, x2), max(x2, x1)+1):
			self.grid[y][x] = "."
			
	def criarTunelVertical(self, y1, y2, x):
		for y in range(min(y1, y2), max(y2, y1)+1):
			self.grid[y][x] = "."
		
	def mover(self, x, y):
		#self.console.log(f"jogador movendo com x: {x} e y: {y}")
		#if self.entidades[0].podeMover(x, y):
		self.entidades[0].fazerTurno(x, y)
			
			
#			self.entidades[0].y %= len(self.grid)
#			self.entidades[0].x %= len(self.grid[0])
		for entidade in self.entidades:
			if entidade.hp<= 0:
				if type(entidade)==Jogador:
					self.reiniciar()
					return
				self.entidades.remove(entidade)
				continue
			if not type(entidade)==Jogador:
				entidade.fazerTurno()
#			
#	def podeMover(self, entidade, x, y):
#		return 
	def update(self):
		self.lidarEventos()
		
	def lidarEventos(self):
		for evento in pg.event.get():
			if evento.type==pg.QUIT:
				pass
			if evento.type in [pg.MOUSEBUTTONDOWN, pg.MOUSEMOTION]:
				pos = telaParaDisplay(list(evento.pos))
				for botao in self.botoes:
					botao.pressionando(pos)
				
			elif evento.type==pg.MOUSEBUTTONUP:
				pos = telaParaDisplay(list(evento.pos))
				for botao in self.botoes:
					botao.pressionar(pos)
		
	def show(self, tela, fps):		

		self.display.fill((9, 9, 27))
		
		entidadesPos = [[entidade.x, entidade.y] for entidade in self.entidades]
		jogador = self.entidades[0]
#		for y in range(len(self.grid)):
#			for x in range(len(self.grid[0])):
		yInicial = min(len(self.grid)-GRID_VISIVEL[1], max(0, jogador.y-GRID_VISIVEL[1]//2))*16
		xInicial = min(len(self.grid[0])-GRID_VISIVEL[0], max(0, jogador.x-GRID_VISIVEL[0]//2))*16
		grossura = 2+1
		pg.draw.rect(self.display, (40, 53, 83), (self.xPos-grossura, self.yPos-grossura, GRID_VISIVEL[0]*16+grossura*2, GRID_VISIVEL[1]*16+grossura*2), grossura-1)
		for y in range(yInicial//16, min(yInicial//16+GRID_VISIVEL[1], len(self.grid))):
			for x in range(xInicial//16, min(xInicial//16+GRID_VISIVEL[0], len(self.grid[0]))):
				char = self.grid[y][x]
				cor = (40, 53, 83)
	#			if char=="@":
#					cor = (64, 154, 215)

				if [x, y] in entidadesPos:
					entidade = self.entidades[entidadesPos.index([x, y])]
					render = self.fonte.render(entidade.char, 0, entidade.cor)
				else:
					render = self.fonte.render(char, 0, cor)

				if [x, y] in entidadesPos:
					self.display.blit(render, (self.xPos+entidade.x*16-xInicial, self.yPos+entidade.y*16-yInicial))
				else:
					self.display.blit(render, (self.xPos+x*16-xInicial, self.yPos+y*16-yInicial))
#		for entidade in self.entidades:
#			#entidade = self.entidades[entidadesPos.index([x, y])]
#			render = self.fonte.render(entidade.char, 0, entidade.cor)
#			self.display.blit(render, (self.xPos+entidade.x*16-xInicial, self.yPos+entidade.y*16-yInicial))
			
		for botao in self.botoes:		
			botao.show(self.display)
			
		self.display.blit(self.fonte.render(fps, 0, (40, 53, 83)), (10, 10))
		self.display.blit(self.fonte.render(AFF, 0, (40, 53, 83)), (10, 10))
		#self.display.blit(self.fonte.render("aventureiro deu 13 de dano ao orc.", 0, (100, 100, 150)), (10, 10))
		self.showConsole()
		tela.blit(pg.transform.scale(self.display, tela.get_size()), (0, 0))
	
	def showConsole(self):
		grossura = 2+1
		pg.draw.rect(self.display, (40, 53, 83), (self.consoleXPos+grossura+2, self.consoleYPos-grossura, 6*16, GRID_VISIVEL[1]*16+grossura*2), 2)
		self.console.show(self.consoleXPos+grossura+7, self.consoleYPos-grossura+2, self.display, self.fonte)