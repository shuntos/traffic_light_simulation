import pygame
import random
import math
import os 
from datetime import datetime
import glob
screen = pygame.display.set_mode((1412, 978)) 
pygame.init()
from itertools import cycle

class Vehicle:
    def __init__(self,direction, position):
        self.rule = { 
                    "right-left":{"stop":[770,850],"signal":3,"axis":0},
                    "right-bottom":{550,6},
                    "right-top":{"stop":[770,850], "signal":4,"axis":0},

                    "left-right":{"stop":[217,417],"signal":1, "axis":0},
                    "left-top":{"stop":[217,417],"signal":4, "axis":0},
                    "left-bottom":{"stop":[217,417],"signal":2, "axis":0},

                    "bottom-top":{"stop":[550,650],"signal":4, "axis":1},
                    "bottom-right":{"stop":[550,650], "signal":1,"axis":1},
                    "bottom-left":{},

                    "top-bottom":{"stop":[240,340],"signal":2, "axis":1},
                    "top-left":{},
                    "top-right":{}
                    }   
        self.vehicle_images = glob.glob("cars/*.png")
        self.directions = {"up-down":[910,0],"left-right":[0,500]}
                   
        self.image = pygame.image.load(random.choice(self.vehicle_images)).convert_alpha() 
        self.image = pygame.transform.scale(self.image, (50,90))

        self.speed = random.uniform(1, 4.1)

        self.alive = True
        
        self.direction = direction
        if self.direction in ["left-right","left-bottom","left-top"]:
             self.image = pygame.transform.rotate(self.image, 90)

        #if self.direction in ["top-bottom"]:
            #self.image = pygame.transform.rotate(self.image, 180)

        if self.direction in ["bottom-top","bottom-right"]:
            self.image = pygame.transform.rotate(self.image, 180)


        if self.direction in ["right-left","right-top"]:
            self.image = pygame.transform.rotate(self.image, -90)


        self.position = position
        self.origin_pos = position

    def update(self):
        if self.direction == "top-bottom":

            self.position = [self.position[0], self.position[1]+self.speed]

            if self.position[1] > display_h:
                self.reset()

        if self.direction == "bottom-top":

            self.position = [self.position[0], self.position[1]-self.speed]

            if self.position[1] <= 0:
                self.reset()

        elif self.direction == "bottom-right":
            if self.position[1] > 545:

                self.position = [self.position[0], self.position[1]-self.speed]

            else:
                if self.image.get_width() < self.image.get_height():

                    self.image = pygame.transform.rotate(self.image, 270)
                self.position = [self.position[0]+self.speed,543]

            if self.position[0] > display_w:
                self.reset()    


        elif self.direction == "left-right":
            self.position = [self.position[0]+self.speed, self.position[1]]
            if self.position[0] > display_w:
                self.reset()



        elif self.direction in ["right-left"]:
            self.position = [self.position[0]-self.speed, self.position[1]]
            if self.position[0] < 0:
                self.reset()

        elif self.direction in ["right-top"]:
            if self.position[0] > 760:

                self.position = [self.position[0]-self.speed, self.position[1]]

            else:
                if self.image.get_width() > self.image.get_height():

                    self.image = pygame.transform.rotate(self.image, 270)
                self.position = [750, self.position[1]-self.speed]

            if self.position[1] < 0:
                self.reset()             


        elif self.direction == "left-bottom":
            if self.position[0] < 610:

                self.position = [self.position[0]+self.speed, self.position[1]]

            else:
                if self.image.get_width() > self.image.get_height():

                    self.image = pygame.transform.rotate(self.image, 90)
                self.position = [610, self.position[1]+self.speed]

            if self.position[1] > display_h:
                self.reset()


        elif self.direction == "left-top":
            if self.position[0] < 700:

                self.position = [self.position[0]+self.speed, self.position[1]]

            else:
                if self.image.get_width() > self.image.get_height():

                    self.image = pygame.transform.rotate(self.image, 270)
                self.position = [750, self.position[1]-self.speed]

            if self.position[1] < 0:
                self.reset()             



    def reset(self):
        self.image = pygame.image.load(random.choice(self.vehicle_images)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (50,90))

        self.position = self.origin_pos
        if self.direction == "left-right":
            self.image = pygame.transform.rotate(self.image, 90)
        
        if self.direction == "left-bottom":
            self.image = pygame.transform.rotate(self.image, 90)

        if self.direction == "left-top":
            self.image = pygame.transform.rotate(self.image, 270)


        if self.direction in ["bottom-top","bottom-right"]:
            self.image = pygame.transform.rotate(self.image, 180)


        if self.direction in ["right-left","right-top"]:
            self.image = pygame.transform.rotate(self.image, -90)


