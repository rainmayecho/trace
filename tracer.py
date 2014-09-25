from ray import *
from tracer import *
from vector import *
import time, math, Image, ImageDraw

class Tracer():
    '''
    -------------------------------------------
    Driver class for the ray tracer.

    set_view requires the following parameters:
        self - The current tracer object.
        eye - The position of the 'eye'.
        lookAt - The vector in which an observer looks.
        up - The arbitrary vector that defines what is 'up'.
        fov - The desired field of view in degrees.

    set_view then calculates the following vectors:
        du - normalized vector, orthogonal to lookAt and up.
        dv - normalized vector, orthogonal to lookAt and du.
        vp - viewpoint vector.
        
        
    render iterates through every pixel, computing its color,
    and saves the image to png.
        For every ray:
            ray.trace tests for intersections with all objects
            in the scene. If there is an intersection, the ray
            calls ray.shade, an abstracted shading method.
    -------------------------------------------    
    '''
    def __init__(self, o, l, scr, background):
        self.objects = o
        self.lights = l
        self.im = scr
        self.width = scr.size[0]
        self.height = scr.size[1]
        self.bg = background
        self.draw = ImageDraw.Draw(self.im)

    def set_view(self, eye, lookAt, up, fov):
        ## Direction of looking
        look = Vector(lookAt.x - eye.x,\
                      lookAt.y - eye.y,\
                      lookAt.z - eye.z)
        ## Field of view calculation
        field = (self.width/(2*(math.tan(.5*fov*math.pi/180))))

        ## Orthogonal Basis
        self.du = Vector.cross(look,up)
        self.du.normalize()
        self.dv = Vector.cross(look,self.du)
        self.dv.normalize()
        look.normalize()

        ## Viewpoint
        self.vp = look
        self.vp.x = self.vp.x*field - .5*(self.width*self.du.x + \
                                         self.height*self.du.x)
        self.vp.y = self.vp.y*field - .5*(self.width*self.du.y + \
                                          self.height*self.dv.y)
        self.vp.z = self.vp.z*field - .5*(self.width*self.du.z + \
                                          self.height*self.du.z)

    def render(self, eye):
        for i in xrange(self.width):
            for j in xrange(self.height):
                ## Direction vector for the ray
                d = Vector(i*self.du.x + j*self.dv.x + self.vp.x,\
                   i*self.du.y + j*self.dv.y + self.vp.y,\
                   i*self.du.z + j*self.dv.z + self.vp.z)
                ray = Ray(eye, d)
                if(ray.trace(self.objects)):
                    color = ray.shade(self.lights, self.objects, self.bg)
                else:
                    color = self.bg
                self.draw.line([i,j,i,j], color)

            percent = (float(i)/self.width)*100
            if percent % 20 == 0 and percent > 0:
                print str(percent)+' % Complete.'
        del self.draw
        self.im.save('test.png','PNG')
