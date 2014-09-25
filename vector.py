
class Vector():

    '''
    -------------------------------------------
    Creates a 3D Vector

    add returns the vector addition of the 'self' vector
    and the 'other' vector.

    dot returns the vector dot product of the
    'self' vector and the 'other' vector.

    cross returns the vector cross product of the
    'self' vector and the 'other' vector.

    cross is also overloaded to accept two
    arbitrary vector parameters (not self).

    scale multiplies all entries by the
    scalar quantity 's'.

    normalize scales the 'self' vector by
    1/self.mag
    
    -------------------------------------------    
    '''
    def __init__(self, i, j, k):
        self.x = float(i)
        self.y = float(j)
        self.z = float(k)
        self.mag = (self.dot(self))**.5

    def add(self,other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def dot(self,other):
        return self.x*other.x + self.y*other.y + self.z*other.z

    def cross(self,other):
        return Vector((self.y*other.z - other.y*self.z),\
                      -(self.x*other.z - other.x*self.z),\
                      (self.x*other.y - other.x*self.y))
    def cross(a,b):
        return Vector((a.y*b.z - b.y*a.z),\
                      -(a.x*b.z - b.x*a.z),\
                      (a.x*b.y - b.x*a.y))

    def scale(self,s):
        self.x *= s
        self.y *= s
        self.z *= s
        
    def normalize(self):
        self.scale(1.0/self.mag)
        
    def __str__(self):
        return '%f i %f j %f k' %(self.x, self.y, self.z)