class TrafficLight:
        def __init__(self,direction, position):

            self.position = position
            self.status = "red"

            if direction == "vertical":
                self.green_image  = pygame.image.load("images/green.png").convert_alpha()
                self.red_image    = pygame.image.load("images/red.png").convert_alpha()
                self.yellow_image = pygame.image.load("images/yellow.png").convert_alpha()

            else:
                self.green_image  = pygame.image.load("images/green_vertical.png").convert_alpha()
                self.yellow_image = pygame.image.load("images/yellow_vertical.png").convert_alpha()
                self.red_image    = pygame.image.load("images/red_vertical.png").convert_alpha()
            
            self.image = self.red_image

        def update_light(self, status):

            if status == "green":
                self.image = self.green_image
                self.status = "green"
    
            elif status == "yellow" :
                self.image = self.yellow_image
                self.status = "yellow"


            elif status == "red":
                self.image = self.red_image
                self.status = "red"


class PedestrainLight:
        def __init__(self, position):

            self.position = position
            self.pedestrian_time = 10
            self.cycle_duration = 25
            self.start = datetime.now()
            self.status = "red"

            self.green_image  = pygame.image.load("images/ped_green.png").convert_alpha()
            self.red_image    = pygame.image.load("images/ped_red.png").convert_alpha()
            self.image = self.red_image

        def update(self,signal):

            if signal == "green":
                self.status = "green"
                self.image = self.green_image       

            else:
                self.image = self.red_image
                self.status  = "red"

class Pedestrain:
        def __init__(self, position):
            self.pedestrian_images = glob.glob("pedestrians/*.png")
            self.org_pos = position
            self.position = position
            self.image  = pygame.transform.scale((pygame.image.load(random.choice(self.pedestrian_images)).convert_alpha() ), (80,70))


        def update(self,step):
            if step:# Moving up
                self.position = [self.position[0],self.position[1]+1]
                if self.position[1] > self.org_pos[1] + 300:
                    self.reset()
            else:# Moving down
                self.position = [self.position[0],self.position[1]-1]
                if self.position[1] < self.org_pos[1] - 300:
                    self.reset()


        def reset(self):
            self.image  = pygame.transform.scale((pygame.image.load(random.choice(self.pedestrian_images)).convert_alpha() ), (80,70))
            self.position = self.org_pos


def test_collision(index, objects):
    current_direction = objects[0].direction

    if current_direction in ["bottom-top","top-bottom"]:
        axis = 1
    else:
        axis = 0

    distances = []
    current_position = objects[index].position[axis]

    if index == 0 :
        
        return False

    for i in range(len(objects)):

        if index != i:

            distances= abs(current_position-objects[i].position[axis] )

            if distances < 95 :
                return True

    return False


# Object variables
display_h = 978
display_w = 1412

background = pygame.display.set_mode((display_w,display_h))
pygame.display.set_caption('Traffic Simulation')
clock = pygame.time.Clock()
imgroad = pygame.image.load('images/road.png').convert_alpha()


def quitsimulation():
    pygame.quit()


