import pygame


class Circle:
    def __init__(
        self,
        screen: pygame.Surface,
        radius: int,
        centerLocation: tuple[int, int],
        text: str,
        colour: pygame.Color = "blue",
        textColour: pygame.Color = "white",
    ):
        self.screen = screen
        self.radius = radius
        self.colour = colour
        self.textColour = textColour
        self.centerLocation = centerLocation
        self.text = text
        self.FONT = pygame.font.Font("JetBrainsMono-Regular.ttf", 20)
        self.textObj = self.FONT.render(text, True, self.textColour, None)
        self.textCenterLocation = (
            self.centerLocation[0] - self.textObj.get_width() / 2,
            self.centerLocation[1] - self.textObj.get_height() / 2,
        )

    def draw(self):
        pygame.draw.circle(self.screen, self.colour, self.centerLocation, self.radius)
        self.screen.blit(self.textObj, self.textCenterLocation)

    def updateLocation(self, newLocation: tuple[int, int]):
        self.centerLocation = newLocation
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

    def __str__(self):
        return str({"location": self.centerLocation, "name": self.text})

    def non_str(self):
        return {"location": self.centerLocation, "name": self.text}


class Vertex(Circle):
    def __init__(
        self,
        screen: pygame.Surface,
        text: str,
        centerLocation: tuple[int, int],
    ):
        super().__init__(screen, 30, centerLocation, text)
        self.centerLocation = centerLocation
        self.text = text

    def checkIfInsideCircle(self, pos: tuple[int, int]):
        dy = pos[1] - self.centerLocation[1]
        dx = pos[0] - self.centerLocation[0]
        distance_squared = dy**2 + dx**2
        return distance_squared <= self.radius**2

    def eventChecker(self, mousePos: tuple[int, int]):
        if self.checkIfInsideCircle(mousePos):
            pygame.draw.rect(
                self.screen,
                "brown",
                (
                    self.centerLocation[0] - self.radius,
                    self.centerLocation[1] - self.radius,
                    self.radius * 2,
                    self.radius * 2,
                ),
                2,
            )

    def mouseClicked(self, mousePos: tuple[int, int]):
        if self.checkIfInsideCircle(mousePos):
            return self
        else:
            return None 

    def setBackgroundColour(self, colour: pygame.Color):
        self.colour = colour
