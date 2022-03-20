import pygame as pg
from scripts.jogo import Jogo

pg.init()
#pg.font.init()

def main():
	tela = pg.display.set_mode((1920, 1080))
	jogo = Jogo()
	clock = pg.time.Clock()
	while True:
		jogo.update()
		jogo.show(tela, str(round(clock.get_fps())))
		pg.display.update()
		clock.tick(30)
		
if __name__=="__main__":
	main()