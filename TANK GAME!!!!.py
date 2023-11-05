# animation2.py

# multiple-shot cannonball animation

from math import sqrt, sin, cos, radians, degrees
from graphics import *
from projectile import Projectile
import random
import time


class Launcher(Rectangle):# super is Rectangle so the updateshot method in Projectile app can have points to use to detect if tank is hit


    def __init__(self, win, point, color, rad,):# I changed the inputs so that I could have the 2 tanks be different colours, and have different angles
        """Create inital launcher with angle 45 degrees and velocity 40
        win is the GraphWin to draw the launcher in.
        """
        self.tank_list = []
        # draws the tank

        #super is initialised
        super().__init__(Point(point.getX()-10,point.getY()-12),Point(point.getX()+10,point.getY()-1)) 
        
        for i in range(6):#draws the wheels
            cir = Circle(Point(point.getX()-8+(3*i),point.getY()-12),1.5)
            cir.setFill('black')
            cir.setOutline('black')
            cir.draw(win)
            self.tank_list.append(cir)
            
        #draws the body of the tank
        base = Rectangle(Point(point.getX()-10,point.getY()-12),Point(point.getX()+10,point.getY()-4))
        base.setFill(color)
        base.setOutline('black')
        base.draw(win)
        self.tank_list.append(base)

        #Draws tank turret
        p1 = Point(point.getX()-8,point.getY()-4)
        p2 = Point(point.getX()-6,point.getY()+2)
        p3 = Point(point.getX()+6,point.getY()+2)
        p4 = Point(point.getX()+8,point.getY()-4)
        
        top = Polygon(p1,p2,p3,p4)
        top.setFill('grey')
        top.setOutline('black')
        top.draw(win)
        self.tank_list.append(top)

        # save the window and create initial angle and velocity
        self.win = win
        self.angle = radians(rad)
        self.vel = 40

        #makes input values into saved variables in class
        self.point = point
        self.color = color

        # create inital "dummy" arrow
        self.arrow = Line(point, point).draw(win)
        self.tank_list.append(self.arrow)

        #added cannon to make the tank have a cannon
        self.cannon = Line(point, point).draw(win)
        self.tank_list.append(self.cannon)
        
        # replace it with the correct arrow
        self.redraw()

        
    def redraw(self):#Only change here is that tank is redrawn whenever an input by the user is done so that the tank is being drawn over the arrow
        """undraw the arrow and draw a new one for the
        current values of angle and velocity.
        """
        
        self.arrow.undraw()
        self.cannon.undraw()
        for i in range(8):
            self.tank_list[i].undraw()
        
        pt2 = Point(self.vel*cos(self.angle) + self.point.getX(), self.vel*sin(self.angle) + self.point.getY())
        ptc = Point(15*cos(self.angle) + self.point.getX(), 15*sin(self.angle) + self.point.getY())
        
        self.arrow = Line(self.point, pt2).draw(self.win)
        self.arrow.setArrow("last")
        self.arrow.setWidth(1)

        self.cannon = Line(self.point, ptc)
        self.cannon.setWidth(4)
        self.cannon.setFill('black')
        self.cannon.setOutline('black')
        self.cannon.draw(self.win)
        for i in range(8):
            self.tank_list[i].draw(self.win)
        
    def adjAngle(self, amt):
        """ change angle by amt degrees """
        
        self.angle = self.angle+radians(amt)
        self.redraw()

        
    def adjVel(self, amt):
        """ change velocity by amt"""
        
        self.vel = self.vel + amt
        self.redraw()

    def undraw(self):
        for i in range(8):
            self.tank_list[i].undraw()
        self.arrow.undraw()
        self.cannon.undraw()

    def fire(self):
        return ShotTracker(self.win, degrees(self.angle), self.vel, self.point.getY(), self.point.getX(), self.color)
  

