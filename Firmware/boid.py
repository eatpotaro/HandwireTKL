import math

def getMag(xpos, ypos):
    return (xpos ** 2 + ypos ** 2)**0.5

#setup ball class for display
class Ball():        
    def __init__(self, xpos, ypos, vel, angle, isWrap = True):
        self.xpos = xpos
        self.ypos = ypos
        self.vel = vel
        self.angle = angle
        self.isWrap = isWrap
        
    def updatePos(self):
        self.moveBall()
        if self.isWrap:
            self.wrapPos()
        else:
            self.clampPos()
        
    def getXYVel(self):
        #return x, then y components of velocity
        return math.cos(self.angle) * self.vel, math.sin(self.angle) * self.vel
        
    def moveBall(self):
        newVel = self.getXYVel()
        self.xpos += newVel[0]
        self.ypos += newVel[1]

    def clampPos(self):
        if(self.xpos < 0):
            self.xpos = 0
            self.angle = math.pi - self.angle 
            
        if(self.xpos > 127):
            self.xpos = 126
            self.angle = math.pi - self.angle 
            
        if(self.ypos < 0):
            self.ypos = 0
            self.angle = (2 * math.pi) - self.angle 
            
        if(self.ypos > 31):
            self.ypos = 30
            self.angle = (2 * math.pi) - self.angle 
        
    def wrapPos(self):
        if(self.xpos < 0):
            self.xpos = 127
        if(self.xpos > 127):
            self.xpos = 0
            
        if(self.ypos < 0):
            self.ypos = 31
        if(self.ypos > 31):
            self.ypos = 0
            
    def getXPosInt(self):
        return int(self.xpos)
    
    def getYPosInt(self):
        return int(self.ypos)

    def distSquared(self, ball):
        return (self.xpos - ball.xpos) ** 2 + (self.ypos - ball.ypos) ** 2

    def angleBetween(self, ball):
        btoax, btoay =  self.xpos - ball.xpos, self.ypos - ball.ypos
        
        return math.atan2(btoay, btoax)
    
    def angleTo(self, xpos, ypos):
        atobx, atoby =  xpos - self.xpos, ypos - self.ypos
        
        return math.atan2(atoby, atobx)
        

class Boid(Ball):    
    def __init__(self, xpos, ypos, vel, angle, isWrap = True):
        super().__init__(xpos, ypos, vel, angle, isWrap)
    
    #extent updatepos to update velocity as well
    def updatePos(self, boids):
        super().updatePos()
        self.updateVel(boids)
        
    def updateVel(self, boids):
        closeboids = []
        for boid in boids:
            if(boid == self):
                continue
            if(self.distSquared(boid) > 2000):
                continue
            closeboids.append(boid)
                
        
        sx, sy = self.seperation(closeboids)
        ax, ay = self.alignment(closeboids)
        cx, cy = self.cohesion(closeboids)
        
        xtotal = sx * 1.6 + ax + cx
        ytotal = sy * 1.6 + ay + cy
        
        targetangle = math.atan2(ytotal, xtotal)
        rotdir = 1
        diff = (targetangle - self.angle + math.pi) % (2 * math.pi) - math.pi
        maxrot = self.vel / 6
        if(diff < 0):
            rotdir = -1
        if(abs(diff) > maxrot):
            self.angle += maxrot * rotdir
        else:
            self.angle = targetangle
        
    def seperation(self, boids):
        #stay at least a certain distance from another boid
        #do this by finding the closest boid and returning the opposite direction
        if(len(boids) == 0):
            return [math.cos(self.angle), math.sin(self.angle)]
        
        closest = None
        dist = 999999
        for boid in boids:
            newdist = self.distSquared(boid)
            if(newdist < dist):
                dist = newdist
                closest = boid
                
        angle = self.angleBetween(closest)
        return [math.cos(angle), math.sin(angle)]

    def alignment(self, boids):
        if(len(boids) == 0):
            return [math.cos(self.angle), math.sin(self.angle)]
        
        angle = 0
        for boid in boids:
            angle += boid.angle
        angle /= len(boids)
        return [math.cos(angle), math.sin(angle)]
    
    def cohesion(self, boids):
        #try to aim towards the center of the flock of boids
        centerx, centery = 0, 0
        if(len(boids) == 0):
            return [math.cos(self.angle), math.sin(self.angle)]
        
        for boid in boids:
            centerx += boid.xpos
            centery += boid.ypos
        centerx /= len(boids)
        centery /= len(boids)
        
        angle = self.angleTo(centerx, centery)
        return [math.cos(angle), math.sin(angle)]
        
        
        
        
        
        
        
