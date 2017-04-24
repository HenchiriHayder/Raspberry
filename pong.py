import pygame
from pygame.locals import *
import socket
from queue import Queue
import threading

myQueue = Queue()

class Pong(object):
    def __init__(self, screensize):

        self.screensize = screensize

        self.centerx = int(screensize[0]*0.5)
        self.centery = int(screensize[1]*0.5)

        self.radius = 8

        self.rect = pygame.Rect(self.centerx-self.radius,
                                self.centery-self.radius,
                                self.radius*2, self.radius*2)

        self.color = (100,100,255)

        self.direction = [1,1]

        self.speedx = 2
        self.speedy = 5


        self.hit_edge_left = False
        self.hit_edge_right = False

    def update(self, player_paddle, ai_paddle):

        self.centerx += self.direction[0]*self.speedx
        self.centery += self.direction[1]*self.speedy

        self.rect.center = (self.centerx, self.centery)

        if self.rect.top <= 0:
            self.direction[1] = 1
        elif self.rect.bottom >= self.screensize[1]-1:
            self.direction[1] = -1

        if self.rect.right >= self.screensize[0]-1:
            self.hit_edge_right = True
        elif self.rect.left <= 0:
            self.hit_edge_left = True

        

        if self.rect.colliderect(player_paddle.rect):
            self.direction[0] = -1
        if self.rect.colliderect(ai_paddle.rect):
            self.direction[0] = 1

    def render(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius, 0)
        pygame.draw.circle(screen, (0,0,0), self.rect.center, self.radius, 1)


class AIPaddle(object):
    def __init__(self, screensize):
        self.screensize = screensize

        self.centerx = 5
        self.centery = int(screensize[1]*0.5)

        self.height = 100
        self.width = 10

        self.rect = pygame.Rect(0, self.centery-int(self.height*0.5), self.width, self.height)

        self.color = (255,100,100)

        

        self.speed = 5

    def update(self, pong):
        if pong.rect.top < self.rect.top:
            self.centery -= self.speed
        elif pong.rect.bottom > self.rect.bottom:
            self.centery += self.speed

        self.rect.center = (self.centerx, self.centery)

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (0,0,0), self.rect, 1)


class PlayerPaddle(object):
    def __init__(self, screensize):
        self.screensize = screensize

        self.centerx = screensize[0]-5
        self.centery = int(screensize[1]*0.5)

        self.height = 100
        self.width = 10

        self.rect = pygame.Rect(0, self.centery-int(self.height*0.5), self.width, self.height)

        self.color = (100,255,100)

        

        self.speed = 3
        self.direction = 0

    def update(self):
        self.centery += self.direction*self.speed

        self.rect.center = (self.centerx, self.centery)
        if self.rect.top < 0:
            self.rect.top = 0
			self.centery = self.height//2
        if self.rect.bottom > self.screensize[1]-1:
            self.rect.bottom = self.screensize[1]-1
			self.centery = self.screensize[1]-self.height//2

    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, 0)
        pygame.draw.rect(screen, (0,0,0), self.rect, 1)


def insert_In_Queue():
    server = socket.socket()
    host = '127.0.0.1'
    port = 1234
    global myQueue

    server.bind((host, port))
    server.listen(1)
    print ("[*] Server started !")
    client, addr = server.accept()
    print("[*] Got connection from ip: ", addr[0])
    while True:
        data = client.recv(1024).decode()
        client.send(data.encode())
        myQueue.put(data);

#def retrieve_From_Queue():




def main():
    pygame.init()

    global myQueue

    screensize = (640,480)

    screen = pygame.display.set_mode(screensize)

    clock = pygame.time.Clock()
    data = ""

    pong = Pong(screensize)
    ai_paddle = AIPaddle(screensize)
    player_paddle = PlayerPaddle(screensize)

    t = threading.Thread(target=insert_In_Queue)
    t.daemon = True
    t.start()

    running = True

    while running:
        #fps limiting/reporting phase
        clock.tick(64)

        #event handling phase
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        if(myQueue.empty()):
            player_paddle.direction = 0
        else:

            data = myQueue.get()
            myQueue.task_done()
            
            if(data == "z"):
                player_paddle.direction = -1
            elif(data == "s"):
                player_paddle.direction = 1
            else:
                player_paddle.direction = 0

        #object updating phase
        ai_paddle.update(pong)
        player_paddle.update()
        pong.update(player_paddle, ai_paddle)


        if pong.hit_edge_left:
            print ("You Won")
            pong = Pong(screensize)
            ai_paddle = AIPaddle(screensize)
            player_paddle = PlayerPaddle(screensize)
           # running = False
        elif pong.hit_edge_right:
            print ("You Lose 2")
            pong = Pong(screensize)
            ai_paddle = AIPaddle(screensize)
            player_paddle = PlayerPaddle(screensize)
            #running = False

        #rendering phase
        screen.fill((100,100,100))

        ai_paddle.render(screen)
        player_paddle.render(screen)
        pong.render(screen)

        pygame.display.flip()

    pygame.quit()


main()
