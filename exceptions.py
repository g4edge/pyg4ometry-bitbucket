
class NullMeshError(Exception):
    """
    Exception for possible null mesh formed in Boolean operation.

    NullMeshError(vol1,vol2,"union")
    """
    def __init__(self, vol1, vol2, combination):
        self.vol1 = vol1
        self.vol2 = vol2
        self.combination = combination

    def __repr__(self):
        s =  str(self.combination) + " null mesh with "
        s += str(self.vol1) + " " + str(self.vol2)
        return s
