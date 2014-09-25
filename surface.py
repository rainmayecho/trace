from light import *
from point import *
from ray import *
from vector import *

class Surface():
    '''
    -------------------------------------------
    Defines a surface with these properties:

        (r, g, b) - Color
        a - Ambient Coefficent
        s - Specular Coefficient
        d - Diffuse Coefficient
        p - Unused Coefficient
        ref - Reflectance Coefficient

    shade computes the contribution to color
    from various light sources, shadows, and
    reflections.

    returns to the calling object
        returns to the ray intersecting that object
            returns color
    -------------------------------------------    
    '''

    def __init__(self, r, g, b, a, s, d, p, ref):
        self.red = r
        self.green = g
        self.blue = b
        self.ka = a
        self.ks = s
        self.kd = d
        self.kp = p
        self.kr = ref
        
    def shade(self, p , v , n, lights, objects, bgcolor):
        r, g, b = 0, 0, 0
        for light in lights:
            ## Ambient contributions are 'independent' of geometry.
            if light.ltype == Light.AMBIENT:
                r += int(self.ka*self.red*light.red)
                g += int(self.ka*self.green*light.green)
                b += int(self.ka*self.blue*light.blue)
            else:
                l = None
                if(light.ltype == Light.POINT):
                    l = Vector(light.v.x - p.x, light.v.y - p.y, light.v.z - p.z)
                    l.normalize()
                else:
                    l = Vector(-light.v.x, -light.v.y, -light.v.z)

                ## Slight offset for the shadow ray
                shadowpoint = Point(p.x + .001*l.x, p.y + .001*l.y, p.z + .001*l.z)
                shadowray = Ray(shadowpoint, l)

                ## Recurse on the shadow ray
                if(shadowray.trace(objects)):
                    continue

                ## Diffuse and Specular contributions.
                cos = n.dot(l)
                if cos > 0:
                    diffuse = self.kd*cos
                    r += int(diffuse*light.red)
                    g += int(diffuse*light.green)
                    b += int(diffuse*light.blue)
                if self.ks > 0:
                    cos *= 2
                    u = Vector(cos*n.x-l.x,cos*n.y-l.y,cos*n.z-l.z)
                    specular = v.dot(u)
                    if specular > 0:
                        specular = self.ks*abs(specular)**1.6
                        r += int(specular*light.red)
                        g += int(specular*light.green)
                        b += int(specular*light.blue)
        ## Reflection contributions
        if self.kr > 0:
            t = v.dot(n)
            if t > 0:
                t *= 2
                ## Reflection ray's direction vector
                reflect = Vector(t*n.x - v.x, t*n.y - v.y, t*n.z - v.z)
                ## Reflection ray's anchor point, can change the 1* to 1.001
                shadowpos = Vector(p.x + 1*reflect.x, p.y + 1*reflect.y, p.z + 1*reflect.z)
                refray = Ray(shadowpos, reflect)
                ## Recurse on reflected rays
                if refray.trace(objects):
                    refColor = refray.shade(lights,objects,bgcolor)
                    r += int(self.kr*refColor[0])
                    g += int(self.kr*refColor[1])
                    b += int(self.kr*refColor[2])
                else:
                    r += int(self.kr*bgcolor[0])
                    g += int(self.kr*bgcolor[1])
                    b += int(self.kr*bgcolor[2])
                            
                    
        return (r,g,b)
