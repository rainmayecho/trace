from point import *
from surface import *
from ray import *
from vector import *

class Plane():
    '''
    -------------------------------------------
    Geometric surfaces are functionally identical
    i.e. shade calculates the required vectors from
    the object's properties and calls surface.shade.
    -------------------------------------------    
    '''

    def __init__(self, c, n, s=None):
        self.center = c
        self.kplane = c.dot(n)
        self.normal = n
        self.normal.normalize()
        self.n1 = n
        self.surface = s

    def intersect(self,ray):
        a = Vector(self.n1.x - ray.anchor.x,\
                   self.n1.y - ray.anchor.y,\
                   self.n1.z - ray.anchor.z)
        t = (self.kplane - self.normal.dot(a))/ray.direct.dot(self.normal)
        if t > ray.t:
            return False
        if t > 0:
            ray.t = t
            ray.object = self
            return True
        return False

    def shade(self, ray, lights, objects, bgcolor):
        px = ray.anchor.x + ray.t*ray.direct.x
        py = ray.anchor.y + ray.t*ray.direct.y
        pz = ray.anchor.z + ray.t*ray.direct.z

        p = Vector(px, py, pz)
        v = Vector(-ray.direct.x, -ray.direct.y, -ray.direct.z)

        return self.surface.shade(p, v, self.normal, lights, objects, bgcolor)
