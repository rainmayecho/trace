
class Point():
    '''
    -------------------------------------------
    Holds information for points.
    -------------------------------------------    
    '''

    def __init__(self,i,j,k):
        self.x = float(i)
        self.y = float(j)
        self.z = float(k)

    def __str__(self):
        return '%f i %f j %f k' %(self.x, self.y, self.z)

