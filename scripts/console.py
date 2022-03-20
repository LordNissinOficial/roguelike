import pygame as pg
from time import time
from scripts.config import *

class Console:
	def __init__(self):
		self.timer = time()
		self.textoMaxSize = 10
		self.textos = []
	
	def show(self, x, y, display, fonte):
		if time()-self.timer>4:
			if len(self.textos)>0:
				self.textos.pop(0)
			self.timer = time()
			
		for index, texto in enumerate(self.textos[::-1]):
			render = fonte.render(texto[0], 0, texto[1])
			display.blit(render, (x, y+GRID_VISIVEL[1]*16-index*16-16-8))
	
	def log(self, texto, cor=(40, 53, 83)):

		textos = []
		self.timer = time()
		for i in range(0, len(texto), self.textoMaxSize):
			textos.append([texto[i:i+self.textoMaxSize], cor])
		
		for texto in textos:
			self.textos.append(texto)
		
		while len(self.textos)>=21:
			self.textos = self.textos[1:len(self.textos)]