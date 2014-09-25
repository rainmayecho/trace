from surface import *
from vector import *

class Sphere():

    '''
    -------------------------------------------
    Creates a sphere with parameters:
        r - radius
        c - center
        s - surface object

    intersect calculates whether or not
    a ray intersects any part of the sphere.

    shade calculates the following vectors:
        p - the intersection point vector from the origin
        v - the direction vector of the ray
        n - the normal vector of the intersection point
    and calls self.surface.shade to compute color
    
    -------------------------------------------    
    '''

    def __init__(self, r, c, s=None):
        self.radius = r
        self.center = c
        self.surface = s
        self.rsqr = r*r
        
    def intersect(self, ray):
        dx = self.center.x - ray.anchor.x
        dy = self.center.y - ray.anchor.y
        dz = self.center.z - ray.anchor.z
        ca = Vector(dx, dy, dz)
        v = ca.dot(ray.direct)
        if v-self.radius > ray.t:
            return False
        t = self.rsqr + v*v - dx*dx - dy*dy - dz*dz
        if t < 0:
            return False
        t = v - t**.5
        if t > ray.t or t < 0:
            return False
        ray.t = t
        ray.object = self
        return True
    
    def shade(self, ray, lights, objects, bgcolor):
        px = ray.anchor.x + ray.t*ray.direct.x
        py = ray.anchor.y + ray.t*ray.direct.y
        pz = ray.anchor.z + ray.t*ray.direct.z

        p = Vector(px, py, pz)
        v = Vector(-ray.direct.x, -ray.direct.y, -ray.direct.z)
        n = Vector(px-self.center.x, py-self.center.y, pz-self.center.z)
        n.normalize()

        return self.surface.shade(p, v, n, lights, objects, bgcolor)
