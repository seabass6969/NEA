import subprocess

import os
from typing import Dict
import pygame

from line import RouteLine
from circle import Circle, Vertex


def awaitKey(
    screen: pygame.Surface,
    lines: dict[str,RouteLine],
    vertice: dict[str, Vertex],
    clock: pygame.time.Clock,
    start: str,
    end: str,
):
    key_pressed = False
    circleStart = Circle(screen, 20, (20, 20), start, "darkgreen")
    circleEnd = Circle(screen, 20, (80, 20), end, "red")

    while not key_pressed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                key_pressed = True
        screen.fill("white")

        circleStart.draw()
        circleEnd.draw()
        pygame.draw.line(screen, "black", (41, 20), (59, 20), 2)
        pygame.draw.line(screen, "black", (54, 18), (59, 20), 2)
        pygame.draw.line(screen, "black", (54, 22), (59, 20), 2)

        for line in lines.values():
            line.draw()

        for object in vertice.values():
            object.draw()

        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60
def visualised(
    screen: pygame.Surface,
    lines: dict[str,RouteLine],
    vertice: dict[str, Vertex],
    clock: pygame.time.Clock,
    start: str,
    end: str
):
    awaitKey(screen, lines, vertice, clock, start, end)


def raptorVisualisation(
    screen: pygame.Surface, lines: dict[str,RouteLine], vertices: dict[str, Vertex]
):
    outputMarkdownText = ""
    start = "A"
    end = "C"
    steps = 1

    clock = pygame.time.Clock()

    # Variables that are displaying

    visualised(screen, lines, vertices, clock, start, end)
        


    # pandoc command 
    # pandoc -f gfm -t docx finalMarkdown.md --resource-path=assets -o final.docx
