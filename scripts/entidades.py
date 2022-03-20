from scripts.componentes import *
import scripts.funcoes as funcoes

class Entidade:
	def __init__(self, x, y, nome, char, cor, jogo):
		self.nome = nome
		self.jogo = jogo
		self.x = x
		self.y = y
		self.ai = Ai(self)
		self.hp = 10
		self.dmg = 4
		self.defesa = 0
		self.char = char
		self.cor = cor
	
	def podeMover(self, x, y):
		return self.jogo.grid[self.y+y][self.x+x]=="."
		
	def fazerTurno(self):
		if funcoes.naVisaoDoJogador(self, self.jogo):			
			return

		jogador = self.jogo.entidades[0]

		if self.ai:

			movimento = self.ai.conseguirMovimento([self.x, self.y], [jogador.x, jogador.y], self.jogo.grid, self.jogo.entidades)

			if movimento==[jogador.x, jogador.y]:
				self.atacar(jogador)
			else:
				self.x = movimento[0]
				self.y = movimento[1]
	
	def atacar(self, inimigo):
		dano = max(0, self.dmg-inimigo.defesa)
		self.jogo.console.log(f"{self.nome} atacando {inimigo.nome}.")

		inimigo.receberDano(dano)
	
	def receberDano(self, dano):
		self.hp -= dano
		
class Jogador(Entidade):
	def __init__(self, x, y, jogo):
		Entidade.__init__(self, x, y, "jogador", "@", (64, 154, 215), jogo)
		self.ai = None
		self.dmg = 5
	
	def fazerTurno(self, x, y):
		if self.podeMover(x, y):
			posNova = [self.x+x, self.y+y]
			for entidade in self.jogo.entidades:
				if not type(entidade)==Jogador:
					if posNova==[entidade.x, entidade.y]:
						self.atacar(entidade)
						return
						
			self.x += x
			self.y += y
			
class HobGoblin(Entidade):
	def __init__(self, x, y, jogo):
		Entidade.__init__(self, x, y, "hobgoblin", "H", (231, 179, 155), jogo)

class Morcego(Entidade):
	def __init__(self, x, y, jogo):
		Entidade.__init__(self, x, y, "morcego", "M", (64, 154, 215), jogo)
		self.ai = AiAleatoria(self)
	
	def fazerTurno(self):
		if funcoes.naVisaoDoJogador(self, self.jogo):			
			return

		jogador = self.jogo.entidades[0]

		if self.ai:
			movimento = self.ai.conseguirMovimento([self.x, self.y], [jogador.x, jogador.y], self.jogo.grid, self.jogo.entidades)

			if movimento==[jogador.x, jogador.y]:
				self.atacar(jogador)
			else:
				atacou = False
				for movimento2 in [[0, 1], [0, -1], [1, 0], [-1, 0], [1, 1], [1, -1], [-1, 1], [-1, -1]]:
					if [self.x+movimento2[0], self.y+movimento2[1]]==[jogador.x, jogador.y]:
						self.atacar(jogador)
						atacou = True
						break
				if not atacou:
					print(self.x, movimento[0])
					print(self.y, movimento[1])
					self.x = movimento[0]
					self.y = movimento[1]

class Escada(Entidade):
	def __init__(self, x, y, jogo):
		Entidade.__init__(self, x, y, "escada", "<", (223, 228, 39), jogo)
		self.ai = None
		
	def fazerTurno(self):
		pass
	
	def receberDano(self, dano):
		self.jogo.reiniciar()
		print("reiniciado")