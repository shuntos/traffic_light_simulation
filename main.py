import pygame
import random
import math
import os 
from datetime import datetime
import glob
screen = pygame.display.set_mode((800, 600)) 
pygame.init()
from itertools import cycle

class Vehicle:
    def __init__(self,direction, position):
        self.vehicle_images = glob.glob("cars/*.png")
        self.directions = {"up-down":[910,0],"left-right":[0,500]}
                   
        self.image = pygame.image.load(random.choice(self.vehicle_images)).convert_alpha() 
        self.image = pygame.transform.scale(self.image, (50,90))

        self.speed = random.uniform(0.7, 3.1)
        
        self.direction = direction
        if self.direction in ["left-right","left-bottom","left-top"]:
             self.image = pygame.transform.rotate(self.image, 90)

        if self.direction in ["top-bottom"]:
            self.image = pygame.transform.rotate(self.image, 180)

        self.position = position
        self.origin_pos = position

    def update(self):
        if self.direction == "top-bottom":

            self.position = [self.position[0], self.position[1]+self.speed]

            if self.position[1] > display_h:
                self.reset()

        elif self.direction == "left-right":
            self.position = [self.position[0]+self.speed, self.position[1]]
            if self.position[0] > display_w:
                self.reset()


        elif self.direction == "left-bottom":
            if self.position[0] < 840:

                self.position = [self.position[0]+self.speed, self.position[1]]

            else:
                if self.image.get_width() > self.image.get_height():

                    self.image = pygame.transform.rotate(self.image, 90)
                self.position = [860, self.position[1]+self.speed]

            if self.position[1] > display_h:
                self.reset()


        elif self.direction == "left-top":
            if self.position[0] < 980:

                self.position = [self.position[0]+self.speed, self.position[1]]

            else:
                if self.image.get_width() > self.image.get_height():

                    self.image = pygame.transform.rotate(self.image, 270)
                self.position = [1020, self.position[1]-self.speed]

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



# Object variables
display_h = 1080
display_w = 1920

background = pygame.display.set_mode((display_w,display_h))
pygame.display.set_caption('Traffic Simulation')
clock = pygame.time.Clock()
imgroad = pygame.image.load('images/road.png').convert_alpha()


def quitsimulation():
    pygame.quit()


def gameloop():

    vehicle_1 = Vehicle("left-right",[0,460])
    vehicle_2 = Vehicle("left-right",[0,540])

    vehicle_3 = Vehicle("left-bottom",[0,590])

    vehicle_4 = Vehicle("left-top",[0,420])

    vehicle_5 = Vehicle("top-bottom",[890,0])
    vehicle_6 = Vehicle("top-bottom",[920,0])


    left_2_right_vehicles = [vehicle_1,vehicle_2]
    left_2_bottom_vehicles = [vehicle_3]
    left_2_top_vehicles = [vehicle_4]

    top_2_bottom_vehicles = [vehicle_5, vehicle_6]


    pedestrians = []
    for i in range(5):
        if i%2 == 0:
            pedestrians.append(Pedestrain([600+i*30,700]))
        else:
            pedestrians.append(Pedestrain([620+i*30,390]))




    signal_1 = TrafficLight("horizontal",[1030,550]) #Right side
    signal_2 = TrafficLight("vertical",[840,620]) #Bottom side
    signal_3 = TrafficLight("horizontal",[780,410]) #Left side
    signal_4 = TrafficLight("vertical",[980,340]) #Top side

    signals = [signal_1, signal_2, signal_3, signal_4]


    ped_signal =  PedestrainLight([650, 340])  # [Right, Bottom, Left, Top]


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



        for vehicle in left_2_right_vehicles: # Case for Left to right Vehicles
            background.blit(vehicle.image, vehicle.position)

            stop = False


            if signal_1.status == "yellow":
                if vehicle.position[0]>(ped_signal.position[0]- 200) and  vehicle.position[0]<ped_signal.position[0]  :
                    stop = True

                if vehicle.position[0]>ped_signal.position[0]:
                    stop = False


            if signal_1.status == "red":
                if vehicle.position[0]>(ped_signal.position[0]- 200) and  vehicle.position[0]<ped_signal.position[0]  :
                    stop = True

            if not stop:
                vehicle.update()


        for vehicle in left_2_bottom_vehicles:
            background.blit(vehicle.image, vehicle.position)
            stop = False

            if signal_2.status == "yellow":
                if vehicle.position[0]>(ped_signal.position[0]- 200) and  vehicle.position[0]<ped_signal.position[0]  :
                    stop = True


            if signal_2.status == "red":
                if vehicle.position[0]>(ped_signal.position[0]- 200) and  vehicle.position[0]<ped_signal.position[0]  :
                    stop = True


            if not stop:
                vehicle.update()




        for vehicle in left_2_top_vehicles:
            background.blit(vehicle.image, vehicle.position)
            stop = False

            if signal_4.status == "yellow":
                if vehicle.position[0]>(ped_signal.position[0]- 200) and  vehicle.position[0]<ped_signal.position[0]  :
                    stop = True


            if signal_4.status == "red":
                if vehicle.position[0]>(ped_signal.position[0]- 200) and  vehicle.position[0]<ped_signal.position[0]  :
                    stop = True


            if not stop:
                vehicle.update()


        for vehicle in top_2_bottom_vehicles:
            background.blit(vehicle.image, vehicle.position)
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
