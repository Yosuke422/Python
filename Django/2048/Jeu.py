from tkinter import font, messagebox
import pygame
import random

class Main:
    
    pygame.init()
    screen = pygame.display.set_mode((500,500))
    pygame.display.set_caption('2048')

    def __init__(self):
        self.board = Board()
        self.run()

    def back (self):
        #le background
        self.screen.fill((255,255,255))
        #affichage de l'écran
        self.board.paint(self.screen)
        pygame.display.flip()

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.board.move("LEFT")
                if event.key == pygame.K_RIGHT:
                    self.board.move("RIGTH")
                if event.key == pygame.K_UP:
                    self.board.move("UP")
                if event.key == pygame.K_DOWN:
                    self.board.move("DOWN")
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()

    # mettre a jour la fonction.
    def update(self):
        self.board.update_cases()

    # boucle du jeu
    def run(self):

        self.running = True
        while self.running:
            
            self.event()
            self.update()
            self.back()

    
class cases:
    def __init__(self,x,y,num):
        #  num = 2,4,8,16,32,64,128...
        self.x = x
        self.y = y
        self.num = num
        self.colorlist = [(255,255,255),(255,255,255),(255,255,255),(255,255,255),(255,255,255),(255,255,255),(255,255,255),(255,255,255),(255,255,255),(255,255,255),(255,255,255)]

    # deplace une case avec les nouveau coordonnee 
    def move_cases(self,x=0,y=0):
        self.x += x
        self.y += y
        if self.x<0 or self.x > 3 or self.y < 0 or self.y > 3:
            self.x -= x
            self.y -=y
            return False
        return True

    # Fusionner 2 cases.
    def merge_cases(self,case): 
        if case.num == self.num:
            self.num +=1
            return True
        else:
            return False

   
    # Afficher les nouveau cases.
    def draw(self,screen,x,y,font):
        pygame.draw.rect(screen,self.colorlist[self.num-1],(x,y,87,87))

        # afficher les nombres dans les cases
        if self.num <= 2:
            color = (0,0,0)
        else:
            color = (255,34,62)
        #cree un surface du text 
        text = font.render(str(2**self.num),2,color)
        screen.blit(text,(x+(100/2 - text.get_width()/2), y + ( 100/2-text.get_height()/2)))


class Board:
    def __init__(self):
        ## self.cases track les positions des cases
        self.cases = [[0,0,0,0] for i in range(4)]
        self.board = pygame.Rect(50,50,400,400)
        self.color = (0,0,0)
        # casearray store les cases dans un liste. 
        self.casearray = []
        self.add_case()
        self.font = pygame.font.SysFont('',60)


    #affiche le background du board.
    def paint(self,screen):
        pygame.draw.rect(screen,self.color,self.board)
        self.drawcases(screen)

    # afficher les cases dans le screen.
    def drawcases(self,screen):
        for i,array in enumerate(self.cases):
            for j,case in enumerate(array):
                if case == 0:
                    pygame.draw.rect(screen,(255,248,234),(60+i*87+10*i,60+j*87+10*j,87,87))
                else:
                    case.draw(screen,60+i*87+10*i,60+j*87+10*j,self.font)

    # Retourne un arraylist avec les positions dans self.cases
    def get_empty_spaces(self):
        empty = []
        for i,array in enumerate(self.cases):
            for j,case in enumerate(array):
                if case==0:
                    empty.append([i,j])

        return empty

    # Ajoute une case.
    def add_case(self):
        empty = self.get_empty_spaces()
        chosen = random.choice(empty)

        if random.randrange(1,100) <10:
            num = 2
        else:
            num = 1

        t = cases(chosen[0],chosen[1],num)

        self.casearray.append(t)

    # deplacement de tout les cases.
    def move(self,key):

        steps = 0
        if key=="LEFT":
            for i, array in enumerate(self.cases):
                for j, _ in enumerate(array):
                    case = self.cases[j][i]
                    if case!=0:
                        steps += self.movecase(case,-1,0)
                    self.update_cases()
        if key =="RIGTH":
            for i,array in enumerate(self.cases):
                for j,_ in enumerate(array):
                    case = self.cases[3-j][3-i]
                    if case!= 0:
                        steps+= self.movecase(case,1,0)
                    self.update_cases()
        if key == "UP":
            for i,array in enumerate(self.cases):
                for j,_ in enumerate(array):
                    case = self.cases[i][j]
                    if case!=0:
                        steps += self.movecase(case,0,-1)
                    self.update_cases()
        if key == "DOWN":
            for i, array in enumerate(self.cases):
                for j,_ in enumerate(array):
                    case = self.cases[3-i][3-j]
                    if case!=0:
                        steps += self.movecase(case,0,1)
                    self.update_cases()
        if steps>0:
            self.add_case()
  
    def positioncase(self,x,y):
        if x>-1 and x<4 and y>-1 and y<4:
            return True

    def emptycase(self,x,y):
        if self.cases[x][y] == 0:
            return True
    # les cases dans l'arraylist va se mettre a jour dans self.cases
    def update_cases(self):
        self.cases = [[0,0,0,0] for i in range(4)]
        for case in self.casearray:
            self.cases[case.x][case.y] = case
    # deplace une seul case avec les nouveau coordonnee
    def movecase(self,case,x1=0,y1=0):
        steps = 0
        for i in range(0,3):
            if self.positioncase(case.x+x1,case.y+y1) and self.emptycase(case.x+x1,case.y+y1):
                case.move_cases(x1,y1)
                steps+=1
            else:
                if self.positioncase(case.x+x1,case.y+y1) and self.cases[case.x+x1][case.y+y1].merge_cases(case):
                    self.casearray.remove(case)
                    steps += 1

        return steps

   
m=  Main()  