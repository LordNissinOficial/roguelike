import pygame as pg

class Quarto:
	def __init__(self, x, y, largura, altura):
		self.x = x
		self.y = y
		self.largura = largura
		self.altura = altura
		self.Rect = pg.Rect((max(0, x-1), max(0, y-1), largura+2, altura+2))
	
	def criar(self, grid):
		centro = self.centro()
		for y in range(self.y, self.y+self.altura):
			for x in range(self.x, self.x+self.largura):
				if y in [self.y, self.y+self.altura-1] and grid[y][x]==" ":
					grid[y][x] = "-"
				elif x in [self.x, self.x+self.largura-1]and grid[y][x]==" ":
					grid[y][x] = "|"
				else:
					grid[y][x] = "."
	
	def centro(self):
		
		return [int(self.x+self.largura/2), int(self.y+self.altura/2)]
		
	def colidindo(self, quarto):
		return self.Rect.colliderect(quarto.Rect)