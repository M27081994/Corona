import pygame
import random
import pymunk
#import matplotlib.pyplot

pygame.init()

display = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()
space = pymunk.Space()
FPS = 90
population = 300
recovery_time = FPS*5 # 5 Sekunden

class Ball:
    def __init__(self, x, y, collision_type, infection_status):
        self.x = x
        self.y = y
        self.body = pymunk.Body()
        self.body.position = x, y
        self.body.velocity = random.uniform(-100, 100), random.uniform(-100, 100)  #random.uniform liefert eine float zufallszahl zwischen -100 und 100. Im gegensatz zu pygame kann pymunk mit floats umgehen
        self.shape = pymunk.Circle(self.body, 10)
        self.shape.density = 1
        self.shape.collision_type = collision_type
        self.shape.elasticity = 1
        self.infected = infection_status       # wir definieren das Attribut infectec. Achtung: Das Attribut infected und die Methode infect sind etwas völlig verschiedenes. CAVE: Verwechslung
        space.add(self.body, self.shape)
        self.infected_time = 0
        self.recovered = False

    def pass_time(self):
        if self.infected:
            self.infected_time += 1
        if self.infected_time >= recovery_time:
            self.infected = False
            self.recovered = True
            self. announce_recovery()
            self.shape.collision_type = population + 2

    def announce_recovery(self):
        if self.recovered:
            print("Recovered")

    def draw(self):
        x, y = self.body.position
        if self.infected:                                               # wenn das Attribut self.infected True ist, dann male den Circle rot
            pygame.draw.circle(display, (255, 0, 0), (int(x), int(y)), 10)      # circle(surface, color, center, radius
        elif self.recovered:
            pygame.draw.circle(display, (0, 0, 255), (int(x), int(y)), 10)
        else:                                                                   # wenn das Attribut self.infected False ist, dann male den Circle weiß
            pygame.draw.circle(display, (255, 255, 255), (int(x), int(y)), 10)      # circle(surface, color, center, radius

    def infect(self, space=0, arbiter=0, data=0):   # wir definieren die Methode infect
        self.infected = True     # wird die Methode infect ausgeführt, so wird das Attribut self.infected auf True gesetzt
        self.shape.collision_type = population+1
        print("Infektion")
        return


class Wall():
    def __init__(self, p1, p2):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC) # bei Static bodies braucht man die density nicht wählen, diese wir auf unendlich gesetzt
        self.shape = pymunk.Segment(self.body, p1, p2, 5)   # wir nehmen für die wand das pymunk Objekt Segment, die position in x ist p1, die in y p2 und die Dicke ist 5
        self.shape.elasticity = 1
        space.add(self.body)      # ohne diese Code Zeile bringt er: The shape's body must be added to the space before the shape.Failed condition: shape->body->space == space
        space.add(self.shape)


infected_count = []


def game():
    balls = [Ball(random.randint(0, 800), random.randint(0, 800), 1, False) for i in range(0, 300)]  # Eine Liste, die alle unsere 300 Instanzen der Klasse Ball enthält. wir geben jedem Ball eine ganzzahlige, zufällige x und eine ganzzahlige, zufällige y Koordinate, damit sie gleichmäßig auf dem Display verteilt sind
    for i in range (1, population+1):
        balls[i-1].shape.collision_type = i
        handler = space.add_collision_handler(i, population + 1)
        handler.separate = balls[i - 1].infect

    random.choice(balls).infect()                                                          # random.choice wählt ein zufälliges Element der liste
    walls = [Wall((0, 0), (0, 800)),       # left Wall
             Wall((0, 0), (800, 0)),      # upper Wall
             Wall((800, 0), (800, 800)),      # right Wall
             Wall((0, 800), (800, 800))]        # under Wall

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        display.fill((0, 0, 0))                  # erzeugt bei jedem refresh den weißen Hintergrund
        infected_count_this_frame = 0
        [ball.draw() for ball in balls]
        [ball.pass_time() for ball in balls]
        for ball in balls:
            if ball.infected:
                infected_count_this_frame +=1
        if len(infected_count) <= 1000:
            infected_count.append(infected_count_this_frame)
        pygame.display.update()
        clock.tick(FPS)
        space.step(1/FPS)


game()
pygame.quit()
#matplotlib.plot(range(0, len(infected_count), 1), infected_count)