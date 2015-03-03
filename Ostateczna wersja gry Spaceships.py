# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    global missile_group
    
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.acceleration = 4.5
        self.friction = 0.017

        
        self.shift =  self.image_center[0] +self.image_size[0]
        self.Icenter = self.image_center
        
    def draw(self,canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        if self.thrust == False:
            center = list(self.image_center)

        else:
            center = list(self.image_center)
            center[0] = self.shift
        
        canvas.draw_image(self.image,center, self.image_size,
                          self.pos, self.image_size, self.angle)
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius

    def update(self):

        if self.thrust ==True:
            angleVector = angle_to_vector(self.angle)
            self.vel = [angleVector[0]*self.acceleration, angleVector[1]*self.acceleration] 
 
        self.angle += self.angle_vel
        
        self.vel[0]*=(1-self.friction)
        self.vel[1]*=(1-self.friction)            
            
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]  
        

              
        
        self.pos[0]%=WIDTH
        self.pos[1]%=HEIGHT
        
        if self.vel[0] >0:
            self.vel[0]-=self.friction
        
        
    def thrustOn(self, IsOn):
        
        if IsOn:
            self.thrust = True  
            ship_thrust_sound.play()
        else:
            self.thrust = False
            ship_thrust_sound.pause()
            ship_thrust_sound.rewind()
    
    
    def velChange(self, procedure):
        
       
        if procedure[0] =="angle":
            self.angle_vel+=procedure[1]
        elif procedure[0] =="zeroAngle":
            self.angle_vel = 0
        elif procedure[0] =="thrustOn":
            self.thrustOn(True)
        elif procedure[0] =="thrustOff":
            self.thrustOn(False)
        elif procedure[0] =="shoot":
            self.shoot()
        
            
    def shoot(self):
        global missile_group

        
        angleVector = angle_to_vector(self.angle)
        
        missileVel = [angleVector[0]*self.acceleration, angleVector[1]*self.acceleration] 
        missileVel =[missileVel[0]*1.5, missileVel[1]*1.5] 
        
        missile_start = list(self.pos)
        missile_start[0] += angleVector[0]*self.radius
        missile_start[1] += angleVector[1]*self.radius
        
        #pos, vel, ang, ang_vel, image, info, sound
        missile_group.add(Sprite(missile_start, missileVel, 0, 0, missile_image, missile_info, missile_sound))
        
        pass
        
    
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        
        canvas.draw_image(self.image,self.image_center, self.image_size,
                   self.pos, self.image_size, self.angle)
    
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]  
        
        self.pos[0]%=WIDTH
        self.pos[1]%=HEIGHT
        
        self.angle +=self.angle_vel
        
        self.age+=0.9
        if self.age  > self.lifespan:
            return True
        else:
            return False
        
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius        
        
    def collide(self, other_object):
        distance = dist(self.get_position(), other_object.get_position()) 
        if distance < (self.get_radius() + other_object.get_radius()):
            return True
        else:
            return False

    
def process_sprite_group(sprite_group, canvas):
    for sprite in set(sprite_group):
        if sprite.update():
            sprite_group.remove(sprite)
            continue
        sprite.draw(canvas)    


def group_collide(sprite_group, other_object):
    
    isCollide = False
    for e in set(sprite_group):
        if e.collide(other_object):
            sprite_group.remove(e)
            isCollide  = True
    return isCollide
        
def group_group_collide(group1, group2):
    isCollide = False
    for e in set(group1):
        if group_collide(group2, e):
            group1.remove(e)
            isCollide  = True
    return isCollide        
    

# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True

    
def draw(canvas):
    global time, rock_group
    global score, lives, started 
    
    #reset game if player die
    if lives<=0:
        started = False
        rock_group = set([])
        score = 0
        lives = 3
        soundtrack.rewind()
        soundtrack.play()
        
        
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])

    # draw ship and sprites
    my_ship.draw(canvas)
    
    if group_collide(rock_group, my_ship):
        lives-=1
        
    if group_group_collide(missile_group,rock_group):
        score+=1
        
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    my_ship.update()
    
    
    #draw score and lives on the canvas
    canvas.draw_text("lives: "+str(lives), (WIDTH *0.1, 50), 25, "Red")
    canvas.draw_text("score: "+str(score), (WIDTH *0.8, 50), 25, "Red")

    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
    
    
    
def keydown(key):
    
    inputs = {"left": ["angle", -0.1], "right": ["angle", 0.1],
              "up": ["thrustOn", 0.1],"space": ["shoot", 0]}
    
    
    global current_key    
    for i in inputs:
        if key==simplegui.KEY_MAP[i]:
            my_ship.velChange(inputs[i])
     
def keyup(key):
    inputs = {"left": ["zeroAngle",0], "right": ["zeroAngle",0],
              "up": ["thrustOff", 0.1]}
    
    
  
    for i in inputs:
        if key==simplegui.KEY_MAP[i]:
            my_ship.velChange(inputs[i])    
    
            
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group


    
    #pos, vel, ang, ang_vel, image, info, sound = None)
    vel=[0,0]
    pos = [1,1]
    vel[0] = random.randrange(-20, 20, 1)
    vel[1] = random.randrange(-20, 20, 1)
    pos[0] = random.randrange(1,5,1)
    pos[1] = random.randrange(1,5,1)

    pos[0] = WIDTH / pos[0]
    pos[1] = HEIGHT  /pos[1]
    
    ang = random.randrange(-20, 20, 1)
    ang_vel = random.randrange(-15, 15, 1)
       
    
    #normalize velocity
    vel[0] /=10
    vel[1] /=10
    ang /=10
    ang_vel /= 100 
    

    if len(rock_group) < 12 and started == True:
        if dist(pos, my_ship.get_position()) > my_ship.get_radius()*2:
            rock_group.add(Sprite(pos, vel, ang, ang_vel, asteroid_image, asteroid_info))
    
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

rock_group = set([])
missile_group = set([])
#rock_group.add(Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info))
#missile_group = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)



# register handlers
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

frame.set_draw_handler(draw)

timer = simplegui.create_timer(1900.0, rock_spawner)

# get things rolling
soundtrack.play()
timer.start()
frame.start()
