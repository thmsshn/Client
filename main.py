import datetime
import socket
import threading

import pygame
from pygame import *
from pygame.time import Clock
from Client import UDPClient
import time
from time import sleep
from playerCat import *
from lvl import *
from monsters import *
import sys
from playerDino import playerDino
from playerDino import *
from Client import *
from lvl import *

WIN_WIDTH = 800
WIN_HEIGHT = 640
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#89f571"

pygame.mixer.init()
soundtrack = pygame.mixer.Sound("levels/48bb90af8e1e401.mp3")
soundtrack.play(loops=-1)


class GameState:
    def __init__(self, ts, Pl1X, Pl1Y, Pl2X, Pl2Y, LastReq):
        self.TimeStamp = ts
        self.Pl1X = Pl1X
        self.Pl1Y = Pl1Y
        self.Pl2X = Pl2X
        self.Pl2Y = Pl2Y
        self.LastReq = LastReq


import time

prevGS = GameState(time.time(), 100, 100, 100, 100, 0)


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2
    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы
    return Rect(l, t, w, h)


def loadLevel():
    global playerX, playerY
    levelFile = open("levels/1.txt")
    line = " "
    commands = []
    while line[0] != "/":
        line = levelFile.readline()
        if line[0] == "[":
            while line[0] != "]":
                line = levelFile.readline()
                if line[0] != "]":
                    endLine = line.find("|")
                    level.append(line[0: endLine])
        if line[0] != "":
            commands = line.split()
            if len(commands) > 1:
                if commands[0] == "player":
                    playerX = int(commands[1])
                    playerY = int(commands[2])
                if commands[0] == "portal":
                    tp = BlockTeleport(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]))
                    entities.add(tp)
                    platforms.append(tp)


def FirstConnection(client, socket, entities):
    F = True
    while F:
        client.udp_echo_client_send_firstMessage()
        data, client_address = socket.recvfrom(1024)
        message = data.decode('utf-8')
        if (message == 'cat'):
            hero = playerCat(100, 100)
            hero2 = playerDino(100, 100)
            F = False
        if (message == 'dino'):
            hero = playerDino(100, 100)
            hero2 = playerCat(100, 100)
            F = False
    entities.add(hero)
    entities.add(hero2)
    import time

    threading.Thread(target=Receiver, args=(hero, hero2, socket)).start()
    return entities, hero, hero2


def Receiver(hero, hero1, client_socket):
    global prevGS
    while True:
        data, client_address = client_socket.recvfrom(1024)
        message = data.decode('utf-8')
        W = message.split(" ")

        if (len(message) < 3):
            continue
        Gs = GameState(W[1], W[2], W[3], W[4], W[5], W[6])
        if W[7] == 'True':
            print('winner!')
            font = pygame.font.Font(None, 36)
            text = font.render("Победитель", True, (255, 255, 255))
            text_rect = text.get_rect(center=(400, 100))
        if int(W[0]) == 0:
            # hero1.interpolate_coordinates(prevGS.Pl2X, prevGS.Pl2Y, Gs.Pl2X, Gs.Pl2Y, prevGS.TimeStamp,
            hero1.StartInter(prevGS.Pl2X, prevGS.Pl2Y, Gs.Pl2X, Gs.Pl2Y, prevGS.TimeStamp, Gs.TimeStamp)
            #                                  Gs.TimeStamp)
            hero.interpolate_coordinates(prevGS.Pl1X, prevGS.Pl1Y, Gs.Pl1X, Gs.Pl1Y, prevGS.TimeStamp, Gs.TimeStamp)
        else:
            hero1.interpolate_coordinates(prevGS.Pl1X, prevGS.Pl1Y, Gs.Pl1X, Gs.Pl1Y, prevGS.TimeStamp,
                                          Gs.TimeStamp)
            hero.StartInter(prevGS.Pl2X, prevGS.Pl2Y, Gs.Pl2X, Gs.Pl2Y, prevGS.TimeStamp, Gs.TimeStamp)
            # hero.interpolate_coordinates(prevGS.Pl2X, prevGS.Pl2Y, Gs.Pl2X, Gs.Pl2Y, prevGS.TimeStamp, Gs.TimeStamp)
        prevGS = Gs


