from vector import *

class Light():
    '''
    -------------------------------------------
    Holds information for a given light source.

    Types:
        - Ambient: Additive 'natural' lighting
        - Directional: Infinite distance, parallel light rays.
        - Point: Isotropic, defined location source.
    -------------------------------------------    
    '''

    AMBIENT = 0
    DIRECTIONAL = 1
    POINT = 2

    def __init__(self, l, r, g, b, vector = None):
        self.ltype = l
        self.red = r
        self.green = g
        self.blue = b
        if not self.ltype == self.AMBIENT:
            self.v = vector
            if self.ltype == self.DIRECTIONAL:
                self.v.normalize()
