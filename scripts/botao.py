import pygame as pg

pg.init()

class Botao():
	def __init__(self, x, y, funcao):
		self.funcao = funcao
		#self.args = args
		#self.img = pg.image.load("recursos/sprites/botoes/"+img+".png").convert()
#		self.img.set_colorkey((0, 0, 0))
		self.Rect = pg.Rect((x, y, 30, 30))#, self.img.get_size())
		self.pressionado = False

	def pressionando(self, mousePos):
		if self.Rect.collidepoint(mousePos):
			self.pressionado = True
		else:
			self.pressionado = False
	
	def pressionar(self, mousePos):
		if self.Rect.collidepoint(mousePos):
			self.pressionado = False
			self.funcao()#*self.args, jogo)
			
	def show(self, display):
		pg.draw.rect(display, (40, 53, 83), self.Rect)
		if self.pressionado:
			pg.draw.rect(display, (20, 33, 63), self.Rect)
		#display.blit(self.img, self.Rect)