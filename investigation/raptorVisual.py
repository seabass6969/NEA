import json
import math
import subprocess

import os
from typing import Dict
import pygame

from line import RouteLine
from circle import Circle, Vertex


def awaitKey(
    screen: pygame.Surface,
    lines: dict[str, RouteLine],
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
    lines: dict[str, RouteLine],
    vertice: dict[str, Vertex],
    clock: pygame.time.Clock,
    start: str,
    end: str,
):
    awaitKey(screen, lines, vertice, clock, start, end)


def timeparser(time: str | None):
    # example 23:04
    if time is None:
        return math.inf
    else:
        times = [int(i) for i in time.split(":")]
        return (times[0] * 60 + times[1]) * 60


def timeparser_reverer(time: int):
    return "{}:{}".format(time // 60 // 60, (time // 60) % 60)


def footpathsCalculation(vertexA: Vertex, vertexB: Vertex):
    return int(
        (vertexA.centerLocation[0] - vertexB.centerLocation[0]) ** 2
        + (vertexA.centerLocation[1] - vertexB.centerLocation[1]) ** 2
    )


def raptorVisualisation(
    screen: pygame.Surface, lines: dict[str, RouteLine], vertices: dict[str, Vertex]
):
    file = json.load(open("arrangement_raptor.json"))
    routeList = file["route_list"]
    timetablesList = file["timetable"]
    timetables = {}

    for timetable in timetablesList:
        timetables[timetable["trip"]] = timetable

    stopsRoute = {}
    routes = {}
    for rout in routeList:
        for connected in rout["connections"]:
            if connected not in stopsRoute:
                stopsRoute[connected] = []
            stopsRoute[connected].append(rout["line_name"])
        routes[rout["line_name"]] = rout

    print(stopsRoute)

    outputMarkdownText = ""
    startingTime = "10:00"
    start = "A"
    end = "C"
    steps = 1
    improvement = True

    clock = pygame.time.Clock()

    # Variables that are displaying
    # τ_k (p) arrival time for k rounds and stop p
    arrival_time_per_round = {}
    round_k = 0
    mark_updated = set()

    # initialising data
    # all the label are initialised to be infinity, in this case None
    arrival_time_per_round[round_k] = {}
    for vertex in vertices.keys():
        arrival_time_per_round[round_k][vertex] = None
    arrival_time_per_round[round_k][start] = startingTime

    mark_updated.add(start)

    print(mark_updated)
    print(arrival_time_per_round[round_k])
    visualised(screen, lines, vertices, clock, start, end)
    # rounds start
    while improvement:
        round_k += 1
        # stage 1: copy previous round
        # copy τ_k (p) = τ_{k-1} (p)
        arrival_time_per_round[round_k] = {}
        for vertex in vertices.keys():
            arrival_time_per_round[round_k][vertex] = arrival_time_per_round[
                round_k - 1
            ][vertex]

        # stage 2: process routes
        # search through marked stops
        # check its route
        currentRoundMarked = [marked for marked in mark_updated]
        for marked in currentRoundMarked:
            for route in stopsRoute[marked]:
                canWeBoard = False
                markedStopTime = timeparser(arrival_time_per_round[round_k][marked])
                for time in timetables[route]["schedules"]:
                    if time["stop"] == marked:
                        if timeparser(time["time"]) <= markedStopTime:
                            canWeBoard = True
                            arrival_time_per_round[round_k][marked] = time["time"]

                # mark_updated.remove(marked)  # unmark p
                if canWeBoard:
                    # traverse route onwards
                    for connectedStop in routes[route]["connections"]:
                        markedStopTime = timeparser(
                            arrival_time_per_round[round_k][connectedStop]
                        )
                        for time in timetables[route]["schedules"]:
                            if time["stop"] == connectedStop:
                                if timeparser(time["time"]) <= markedStopTime:
                                    arrival_time_per_round[round_k][connectedStop] = (
                                        time["time"]
                                    )
                                    # mark p
                                    # change p's earlist arrival time
                                    mark_updated.add(connectedStop)


        print()
        print("round {}".format(round_k))
        print(mark_updated)
        print(arrival_time_per_round[round_k])
        visualised(screen, lines, vertices, clock, start, end)
        # # stage 3: footpaths
        currentRoundMarked = [marked for marked in mark_updated]
        for marked in currentRoundMarked:
            if (footpathsCalculation(vertices[marked], vertices[end]) + timeparser(arrival_time_per_round[round_k][marked])) < timeparser(arrival_time_per_round[round_k][end]):
                mark_updated.add(end)

        if currentRoundMarked == mark_updated:
            improvement = False
    visualised(screen, lines, vertices, clock, start, end)

    # pandoc command
    # pandoc -f gfm -t docx finalMarkdown.md --resource-path=assets -o final.docx
