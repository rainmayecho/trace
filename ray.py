from vector import *

class Ray():
    '''
    -------------------------------------------
    Creates a ray with:
        p - The anchor point of the ray.
        v - the direction vector of the ray.

    trace iterates through the list of 'objects'
    and tests if the ray and the object intersect.

    shade calls the ray's object's shade method.
    -------------------------------------------    
    '''

    def __init__(self, p, v):
        self.anchor = p
        self.direct = v
        self.direct.normalize()
        self.t = 10.0**10
        self.object = None

    def trace(self, objects):
        for e in objects:
            if e.intersect(self):
                return True
            
    def shade(self, lights, objects, bgcolor):
        return self.object.shade(self, lights, objects, bgcolor)
