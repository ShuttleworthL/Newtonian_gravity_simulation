import pygame
import numpy as np
import math
#importing dependecies

pygame.init()

screen_info = pygame.display.Info() #finding display's resolution
screen_center = [screen_info.current_w/2, screen_info.current_h/2] #finding center cords of screen
screen_width, screen_height = screen_info.current_w, screen_info.current_h #setting screen parameters to display's resolution
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

thrust_multiplier = 1000

#f = g*((m1*m2)/r**2)
#f = m*a

def compute_gravity(body1, body2):
    g = 10000 #gravitational constant (astronomically bigger for scaled down model)
    dx = body2.position[0] - body1.position[0] #horazontal distance
    dy = body2.position[1] - body1.position[1] #vertical distance
    distance = math.sqrt(dx**2 + dy**2) #total distance (hypotenuse)
    force = g * (body1.mass * body2.mass) / distance**2 #force(N) via newton's law of universal gravitation
    fx = force * dx / distance #magnitude of force in x axis
    fy = force * dy / distance #magnitude of force in y axis
    return np.array([fx, fy]) #force vector


class body:
    def __init__(self, position, velelocity, colour, radius, mass, control):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velelocity, dtype=float)
        self.colour = colour
        self.radius = radius
        self.mass = mass
        self.control = control
    
    def update(self, force, delta_time):
        acceleration = force / self.mass
        self.velocity += acceleration * delta_time
        self.position += self.velocity * delta_time

    def burn(self, delta_time, thrust_multiplier, is_prograde):
        if self.control == False:
            return
        magnitude = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2) #finding magnitude eg total force of vector (hypotenuse)
        direction = self.velocity / magnitude #diving velocity by magnitude so that you are only left with direction as direction * force = velocity
        if is_prograde == True:
            self.velocity += direction * thrust_multiplier * delta_time #adding thrust over time to velocity in prograde direction
        elif is_prograde == False:
            self.velocity += -(direction * thrust_multiplier) * delta_time #adding thrust over time to velocity in retrograde direction

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, self.position, self.radius)

objects = [
    body([screen_center[0], screen_center[1]], [0, 0], (255, 200, 0), 100, 1000, False),
    body([screen_center[0] + 300, screen_center[1]], [0, -200], (0, 255, 0), 15, 1, True),
]

clock = pygame.time.Clock()

running = True
while running: #while loop
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False #if quit is clicked end loop

    delta_time = clock.get_time() / 1000 #get time in seconds
    screen.fill((0,0,0))

    for bodys in objects:
        bodys.draw(screen) #drawring body to screen
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                bodys.burn(delta_time, thrust_multiplier, True)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                bodys.burn(delta_time, thrust_multiplier, False)


    for i, body1 in enumerate(objects): #finding index and iteration 
        force = np.array([0.0, 0.0]) #resetting force vector
        for j, body2 in enumerate(objects): #finding second index and iteration
            if i != j: #checking second iteration is not the first
                force += compute_gravity(body1, body2) #adding force vector
        body1.update(force, delta_time) #updating bodys location

    pygame.display.flip() #update display

    clock.tick(60) #limiting 60 fps

pygame.quit() #if loop ends close program