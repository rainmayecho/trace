import math,Image,ImageDraw,time

class Vector():
    def __init__(self,i,j,k):
        self.x = float(i)
        self.y = float(j)
        self.z = float(k)
        self.mag = (self.dot(self))**.5
    def add(self,other):
        return Vector(self.x+other.x,self.y+other.y,self.z+other.z)

    def dot(self,other):
        return self.x*other.x+self.y*other.y+self.z*other.z

    def cross(self,other):
        return Vector((self.y*other.z-other.y*self.z),\
                      -(self.x*other.z-other.x*self.z),\
                      (self.x*other.y-other.x*self.y))
    def cross(a,b):
        return Vector((a.y*b.z-b.y*a.z),\
                      -(a.x*b.z-b.x*a.z),\
                      (a.x*b.y-b.x*a.y))

    def scale(self,s):
        self.x*=s
        self.y*=s
        self.z*=s
    def normalize(self):
        self.scale(1/self.mag)
    def __str__(self):
        return str(self.x)+'i  '+str(self.y)+'j  '+str(self.z)+'k  '

class Point():

    def __init__(self,i,j,k):
        self.x = float(i)
        self.y = float(j)
        self.z = float(k)

    def __str__(self):
        return str(self.x)+'i  '+str(self.y)+'j  '+str(self.z)+'k  '

class Ray():

    def __init__(self,p,v):
        self.anchor = p
        self.direct = v
        self.direct.normalize()
        self.t = 10.0**99
        self.object = None

    def trace(self,objects):
        for e in objects:
            if e.intersect(self):
                return True
    def shade(self,lights, objects, bgcolor):
        return self.object.shade(self,lights,objects, bgcolor)

class Sphere():

    def __init__(self,r,c,s=None):
        self.radius = r
        self.center = c
        self.surface = s
        self.rsqr = r*r
        
    def intersect(self,ray):
        dx = self.center.x-ray.anchor.x
        dy = self.center.y-ray.anchor.y
        dz = self.center.z-ray.anchor.z
        ca = Vector(dx,dy,dz)
        v = ca.dot(ray.direct)
        if v-self.radius > ray.t:
            return False
        t = self.rsqr + v*v -dx*dx-dy*dy-dz*dz
        if t < 0:
            return False
        t = v-t**.5
        if t > ray.t or t < 0:
            return False
        ray.t = t
        ray.object = self
        return True
    
    def shade(self,ray,lights,objects,bgcolor):
        px = ray.anchor.x + ray.t*ray.direct.x
        py = ray.anchor.y + ray.t*ray.direct.y
        pz = ray.anchor.z + ray.t*ray.direct.z

        p = Vector(px,py,pz)
        v = Vector(-ray.direct.x,-ray.direct.y,-ray.direct.z)
        n = Vector(px-self.center.x,py-self.center.y,pz-self.center.z)
        n.normalize()

        return self.surface.shade(p,v,n,lights,objects,bgcolor)

class Plane():

    def __init__(self,c,n,s=None):
        self.center = c
        self.kplane = c.dot(n)
        self.normal = n
        self.normal.normalize()
        self.n1 = n
        self.surface = s

    def intersect(self,ray):
        a = Vector(self.n1.x-ray.anchor.x,self.n1.y-ray.anchor.y,self.n1.z-ray.anchor.z)
        t = (self.kplane-self.normal.dot(a))/ray.direct.dot(self.normal)
        if t > ray.t:
            return False
        if t > 0:
            ray.t = t
            ray.object = self
            return True
        return False

    def shade(self,ray,lights,objects,bgcolor):
        px = ray.anchor.x +ray.t*ray.direct.x
        py = ray.anchor.y +ray.t*ray.direct.y
        pz = ray.anchor.z +ray.t*ray.direct.z

        p = Vector(px,py,pz)
        v = Vector(-ray.direct.x,-ray.direct.y,-ray.direct.z)

        return self.surface.shade(p,v,self.normal,lights,objects,bgcolor)
        

