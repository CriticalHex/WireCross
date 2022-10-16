import os
import pygame
import random

pygame.init()

BLUE = (0, 0, 200)
PINK = (200, 0, 200)
RED = (200, 0, 0)
GREEN = (0, 100, 0)
WHITE = (255, 255, 255)


class Port:
    def __init__(self, Color: tuple[int, int, int], Pos: tuple[int, int]) -> None:
        self.x = Pos[0]
        self.y = Pos[1]
        self.w = 100
        self.h = 50
        self.color = Color
        self.wired = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))


class Wire:
    def __init__(self, start, color) -> None:
        self.color = color
        self.startPos = start
        self.stopPos = None
        self.set = False

    def draw(self, screen):
        pygame.draw.line(screen, self.color, self.startPos, self.stopPos, 10)


def setup():
    LPos = [(100, 100), (100, 300), (100, 500), (100, 700)]
    RPos = [(550, 100), (550, 300), (550, 500), (550, 700)]
    random.shuffle(LPos)
    random.shuffle(RPos)
    return [
        Port(RED, LPos[0]),
        Port(GREEN, LPos[1]),
        Port(PINK, LPos[2]),
        Port(BLUE, LPos[3]),
        Port(RED, RPos[0]),
        Port(GREEN, RPos[1]),
        Port(PINK, RPos[2]),
        Port(BLUE, RPos[3]),
    ]


def getPort(mousePos, ports: list[Port]):
    for p in ports:
        if (
            mousePos[0] >= p.x
            and mousePos[0] <= p.x + p.w
            and mousePos[1] >= p.y
            and mousePos[1] <= p.y + p.h
        ):
            return p
    return None


def highlight(screen, port: Port):
    pygame.draw.rect(screen, WHITE, (port.x, port.y, port.w, port.h), 1)


def center(port: Port):
    return (port.x + (port.w / 2), port.y + (port.h / 2))


screen = pygame.display.set_mode((800, 800))
MousePos = (0, 0)

ports = setup()
wires: list[Wire] = []
edit = None

running = True
while running:
    for event in pygame.event.get():
        MousePos = pygame.mouse.get_pos()
        hovering = getPort(MousePos, ports)
        if event.type == pygame.QUIT:
            running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL]:
            running = False
        if keys[pygame.K_LSHIFT]:
            os.system("cls")
            ports = setup()
            wires: list[Wire] = []
        if event.type == pygame.MOUSEBUTTONDOWN:
            if hovering is not None and edit is None and not hovering.wired:
                start = hovering
                wires.append(Wire(center(hovering), hovering.color))
                edit = wires[-1]
        if event.type == pygame.MOUSEBUTTONUP:
            if len(wires) > 0:
                if (
                    hovering is not None
                    and hovering is not start
                    and not hovering.wired
                    and edit is not None
                ):
                    if hovering.color != edit.color:
                        wires.pop(-1)
                    else:
                        edit.stopPos = center(hovering)
                        hovering.wired = True
                        start.wired = True
                        edit.set = True
                    edit = None
                elif wires[-1].set == False:
                    wires.pop(-1)
                    edit = None

    if edit is not None:
        edit.stopPos = MousePos

    screen.fill((0, 0, 0))

    for p in ports:
        p.draw(screen)

    for p in ports:
        if not p.wired:
            break
    else:
        print("You Win!")

    for w in wires:
        w.draw(screen)

    if hovering is not None:
        highlight(screen, hovering)

    pygame.display.flip()
