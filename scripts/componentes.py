import pyastar2d
#from math import inf
import numpy, random

class Ai():
	def __init__(self, entidade):
		self.entidade = entidade
		self.weights = numpy.array([[1 for _ in range(len(entidade.jogo.grid[0]))] for _ in range(len(entidade.jogo.grid))], dtype=numpy.float32)
		for y in range(len(entidade.jogo.grid)):
			for x in range(len(entidade.jogo.grid[0])):
				if entidade.jogo.grid[y][x] in "|- ":
					self.weights[y][x] = 9999
					
	def conseguirMovimento(self, comeco, destino, grid, entidades):
		
		
		
		#print(comeco, destino)
		#print(comeco[::-1], destino[::-1])
		path = list(pyastar2d.astar_path(self.weights, comeco[::-1], destino[::-1], allow_diagonal=True))
		if len(path)==1:
			return comeco
		b = path[1][::-1]
		
		if grid[b[1]][b[0]] in "|- ":
			return comeco
		return list(b)

class AiAleatoria():
	def __init__(self, entidade):
		self.entidade = entidade
	
	def conseguirMovimento(self, comeco, destino, grid, entidades):
		movimentos = [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]
		#movimento = comeco
		random.shuffle(movimentos)
		for movimento in movimentos:
			if grid[comeco[1]+movimento[1]][comeco[0]+movimento[0]]==".":
				print([comeco[0]+movimento[0], comeco[1]+movimento[1]])
				return [comeco[0]+movimento[0], comeco[1]+movimento[1]]
		return comeco
#		for i in range(10):
#			if random.choice()