import subprocess

import os
from typing import Dict
import pygame

from line import Line
from circle import Circle, Vertex

def screenCapture(screen: pygame.Surface, file_name: str) -> str:
    pygame.image.save(screen, "assets/{}.jpg".format(file_name))
    return "![]({}.jpg)\n".format(file_name)

def highlightNode(
    nodes: Dict[str, Vertex],
    nodeTohighlight: str | None | list[str],
    grayedOutColour: pygame.Color = "gray",
    highlightColour: pygame.Color = "pink",
):
    for _, node in nodes.items():
        node.setBackgroundColour(grayedOutColour)
    if nodeTohighlight is not None and isinstance(nodeTohighlight, str):
        nodes[nodeTohighlight].setBackgroundColour(highlightColour)
    if nodeTohighlight is not None and isinstance(nodeTohighlight, list):
        for highlight in nodeTohighlight:
            nodes[highlight].setBackgroundColour(highlightColour)

def chooseLowestDistanceNode(nodes_distance: Dict[str, int], unvisited_node: list[str]) -> str:
    return min(unvisited_node, key=lambda x: nodes_distance[x])


def chooseUnvisitedNeighbour(items: list[str],unvisited_vertex: str):
    return [item for item in items if item in unvisited_vertex]
def awaitKey(
    screen: pygame.Surface,
    lines: list[Line],
    vertice: list[Vertex],
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

        for line in lines:
            line.draw()

        for object in vertice:
            object.draw()

        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60


def visualised(screen, lines, vertices, clock, start, end, unvisited_node, nodes_distance: Dict[str, str], nodes_previous: Dict[str, None | str], steps: int):
    outputText = ""
    outputText += screenCapture(screen, str(steps))
    outputText += ("unvisited_vertex:\n")
    outputText += ("{}\n".format(unvisited_node))
    outputText += ("\n")
    outputText += "| vertex | distance from start | previous vertex |\n"
    outputText += "| ------ | ------------------- | --------------- |\n"
    liner = []
    for vertex in nodes_distance.keys():
        liner.append("| {} | {} | {} |\n".format(vertex,nodes_distance[vertex] if nodes_distance[vertex] != 100000 else "inf", nodes_previous[vertex]))
    outputText += "".join(liner)
    outputText += ("\n")
    outputText += ("\n")
    awaitKey(screen, lines, vertices, clock, start, end)
    return outputText

def dijkstraVisualisation(
    screen: pygame.Surface, lines: list[Line], vertices: list[Vertex]
):
    outputMarkdownText = ""
    start = "A"
    end = "C"
    steps = 1

    clock = pygame.time.Clock()
    nodes = {}
    lines_node = {}
    connections = {}

    current_node = start

    # Variables that are displaying
    unvisited_node = [] 
    nodes_distance = {}
    nodes_previous = {}


    for vertex in vertices:
        nodes[vertex.text] = vertex
        nodes_distance[vertex.text] = 100000
        nodes_previous[vertex.text] = None

    unvisited_node = list(nodes.keys())

    for line in lines:
        if line.connection[1] not in connections:
            connections[line.connection[1]] = []
        if line.connection[0] not in connections[line.connection[1]]:
            connections[line.connection[1]].append(line.connection[0])

        if line.connection[0] not in connections:
            connections[line.connection[0]] = []
        if line.connection[1] not in connections[line.connection[0]]:
            connections[line.connection[0]].append(line.connection[1])

        lines_node["{}-{}".format(min(line.connection, key=lambda x: ord(x)), max(line.connection, key=lambda x: ord(x)))] = line


    nodes[start].setBackgroundColour("red")
    nodes[end].setBackgroundColour("green")
    visualised(screen, lines, vertices, clock, start, end, unvisited_node, nodes_distance, nodes_previous, steps)
    steps += 1

    # step 1: Mark all nodes as unvisited
    outputMarkdownText += "**step 1**: Mark all vertex as unvisited\n"
    highlightNode(nodes, None)
    outputMarkdownText += visualised(screen, lines, vertices, clock, start, end, unvisited_node, nodes_distance, nodes_previous, steps)
    steps += 1

    # step 2: Mark all other nodes to infinity
    outputMarkdownText += "**step 2**: Mark all other nodes to infinity\n"
    current_node = start
    highlightNode(nodes, current_node)
    nodes_distance[start] = 0
    outputMarkdownText += visualised(screen, lines, vertices, clock, start, end, unvisited_node, nodes_distance, nodes_previous, steps)
    steps += 1

    # step 3: STARTING LOOP
    outputMarkdownText += "**step 3**: start a while loop\n"
    outputMarkdownText += "\n"
    outputMarkdownText += "**step 3a**: For the current node, calculate all unvisited neighbors. Place the previous node on it.\n"
    outputMarkdownText += "\n"
    outputMarkdownText += "**step 3b**: Update the shortest distance, if new distance is shorter\n"
    outputMarkdownText += "\n"
    outputMarkdownText += "**step 3c**: Mark current node as visited\n"
    while unvisited_node != []:

        # reset visual
        for line in lines:
            line.updateColour("orange")

        chooseunvisited = chooseUnvisitedNeighbour(connections[current_node], unvisited_node)

        for connectedNode in chooseunvisited:
            connected = [current_node, connectedNode]
            connectedLine = lines_node["{}-{}".format(min(connected, key=lambda x: ord(x)), max(connected, key=lambda x: ord(x)))]
            connectedLine.updateColour("green")
            connectionValue = int(connectedLine.text)
            if nodes_distance[connectedNode] is None:
                nodes_distance[connectedNode] = connectionValue
                nodes_previous[connectedNode] = current_node
            elif (nodes_distance[current_node] + connectionValue) < nodes_distance[connectedNode]:
                nodes_distance[connectedNode] = connectionValue + nodes_distance[current_node]
                nodes_previous[connectedNode] = current_node

        highlightNode(nodes, current_node)
        unvisited_node.remove(current_node)
        outputMarkdownText += visualised(screen, lines, vertices, clock, start, end, unvisited_node, nodes_distance, nodes_previous, steps)
        steps += 1

        if unvisited_node != []:
            current_node = chooseLowestDistanceNode(nodes_distance, unvisited_node) 

    # highlight paths
    outputMarkdownText += "**step 5**: after there are no unvisited_node, calculate the paths\n"
    outputMarkdownText += "\n"
    outputMarkdownText += "**step 5a**: the path are calculated by tracing back the previous node\n"
    highlightNode(nodes, [start, end], highlightColour="red")
    awaitKey(screen, lines, vertices, clock, start, end)
    current_node = end
    while current_node != start:
        previous = nodes_previous[current_node]
        nodes[previous].setBackgroundColour("red")
        connected = [current_node, previous]
        connectedLine = lines_node["{}-{}".format(min(connected, key=lambda x: ord(x)), max(connected, key=lambda x: ord(x)))]
        connectedLine.updateColour("red")
        current_node = previous
        awaitKey(screen, lines, vertices, clock, start, end)

    awaitKey(screen, lines, vertices, clock, start, end)
    outputMarkdownText += screenCapture(screen, "final")
    
    # reset everything
    highlightNode(nodes, None, grayedOutColour="blue")
    for line in lines:
        line.updateColour("orange")

    with open("finalMarkdown.md", "w") as file:
        file.write(outputMarkdownText)
        print("saved")
    subprocess.Popen("pandoc -f gfm -t docx finalMarkdown.md --resource-path=assets -o final.docx", shell=True)
    print("converted")
        


    # pandoc command 
    # pandoc -f gfm -t docx finalMarkdown.md --resource-path=assets -o final.docx