def main(screen, weight, height):
    loadLevel()
    pygame.init()
    bi = image.load("blocks/Sprite-0001.png")
    bi = pygame.transform.scale(bi, (WIN_WIDTH, WIN_HEIGHT))
    win = screen
    pygame.display.set_caption("babushka")
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))
    bg.fill(Color(BACKGROUND_COLOR))

    left = right = False
    up = False
    running = False
    animCount = 0
    server_host = "188.120.237.31"
    server_port = 12345
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind(("0.0.0.0", 0))
    Client = UDPClient(server_host, server_port, client_socket)

    entities = pygame.sprite.Group()
    platforms = []
    tp = [BlockTeleport(162, 1038, 144, 1230), BlockTeleport(2365, 1808, 714, 144), BlockTeleport(660, 1296, 653, 1680),
          BlockTeleport(970, 912, 2195, 1552)]
    for i in range(4):
        entities.add(tp[i])
        platforms.append(tp[i])
        animatedEntities.add(tp[i])

    frame_timer = 0

    x = y = 0
    for row in level:
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "*":
                bd = BlockDie(x, y)
                entities.add(bd)
                platforms.append(bd)
            if col == "D":
                dr = Door(x, y)
                entities.add(dr)
                platforms.append(dr)
                animatedEntities.add(dr)

            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
        x = 0

    total_level_width = len(level[0]) * PLATFORM_WIDTH
    total_level_height = len(level) * PLATFORM_HEIGHT

    camera = Camera(camera_configure, total_level_width, total_level_height)

    PredictPos = []

    timer = pygame.time.Clock()
    entities, hero, hero2 = FirstConnection(Client, client_socket, entities)

    while 1:
        for e in pygame.event.get():
            if e.type == QUIT:
                raise SystemExit("QUIT")
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
                right = False

            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
                left = False

            if e.type == KEYDOWN and e.key == K_LSHIFT:
                running = True

            if e.type == KEYUP and e.key == K_UP:
                up = False

            if e.type == KEYUP and e.key == K_RIGHT:
                right = False

            if e.type == KEYUP and e.key == K_LEFT:
                left = False

            if e.type == KEYUP and e.key == K_LSHIFT:
                running = False
        timer.tick(60)
        frame_timer += 1
        #print(hero.rect.x," ",hero.rect.y)
        win.blit(bi, (0, 0))

        camera.update(hero)
        # hero.update(left, right, up, running, platforms)
        # PredictPos.append(str(hero.rect.x)+" "+str(hero.rect.y))
        ListInp = str(left) + " " + str(right) + " " + str(up) + " " + str(running)
        #  print(prevGS.Pl1X," ",prevGS.Pl1Y," ",PredictPos[int(prevGS.LastReq)])
        Client.udp_echo_client_send(ListInp)
        for e in entities:
            win.blit(e.image, camera.apply(e))
        pygame.display.update()
        # cpu_percent = psutil.cpu_percent(interval=1)  # интервал в секундах
        # print(f"Использование процессора: {cpu_percent}%")
        # memory_info = psutil.Process().memory_info()
        # Количество использованной памяти
        # used_memory = memory_info.rss
        # print(f"Использованная память: {used_memory} байт")


level = []
entities = pygame.sprite.Group()
animatedEntities = pygame.sprite.Group()
platforms = []


class Button:
    def __init__(self, x, y, weight, height, text, image_path, hover_image_path=None, sound_path=None):
        self.x = x
        self.y = y
        self.weight = weight
        self.height = height
        self.text = text

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, [weight, height])
        self.hover_image = self.image
        if hover_image_path:
            self.hover_image = pygame.image.load(hover_image_path)
            self.hover_image = pygame.transform.scale(self.hover_image, [weight, height])
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = None
        if sound_path:
            self.sound = pygame.mixer.Sound(sound_path)
        self.is_hovered = False

    def draw(self, screen):  # отрисовка кнопки на экране
        current_image = self.hover_image if self.is_hovered else self.image
        screen.blit(current_image, self.rect.topleft)

        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, [255, 255, 255])
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):  # проверка наведения мыши на кнопку
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def green_handle_event(self, event, screen, weight, height):  # действие кнопки начального меню
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            main(screen, weight, height)
            if self.sound:
                self.sound.play()

            pygame.quit()

    def red_handle_event(self, event):  # выход из игры в начальном меню
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            print('exit')
            # if self.sound:
            #     self.sound.play()
            pygame.quit()
            sys.exit()


def main_menu(green_button, screen, screen_weight, red_button, screen_height):
    interimage = pygame.image.load('sprite/Sprite-0002.png').convert_alpha()
    interimage = pygame.transform.scale(interimage, [screen_weight, screen_height])
    interimageRect = interimage.get_rect()

    running = True
    i = 0
    clock = pygame.time.Clock()
    while running:
        screen.fill((0, 0, 0))
        screen.blit(interimage, interimageRect)
        # label = pygame.font.Font(None, 72)
        # text_surface = label.render("babushka", True, [255, 255, 255])
        # text_rect = text_surface.get_rect(center=(screen_weight/2, 50))
        # screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            green_button.green_handle_event(event, screen, screen_weight, screen_height)
            red_button.red_handle_event(event)
        green_button.check_hover(pygame.mouse.get_pos())
        green_button.draw(screen)
        red_button.check_hover(pygame.mouse.get_pos())
        red_button.draw(screen)
        pygame.display.flip()
        clock.tick(150)


def start():
    button_weight, button_height = 150, 100
    screen_weight, screen_height = 800, 640  # размер окна приложения
    screen = pygame.display.set_mode([screen_weight, screen_height])  # создание окна приложения
    pygame.display.set_caption("babushka")  # название окна приложенния
    green_button = Button(screen_weight / 2 - (150 / 2), 340, button_weight, button_height, '', 'sprite/мордаК1.1.png',
                          'sprite/мордаК1.2.png')
    red_button = Button(screen_weight / 2 - (150 / 2), (green_button.y + green_button.height), button_weight,
                        button_height, '', 'sprite/мордад1.png', 'sprite/мордад2.png')
    main_menu(green_button, screen, screen_weight, red_button, screen_height)


if __name__ == "__main__":
    pygame.init()
    start()
