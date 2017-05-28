import random
import sys
import pygame
from pygame.locals import *

#CLASSES ------
class MyRect(Rect):
	def __init__(self, cords, size, type, revealed=False):
		super().__init__(cords, size)
		self.type = type
		self.revealed = revealed
#CLASSES ------

#FUNCTIONS ------
#quit program
def terminate():
	pygame.quit()
	sys.exit()

#get a representation of a board	
def getBoard(shapes):
	assert len(shapes) == NUMPEICES
	
	tempShapes = shapes #return shapes after poping
	print(tempShapes) ####FIX
	
	board = []
	
	random.shuffle(shapes)
	
	for x in range(MARGIN, WIDTH-MARGIN, BOXSIZE):
		for y in range(MARGIN, HEIGHT-MARGIN, BOXSIZE):
			if len(shapes) == 0:
				break
			board.append(MyRect((x, y), (BOXSIZE, BOXSIZE),
			                            shapes.pop(), False)) 
										
	shapes = tempShapes
	
	print(shapes)
	
	return board
 
#draw a board based on pieces attributes 
def drawBoard(board, imgDict):
	for piece in board:
		for type, img in imgDict.items():
			if piece.type == type and piece.revealed:
				DISPLAYSURF.blit(img, (piece.left, piece.top))

#determines if two pieces match				
def match(pieces):
	if len(pieces) != 2:
		return False

	if pieces[0].type == pieces[1].type:
		return True
		
	return False

#reveal a hidden piece	
def reveal(piece):
	if not piece.revealed:
		piece.revealed = True

#hide a revealed piece		
def hide(piece):
	if piece.revealed:
		piece.revealed = False

#highlight a rect/piece		
def highlight(piece, color, lineWidth):
	pygame.draw.line(DISPLAYSURF, color, (piece.left, piece.top), 
		             (piece.left + piece.width, piece.top), lineWidth)
					 
	pygame.draw.line(DISPLAYSURF, color, (piece.left, piece.top), 
		             (piece.left, piece.top + piece.height), lineWidth)
					 
	pygame.draw.line(DISPLAYSURF, color, 
		             (piece.left + piece.width, piece.top), 
		             (piece.left + piece.width, piece.top + piece.height), 
						                                             lineWidth)
													 
	pygame.draw.line(DISPLAYSURF, color, 
		             (piece.left, piece.top + piece.height), 
		             (piece.left + piece.width, piece.top + piece.height), 
						                                             lineWidth)
																	 
def renderText(font, text, color, location):
	textSurfaceObj     = font.render(text, True, color)
	textRectObj        = textSurfaceObj.get_rect()
	textRectObj.center = (location)
	DISPLAYSURF.blit(textSurfaceObj, textRectObj)
#FUNCTIONS ------

#GLOBALS ------
BOXSIZE       = 100
MARGIN        = 50 
HEIGHT, WIDTH = 600, 600
WINDOWSIZE    = (HEIGHT, WIDTH)
DISPLAYSURF   = pygame.display.set_mode(WINDOWSIZE)
NUMPEICES     = 20
#GLOBALS ------

#COLORS ------
BLACK = (  0, 0,   0)
RED   = (255, 0,   0)
BLUE  = (  0, 0, 255)
#COLORS ------
def main():
	pygame.init()
	pygame.display.set_caption("Memory Madness!")
	
	fpsClock = pygame.time.Clock()
	fps      = 30
	
	backImg = pygame.image.load("images/back.png").convert()
	oImg = pygame.image.load("images/o.png").convert()
	xImg = pygame.image.load("images/x.png").convert()
	tImg = pygame.image.load("images/t.png").convert()
	dImg = pygame.image.load("images/d.png").convert()
	hImg = pygame.image.load("images/h.png").convert()
	yImg = pygame.image.load("images/y.png").convert()
	zImg = pygame.image.load("images/z.png").convert()
	kImg = pygame.image.load("images/k.png").convert()
	bImg = pygame.image.load("images/b.png").convert()
	cImg = pygame.image.load("images/c.png").convert()
	movesImg = pygame.image.load("images/moves.png").convert()
	refreshImg = pygame.image.load("images/refresh.png").convert()
	
	imgDict = {'x': xImg,
			   'o': oImg,
			   't': tImg,
			   'd': dImg,
			   'h': hImg,
			   'y': yImg,
			   'z': zImg,
			   'k': kImg,
			   'b': bImg,
			   'c': cImg,}
	
	shapes = ['x', 'x', 
	          'o', 'o', 
			  't', 't',
			  'd', 'd',
			  'h', 'h',
			  'y', 'y',
			  'z', 'z',
			  'k', 'k',
			  'b', 'b',
			  'c', 'c']
			  
	board = getBoard(shapes)
	
	piecesChoosen = []
	
	numMoves      = 0
	scoreLocation = (245, 575) 
	
	font = pygame.font.Font('freesansbold.ttf', 34)
	
	#MENU ------
	buttonsize  = (100, 40)
	movesRect   = Rect((MARGIN+BOXSIZE, 555), (buttonsize))
	refreshRect = Rect((MARGIN, 555), (buttonsize))
	#MENU ------
	
	#SOUND ------

	#SOUND ------
	while True:
		DISPLAYSURF.fill(BLACK)
		
		drawBoard(board, imgDict)
		
		DISPLAYSURF.blit(movesImg,   (movesRect.left, movesRect.top))
		DISPLAYSURF.blit(refreshImg, (refreshRect.left, refreshRect.top))
		
		for piece in board:
			if not piece.revealed:
				DISPLAYSURF.blit(backImg, (piece.left, piece.top))
			if piece.collidepoint(pygame.mouse.get_pos()):
				highlight(piece, RED, 3)
				
		if refreshRect.collidepoint(pygame.mouse.get_pos()):
			highlight(refreshRect, RED, 3)
			
		for event in pygame.event.get():
			if event.type == QUIT:
				terminate()
				
			elif event.type == MOUSEBUTTONUP:
				if len(piecesChoosen) == 2:
					if match(piecesChoosen):
						numMoves += 1
						piecesChoosen = []
					else:
						numMoves += 1
						for piece in piecesChoosen:
							hide(piece)
						piecesChoosen = []
				if len(piecesChoosen) < 2:
					for piece in board:
						if piece.collidepoint(pygame.mouse.get_pos()) and not piece.revealed:	
							reveal(piece)
							piecesChoosen.append(piece)
				if refreshRect.collidepoint(pygame.mouse.get_pos()):
					for peice in board:
						peice.revealed = False
					numMoves      = 0
					
					shapes = ['x', 'x', 
							  'o', 'o', 
							  't', 't',
							  'd', 'd',
							  'h', 'h',
							  'y', 'y',
							  'z', 'z',
							  'k', 'k',
							  'b', 'b',
							  'c', 'c']
							  
					board = getBoard(shapes)
					piecesChoosen = []
			
		renderText(font, str(numMoves), BLUE, scoreLocation)
		
		if numMoves > 999:
			numMoves = 999
				
		pygame.display.update()
		fpsClock.tick(fps)

if __name__ == "__main__":
	main()