class ShotTracker(Rectangle): #Stayed mostly the same except for added inputs to allow the shottracker to start from 2 different points on the gui, and have different coloured shots
    

    """ Graphical depiction of a projectile flight using a Circle """

    def __init__(self, win, angle, velocity, height, xpos, color):
        """win is the GraphWin to display the shot, angle, velocity, and
        height are initial projectile parameters.
        """
        self.proj = Projectile(angle, velocity, height, xpos)
        self.marker = Circle(Point(xpos,height), 3)
        self.marker.setFill(color)
        self.marker.setOutline(color)
        self.marker.draw(win)
        super().__init__(Point(xpos-2.4,height-2.4),Point(xpos+2.4,height+2.4))

        
    def update(self, dt):
        """ Move the shot dt seconds farther along its flight """
        
        self.proj.update(dt)
        center = self.marker.getCenter()
        dx = self.proj.getX() - center.getX()
        dy = self.proj.getY() - center.getY()
        self.marker.move(dx,dy)
        super().move(dx,dy)
        
    def getX(self):
        """ return the current x coordinate of the shot's center """
        return self.proj.getX()

    def getY(self):
        """ return the current y coordinate of the shot's center """
        return self.proj.getY()

    def undraw(self):
        """ undraw the shot """
        self.marker.undraw()