class Surface():

    def __init__(self,r,g,b,a,s,d,p,ref):
        self.red = r
        self.green = g
        self.blue = b
        self.ka = a
        self.ks = s
        self.kd = d
        self.kp = p
        self.kr = ref
        
    def shade(self,p,v,n,lights,objects,bgcolor):
        r = 0
        g = 0
        b = 0
        for light in lights:
            if light.ltype == Light.AMBIENT:
                r+=int(self.ka*self.red*light.red)
                g+=int(self.ka*self.green*light.green)
                b+=int(self.ka*self.blue*light.blue)
            else:
                l = None
                if(light.ltype == Light.POINT):
                    l = Vector(light.v.x-p.x,light.v.y-p.y,light.v.z-p.z)
                    l.normalize()
                else:
                    l = Vector(-light.v.x,-light.v.y,-light.v.z)
                shadowpoint = Point(p.x+.001*l.x,p.y+.001*l.y,p.z+.001*l.z)
                shadowray = Ray(shadowpoint,l)
                if(shadowray.trace(objects)):
                    continue
                cos = n.dot(l)
                if cos > 0:
                    diffuse = self.kd*cos
                    r+=int(diffuse*light.red)
                    g+=int(diffuse*light.green)
                    b+=int(diffuse*light.blue)
                if self.ks > 0:
                    cos*=2
                    u = Vector(cos*n.x-l.x,cos*n.y-l.y,cos*n.z-l.z)
                    specular = v.dot(u)
                    if specular > 0:
                        specular = self.ks*abs(specular)**1.6
                        r+=int(specular*light.red)
                        g+=int(specular*light.green)
                        b+=int(specular*light.blue)
        if self.kr > 0:
            t = v.dot(n)
            if t > 0:
                t*=2
                reflect = Vector(t*n.x-v.x,t*n.y-v.y,t*n.z-v.z)
                shadowpos = Vector(p.x+1*reflect.x,p.y+1*reflect.y,p.z+1*reflect.z)
                refray = Ray(shadowpos,reflect)
                if refray.trace(objects):
                    refColor = refray.shade(lights,objects,bgcolor)
                    r+=int(self.kr*refColor[0])
                    g+=int(self.kr*refColor[1])
                    b+=int(self.kr*refColor[2])
                else:
                    r+=int(self.kr*bgcolor[0])
                    g+=int(self.kr*bgcolor[1])
                    b+=int(self.kr*bgcolor[2])
                            
                    
        return (r,g,b)
    
class Light():

    AMBIENT = 0
    DIRECTIONAL = 1
    POINT = 2

    def __init__(self,l,r,g,b,vector = None):
        self.ltype = l
        self.red = r
        self.green = g
        self.blue = b
        if not self.ltype == self.AMBIENT:
            self.v = vector
            if self.ltype == self.DIRECTIONAL:
                self.v.normalize()
                
class Tracer():

    def __init__(self,o,l,scr,background):
        self.objects = o
        self.lights = l
        self.im = scr
        self.width = scr.size[0]
        self.height = scr.size[1]
        self.bg = background
        self.draw = ImageDraw.Draw(self.im)

    def set_view(self,eye,lookAt,up,fov):
        look = Vector(lookAt.x-eye.x,lookAt.y-eye.y,lookAt.z-eye.z)
        field = (self.width/(2*(math.tan(.5*fov*math.pi/180))))
        self.du = Vector.cross(look,up)
        self.du.normalize()
        self.dv = Vector.cross(look,self.du)
        self.dv.normalize()
        look.normalize()
        self.vp = look
        self.vp.x = self.vp.x*field-.5*(self.width*self.du.x+self.height*self.du.x)
        self.vp.y = self.vp.y*field-.5*(self.width*self.du.y+self.height*self.dv.y)
        self.vp.z = self.vp.z*field-.5*(self.width*self.du.z+self.height*self.du.z)

    def render(self):
        for i in range(width):
            for j in range(height):
                d = Vector(i*self.du.x+j*self.dv.x+self.vp.x,\
                   i*self.du.y+j*self.dv.y+self.vp.y,\
                   i*self.du.z+j*self.dv.z+self.vp.z)
                ray = Ray(eye,d)
                if(ray.trace(self.objects)):
                    color = ray.shade(self.lights,self.objects,self.bg)
                else:
                    color = self.bg
                self.draw.line([i,j,i,j],color)

            percent = (float(i)/width)*100
            if percent % 20 == 0 and percent > 0:
                print str(percent)+' % Complete.'
        del self.draw
        self.im.save('test3.png','PNG')

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
testdraw.render()
print str(time.clock()/60)+'min'
                
