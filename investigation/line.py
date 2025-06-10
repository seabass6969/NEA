import pygame
from circle import Vertex


class Line:
    def __init__(
        self,
        screen: pygame.Surface,
        startPos: tuple[int, int],
        endPos: tuple[int, int],
        text: int,
        connection: tuple[str, str],
        colour: pygame.Color = "orange",
        textColour: pygame.Color = "black",
    ):
        self.screen = screen
        self.colour = colour
        self.textColour = textColour
        self.text = str(text)
        self.startPos = startPos
        self.endPos = endPos
        self.FONT = pygame.font.Font("JetBrainsMono-Regular.ttf", 20)
        self.textObj = self.FONT.render(self.text, True, self.textColour, None)
        self.textSurface = pygame.Surface(self.textObj.get_size())
        self.textSurface.fill((220, 220, 220))
        self.textSurface.blit(self.textObj, self.textObj.get_rect())
        self.textObj = self.textSurface
        self.connection = connection
        self.centerLocation = (
            (self.startPos[0] + self.endPos[0]) / 2,
            (self.startPos[1] + self.endPos[1]) / 2,
        )
        self.textCenterLocation = (
            self.centerLocation[0] - self.textObj.get_width() / 2,
            self.centerLocation[1] - self.textObj.get_height() / 2,
        )

    def draw(self):
        pygame.draw.line(self.screen, self.colour, self.startPos, self.endPos, 3)
        if self.text != 0:
            self.screen.blit(self.textObj, self.textCenterLocation)

    def updateStartLocation(self, newLocation: tuple[int, int]):
        self.startPos = newLocation
        self.centerLocation = (
            (self.startPos[0] + self.endPos[0]) / 2,
            (self.startPos[1] + self.endPos[1]) / 2,
        )
        self.textCenterLocation = (
            self.centerLocation[0] - self.textObj.get_width() / 2,
            self.centerLocation[1] - self.textObj.get_height() / 2,
        )

    def updateEndLocation(self, newLocation: tuple[int, int]):
        self.endPos = newLocation
        self.centerLocation = (
            (self.startPos[0] + self.endPos[0]) / 2,
            (self.startPos[1] + self.endPos[1]) / 2,
        )
        self.textCenterLocation = (
            self.centerLocation[0] - self.textObj.get_width() / 2,
            self.centerLocation[1] - self.textObj.get_height() / 2,
        )

    def updateText(self, newText: str):
        self.textObj = self.FONT.render(newText, True, self.textColour, None)
        self.textCenterLocation = (
            self.centerLocation[0] - self.textObj.get_width() / 2,
            self.centerLocation[1] - self.textObj.get_height() / 2,
        )

    def updateColour(self, newColour):
        self.colour = newColour

    def __str__(self):
        return str(
            {
                "startPos": self.startPos,
                "endPos": self.endPos,
                "centerLocation": self.centerLocation,
                "value": int(self.text),
                "connection": self.connection,
            }
        )

    def non_str(self):
        return {
            "startPos": self.startPos,
            "endPos": self.endPos,
            "centerLocation": self.centerLocation,
            "value": int(self.text),
            "connection": self.connection,
        }


class RouteLine:
    def __init__(
        self,
        screen: pygame.Surface,
        lineName: str,
        stops: dict[str, Vertex],
        lineColour: pygame.Color = "orange",
        textColour: pygame.Color = "black",
    ):
        self.screen = screen
        self.connections = []
        self.drawableLines = []
        self.stopsList = []
        self.lineName = lineName
        self.lineColour = lineColour
        self.textCenterLocations = []

        self.textColour = textColour
        self.FONT = pygame.font.Font("JetBrainsMono-Regular.ttf", 20)
        self.textObj = self.FONT.render(self.lineName, True, self.textColour, None)
        self.textSurface = pygame.Surface(self.textObj.get_size())
        self.textSurface.fill((220, 220, 220))
        self.textSurface.blit(self.textObj, self.textObj.get_rect())
        self.textObj = self.textSurface

        self.stops = stops 

    def addConnections(self, connectionA: Vertex, connectionB: Vertex):
        self.connections.extend([connectionA, connectionB])
        self.connections = list(set(self.connections))
        self.drawableLines.append((connectionA, connectionB))
        centerLocation = (
            (connectionA.centerLocation[0] + connectionB.centerLocation[0]) / 2,
            (connectionA.centerLocation[1] + connectionB.centerLocation[1]) / 2,
        )
        self.textCenterLocations.append(
            (
                centerLocation[0] - self.textObj.get_width() / 2,
                centerLocation[1] - self.textObj.get_height() / 2,
            )
        )

    def draw(self):
        for line in self.drawableLines:
            pygame.draw.line(
                self.screen,
                self.lineColour,
                line[0].centerLocation,
                line[1].centerLocation,
                3,
            )
        for centertextlocation in self.textCenterLocations:
            self.screen.blit(self.textObj, centertextlocation)
            

    def selfExportDetail(self):
        return {
            "connections": [connection.text for connection in self.connections],
            "drawableLines": [
                {"connectionA": connectionA.text, "connectionB": connectionB.text}
                for connectionA, connectionB in self.drawableLines
            ],
            "lineName": self.lineName,
            "lineColour": self.lineColour,
        }
    