def gameloop():
    ped_signal =  PedestrainLight([417, 310])  # [Right, Bottom, Left, Top]
    signal_1 = TrafficLight("horizontal",[770,495]) #Right side
    signal_2 = TrafficLight("vertical",[600,550]) #Bottom side
    signal_3 = TrafficLight("horizontal",[540,390]) #Left side
    signal_4 = TrafficLight("vertical",[710,340]) #Top side
    signals = [signal_1, signal_2, signal_3, signal_4]


    vehicle_12 = Vehicle("right-top",[display_w,395])
    vehicle_13 = Vehicle("bottom-right",[750,display_h])

    left_2_right_vehicles = [ (Vehicle("left-right",[0,490])) for i in range(2) ]

    left_2_bottom_vehicles = [Vehicle("left-bottom",[0,540])]
    left_2_top_vehicles = [Vehicle("left-top",[0,400])]

    top_2_bottom_vehicles = [ (Vehicle("top-bottom",[655,0])) for i in range(2) ]

    bottom_2_top_vehicles = [ (Vehicle("bottom-top",[705,display_h])) for i in range(2) ]

    botton_2_left_vehicles = [ (Vehicle("bottom-left",[display_w,445])) for i in range(1) ]

    right_2_left_vehicles = [ (Vehicle("right-left",[display_w,445])) for i in range(2) ]

    vehicles = [ [vehicle_12], [vehicle_13], right_2_left_vehicles,left_2_right_vehicles, left_2_bottom_vehicles, left_2_top_vehicles, bottom_2_top_vehicles, top_2_bottom_vehicles]

    pedestrians = []
    for i in range(5):
        if i%2 == 0:
            pedestrians.append(Pedestrain([(ped_signal.position[0] - 40)+i*30,600]))
        else:
            pedestrians.append(Pedestrain([(ped_signal.position[0]-40)+i*30,340]))


    global start 
    start = datetime.now()
   
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        background.blit(imgroad,(0,0))

        for ii in range(4):

            if math.ceil( (datetime.now() - start).total_seconds()) >ii*20  and  (datetime.now() - start).total_seconds() <= (ii +   1)*20 :# Glow Right traffic light= Green

                if (datetime.now() - start).total_seconds() > (ii +   1)*20 -8:

                    signals[ii].update_light("yellow")

                else:

                    signals[ii].update_light("green")

            else:

                signals[ii].update_light("red")


        if (datetime.now() - start).total_seconds() > 90:
            start = datetime.now()

        if (datetime.now() - start).total_seconds() <= 90 and (datetime.now() - start).total_seconds() >= 80 :

            ped_signal.update("green")

            for i, ped in enumerate(pedestrians): # Moving pedestrains
                background.blit(ped.image, ped.position)
                ped.update(i%2)

        else:
            ped_signal.update("red")

        background.blit(ped_signal.image, ped_signal.position)



        for vehicle_list in vehicles:

            for k, vehicle in enumerate( vehicle_list): # Case for Left to right Vehicles
                background.blit(vehicle.image, vehicle.position)


                wait_and_watch = vehicle.rule[vehicle.direction]["stop"]
                axis = vehicle.rule[vehicle.direction]["axis"]

                signal = signals[vehicle.rule[vehicle.direction]["signal"]-1]

                stop = False
                stop = test_collision(k, vehicle_list)

                if signal.status == "yellow":
                    if vehicle.position[axis] <wait_and_watch[1]and  vehicle.position[axis] >wait_and_watch[0] :
                        stop = True

                if signal.status == "red":
                    if vehicle.position[axis] <wait_and_watch[1]and  vehicle.position[axis] >wait_and_watch[0]  :
                        stop = True

                if not stop:
                    vehicle.update()


        cycle_ = [0,1,2,3]
        ped_light_flag = 5
        for iii, signal in enumerate(signals):
            background.blit(signal.image, signal.position)
            if signal.status == "yellow":
                cycle_.append(cycle_.pop(0))
                cycle_.append(cycle_.pop(0))
                ped_light_flag = cycle_[iii]
         

        pygame.display.update()
        clock.tick(60)

gameloop()
pygame.quit()
quit()
