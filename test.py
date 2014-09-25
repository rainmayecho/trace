'''
  Testing objects in a scene
  * imports are bad
'''
from light import *
from plane import *
from sphere import *
from surface import *
from tracer import *
from vector import *
import time, math, Image, ImageDraw

width = 400
height = 300

fov = 120.0
surface = Surface(70,120,200,.01,.99,.1,.1,.1)
surface2 = Surface(250,120,70,.01,.99,.05,.3,.4)
o = [Sphere(6,Vector(-10,2,-10),surface)]
#o.append(Sphere(4,Vector(-20,3,-12),surface2))
o=[]
for j in range(2):
    for i in range(5):
        o.append(Sphere(3.0,Vector(-20+10*i,10*j,-20),surface))

o.append(Plane(Vector(1,-10,0),Vector(0,1,.2),surface))
#o.append(Plane(Vector(0,0,-100),Vector(0,0,1),surface))
l = [Light(0,75,75,75),Light(1,40,100,100,Vector(3,-6,3))]
l.append(Light(2,10,0,130,Vector(-10,1,-10)))

eye = Vector(-20,-5,20)
lookAt = Vector(0,0,0)
up = Vector(0,1,0)
background = (0,0,0)

time.clock()
im = Image.new('RGB',(width,height))
testdraw = Tracer(o,l,im,background)
testdraw.set_view(eye,lookAt,up,fov)
testdraw.render(eye)
print str(time.clock()/60)+'min'