class ProjectileApp:

    def __init__(self):
        self.win = GraphWin("Projectile Animation", 1000, 750)
        self.win.setCoords(-10, -30, 510, 390)

        #Draws the labels under the land
        Text(Point(20,-15), 'Angle:').draw(self.win)
        Text(Point(100,-15), 'Power:').draw(self.win)
        Text(Point(360, -15), 'Red:').draw(self.win)
        Text(Point(410, -15), 'Blue:').draw(self.win)
        f = Text(Point(480, -15), 'Press h for help')
        f.setSize(8)
        f.draw(self.win)

        #Initialising score system
        self.red_point = 0
        self.blue_point = 0
        self.red_text = Text(Point(380, -15), "0").draw(self.win)
        self.blue_text = Text(Point(430, -15), "0").draw(self.win)

        #Initialising various used variables/lists
        self.shot = 0 #will be the shot travelling across the screen
        self.land = [] #will be every point that makes up the randomly generated land
        self.hit = 0 #Used between updateshot and run to detect if shot hit opposing tank
        self.drawland = 0#will be the green land generated in the gui
        
        self.restart(0)

    def restart(self, p):#Initialises the rest of the variables/remakes parts of the gui when someone gains a point
        if p == 1:# Undraws parts of the gui that will be redrawn
            self.launcher1.undraw()
            self.launcher2.undraw()
            self.angle_txt.undraw()
            self.power_txt.undraw()
            self.turn.undraw()
            self.drawland.undraw()
            self.sky.undraw()
            self.land = []
            self.sun.undraw()

        #Sky and sun creation
        self.sky = Rectangle(Point(-10,0),Point(510,390))
        self.sky.setFill('light blue')
        self.sky.draw(self.win)
        self.sun = Circle(Point(480,360),18)
        self.sun.setFill('yellow')
        self.sun.setOutline('yellow')
        self.sun.draw(self.win)
        
        #Drawn number for power and angle 
        self.angle_txt = Text(Point(40,-15), '45').draw(self.win )
        self.power_txt = Text(Point(120,-15), '40').draw(self.win)

        #initialising/restarting starting angle and power for both tanks
        self.angle1 = 45
        self.angle2 = 45
        self.power1 = 40
        self.power2 = 40

        #Text to show gamestate
        self.turn = Text(Point(255, -15), "Player 1's turn")
        self.turn.setSize(20)
        self.turn.draw(self.win)

        #Position for both tanks, y position is randomly generated and land() function adapts to it)
        self.pos1 = Point(10,random.randrange(13,300))
        self.pos2 = Point(490,random.randrange(13,300))

        #Call on Launcher class to create the tanks
        self.launcher1 = Launcher(self.win, self.pos1, "red", 45)
        self.launcher2 = Launcher(self.win, self.pos2, "blue", 135)
        print(str(self.launcher1))
        print(self.launcher2)
        
        self.lands()

        
    def updateShots(self, dt, ln):#detects if shot hits something, land or the other tank
        self.shot.update(dt)
        if (
            (self.shot.getP2().getX() >= ln.getP1().getX() and self.shot.getP2().getY() >= ln.getP1().getY())
            and (self.shot.getP1().getX() <= ln.getP2().getX() and self.shot.getP1().getY() <= ln.getP2().getY())
            ): #statement to tell if shot hit the other tank      
            self.hit = 1
            return True
        
        else:
            for i in range(len(self.land)-2):#loop that tests every space between every point on the land list to see if projectile is between the 2 points
                if (
                    (self.shot.getP1().getX() >= self.land[i+1].getX()
                     and self.shot.getP1().getX() <= self.land[i+2].getX())
                    ):
                    if (
                     (self.shot.getP1().getY() <= self.land[i+1].getY()
                     or self.shot.getP1().getY() <= self.land[i+2].getY())
                     ):
                        return True
        
    def run(self):
        player = 1
        
        # main event/animation loop
        while not player == 0:

            #outputs the saved angle and power values for tank 1 to the gui 
            self.angle_txt.setText(self.angle1)
            self.power_txt.setText(self.power1)
            while player == 1:
                
                key = self.win.checkKey()# checks for inputs by used
                
                if key in ["q", "Q"]:
                    player = 0 #makes player = 0 so main loop ends and the programme exits

                elif key == 'h':
                    self.help()# calls upon help method

                if key == "Left": # adjust the angle of the cannon, arrow, and bottom left angle value
                    self.launcher1.adjAngle(1)
                    self.angle1 = self.angle1 + 1
                    self.angle_txt.setText(self.angle1)
                    
                elif key == "Right":# adjust the angle of the cannon, arrow, and bottom left angle value
                    self.launcher1.adjAngle(-1)
                    self.angle1 = self.angle1 - 1
                    self.angle_txt.setText(self.angle1)
                    
                elif key == "Up":# adjust the power, arrow, and bottom left angle value
                    self.launcher1.adjVel(1)
                    self.power1 = self.power1 + 1
                    self.power_txt.setText(self.power1)
                    
                elif key == "Down":# adjust the power, arrow, and bottom left angle value
                    self.launcher1.adjVel(-1)
                    self.power1 = self.power1 - 1
                    self.power_txt.setText(self.power1)
                    
                elif key == "space":# Fires the projectile
                    
                    self.shot = self.launcher1.fire()# calls upon launcher fire method, which calls upon ShotTracker, which makes the projectile drawn and fly the air

                    while self.shot.getP1().getX() >= -10 and self.shot.getP2().getX() <= 510:#shot stops moving when it hits left or right corners of gui

                        if self.updateShots(1/30,self.launcher2):# calls upon updateShots method to tell if shot hit the other tank or the land
                            break
                        
                        update(60)#Moves projectile
                        # I legit have no idea which method this is because it could be like 3

                    if self.hit == 1:# if shot hit the other tank
                        
                        self.hit = 0 #resets variable
                        
                        self.red_point = self.red_point + 1 #increases score in gui
                        self.red_text.setText(self.red_point)
                        
                        self.turn.setText('HIT!!!!!!')#updates gamestate to tell user that projectile hit
                        time.sleep(2)#lets user read prompt
                        self.shot.undraw()#undraws shot
                        self.restart(1)#redraws the map
                        player = 1# player one first to shoot
                    else:
                        self.turn.setText('miss :(')#updates gamestate text in gui
                        time.sleep(2)
                        self.turn.setText("Player 2's turn")
                        self.shot.undraw()
                        player = 2 #player 2's turn
                        
            self.angle_txt.setText(self.angle2)
            self.power_txt.setText(self.power2)
            while player == 2: # player 2 is basically the same code except with minor changes to flip the controls and corresponding values 
                
                key = self.win.checkKey()
                if key in ["q", "Q"]:
                    player = 0
                elif key == 'h':
                    self.help()


                if key == "Left":
                    self.launcher2.adjAngle(1)
                    self.angle2 = self.angle2 - 1
                    self.angle_txt.setText(self.angle2)
                    
                elif key == "Right":
                    self.launcher2.adjAngle(-1)
                    self.angle2 = self.angle2 + 1
                    self.angle_txt.setText(self.angle2)
                    
                elif key == "Up":
                    self.launcher2.adjVel(1)
                    self.power2 = self.power2 + 1
                    self.power_txt.setText(self.power2)
                    
                elif key == "Down":
                    self.launcher2.adjVel(-1)
                    self.power2 = self.power2 - 1
                    self.power_txt.setText(self.power2)

                elif key == "space":
                    self.shot = self.launcher2.fire()
                    while self.shot.getP1().getX() >= -10 and self.shot.getP2().getX() <= 510:

                        if self.updateShots(1/30,self.launcher1):
                            break
                        update(60)

                    if self.hit == 1:
                        self.hit = 0
                        self.blue_point = self.blue_point + 1
                        self.blue_text.setText(self.blue_point)
                        self.turn.setText('HIT!!!!!!')
                        time.sleep(2)
                        self.shot.undraw()
                        self.restart(1)
                        player = 1
                    else:
                        self.turn.setText('miss :(')
                        time.sleep(2)
                        self.turn.setText("Player 1's turn")
                        self.shot.undraw()
                        player = 1 
            
        self.win.close()

    def help(self): #Draws help menu
        drawing = []

        f = Rectangle(Point(150,80),Point(350,280))
        f.setFill('grey')
        f.draw(self.win)
        drawing.append(f)
        
        drawing.append(Text(Point(250,260),'Controls').draw(self.win))
        drawing.append(Launcher(self.win, Point(325,105), 'green', 135))
        drawing.append(Launcher(self.win, Point(175,105), 'purple', 45))
        drawing.append(Text(Point(270,230),'Up/Down arrows for change in power').draw(self.win))
        drawing.append(Text(Point(270,205),'Left/Right arrows for change in angle').draw(self.win))
        drawing.append(Text(Point(270,180),'Space to FIRE AHHHHHHHHHHHHH').draw(self.win))
        drawing.append(Text(Point(250,145),'Press Q to exit the game').draw(self.win))
        drawing.append(Text(Point(250,105),'Press r to exit help screen').draw(self.win))

        arrow = Line(Point(170,220),Point(170,240)).draw(self.win)
        arrow.setArrow("last")
        arrow.setWidth(8)
        drawing.append(arrow)

        arrow = Line(Point(180,240),Point(180,220)).draw(self.win)
        arrow.setArrow("last")
        arrow.setWidth(8)
        drawing.append(arrow)

        arrow = Line(Point(175,205),Point(155,205)).draw(self.win)
        arrow.setArrow("last")
        arrow.setWidth(8)
        drawing.append(arrow)

        arrow = Line(Point(180,205),Point(200,205)).draw(self.win)
        arrow.setArrow("last")
        arrow.setWidth(8)
        drawing.append(arrow)

        cir = Circle(Point(177,180),3)
        cir.setFill('red')
        cir.draw(self.win)
        drawing.append(cir)
        
        #undraws help menu after input
        while True:
            key = self.win.getKey()
                
            if key == 'r':
                for i in drawing:
                    i.undraw()
                break
        
    def lands(self): #How the green land is generated
        
        land2 = [] #land2 is used to so that the random positions of the land can start from each tank and then move to the centre of the gui

        #first 3 points are to create lowest border of lad=nd and the the land under tank1
        self.land.append(Point(-10,0))
        self.land.append(Point(-10,self.pos1.getY()-13))
        self.land.append(Point(30,self.pos1.getY()-13))

        #used as starting y point and then move it up or depending random number t
        r = self.pos1.getY()-13
        f = self.pos2.getY()-13

        #used as starting x point then moving it 10 units after every recurrance of the next 2 loops
        x1 = 30
        x2 = 470

        for i in range(21):
            t = random.randrange(-8,18)
            if t + r > 340:# if elif statement to make sure land doesn't go out of gui
                t = -t
            elif t + r <= 0:
                t = abs(t)
            for j in range(10): #used to have a point in list land at every x integer in the gui
                self.land.append(Point(x1+(1+j),(((1+j)*t)/10)+r))
            x1 = x1 + 10
            r = t + r

        for i in range(21):#same as previous loop except starts at tank2 and moves right to left
            t = random.randrange(-8,18)
            if t + f > 340:
                t = -t
            elif t + f <= 0:
                t = abs(t)
            for j in range(10):
                land2.append(Point(x2 - (1+j),(((1+j)*t)/10)+f))
            x2 = x2 - 10
            f = t + f

        land2.reverse()# takes land2, reverses it to be added into the list self.land to have a complete list of land values that span left to right and all the of the jagged lands

        #Done to add the points between self.land and land2
        mid1 = self.land[len(self.land)-1]
        mid2 = land2[0]
        mid = mid2.getY() - mid1.getY()
        for i in range(1,21):
            self.land.append(Point(240+i,((mid*i)/20)+mid1.getY()))

        self.land = self.land + land2 
        self.land.append(Point(470,self.pos2.getY()-13))
        self.land.append(Point(510,self.pos2.getY()-13))
        self.land.append(Point(510,0))

        #self.land is finally drawn as a polygon
        self.drawland = Polygon(self.land)
        self.drawland.setFill('dark green')
        self.drawland.draw(self.win)

if __name__ == "__main__":
    ProjectileApp().run()\

