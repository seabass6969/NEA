# Example file showing a basic pygame "game loop"
import pygame
import random
import json
from circle import Vertex, Circle
from alphabets import vertices
from line import RouteLine
from raptorVisual import raptorVisualisation

# pygame setup
pygame.init()
# screenSize = (1280, 700)
screenSize = (1000, 400)
screen = pygame.display.set_mode(screenSize)
clock = pygame.time.Clock()
running = True

vertices_index = 0
movableCircle = Circle(screen, 30, (50, 50), vertices[vertices_index])
measurementCircle = Circle(screen, 10, (50, 50), "")

objects = {}
routeLines = {}
routeLinesOn = -1

mode = "edit"
print("edit mode")
joiningA = None
joiningB = None

current = {}

def snapToGrid(pos: tuple[int, int]):
    return ((pos[0] // 100) * 100, (pos[1] // 100) * 100)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if mode == "edit":
                objects[vertices_index] = (
                    Vertex(
                        screen,
                        vertices[vertices_index],
                        snapToGrid(pygame.mouse.get_pos()),
                    )
                )
                if vertices_index < (len(vertices) - 1):
                    vertices_index += 1
                    movableCircle.updateText(vertices[vertices_index])
                else:
                    mode = "normal"
                    print("normal mode")
            elif mode == "joining":
                for object in objects.values():
                    clickedObject = object.mouseClicked(pygame.mouse.get_pos())
                    if clickedObject is not None:
                        if joiningA is None:
                            joiningA = clickedObject
                            print("joiningA is", joiningA.text)
                        elif joiningB is None:
                            joiningB = clickedObject
                            print("joiningB is", joiningB.text)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            with open("arrangement_raptor.json", "w") as file:
                dumping = {
                    "stops_list": [
                        (objecter.non_str()) for objecter in objects.values()
                    ],
                    "route_list": [{"line_name": key} | route.selfExportDetail() for key, route in routeLines.items()]
                }
                print(dumping)
                file.write(
                    json.dumps(
                    dumping
                    )
                )
            print("Saved")
        if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
            with open("arrangement_raptor.json", "r") as file:
                objects = {}
                routeLines = {}
                jsonFile = json.load(file)
                object_list = jsonFile["stops_list"]
                routes = jsonFile["route_list"]
                for objecter in object_list:
                    objects[objecter["name"]] = (
                        Vertex(screen, objecter["name"], objecter["location"])
                    )
                for route in routes:
                    routeLines[route["line_name"]] = RouteLine(screen, route["line_name"], route["lineColour"])
                    for line in route["drawableLines"]:
                        routeLines[route["line_name"]].addConnections(objects[line["connectionA"]], objects[line["connectionB"]])

            print("Imported")
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            mode = "edit"
            print("edit mode")
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            mode = "normal"
            print("normal mode")
        if event.type == pygame.KEYDOWN and event.key == pygame.K_j:
            joiningA = None
            joiningB = None
            mode = "joining"
            print("joining mode")
            print("new joining line created")
            routeLinesOn += 1
            routeLines["t{}".format(routeLinesOn)] = RouteLine(screen, "t{}".format(routeLinesOn), random.choice(["red", "orange", "green"]))

        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            if mode == "autoupdate":
                mode = "normal"
            else:
                mode = "autoupdate"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            mode = "measurement"
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            mode = "raptor"


    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    if joiningA is not None and joiningB is not None:
        print("joining line")
        routeLines["t{}".format(routeLinesOn)].addConnections(joiningA, joiningB)
        joiningA = None
        joiningB = None
    # RENDER YOUR GAME HERE

    if mode == "autoupdate":
        with open("arrangement_raptor.json", "r") as file:
            jsonFile = json.load(file)
            if current != jsonFile:
                current = jsonFile
                objects = {}
                routeLines = {}
                object_list = jsonFile["stops_list"]
                routes = jsonFile["route_list"]
                for objecter in object_list:
                    objects[objecter["name"]] = (
                        Vertex(screen, objecter["name"], objecter["location"])
                    )
                for route in routes:
                    routeLines[route["line_name"]] = RouteLine(screen, route["line_name"], route["lineColour"])
                    for line in route["drawableLines"]:
                        routeLines[route["line_name"]].addConnections(objects[line["connectionA"]], objects[line["connectionB"]])
                print("Updated")

    if mode == "measurement":
        measurementCircle.updateLocation(snapToGrid(pygame.mouse.get_pos()))
        measurementCircle.draw()
        print(snapToGrid(pygame.mouse.get_pos()))

    if mode == "edit":
        movableCircle.updateLocation(snapToGrid(pygame.mouse.get_pos()))
        movableCircle.draw()

    for line in routeLines.values():
        line.draw()

    for object in objects.values():
        object.draw()
    if mode == "joining":
        for object in objects.values():
            object.eventChecker(pygame.mouse.get_pos())

    if mode == "raptor":
        raptorVisualisation(screen, routeLines, objects)
        mode = "normal"
    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
