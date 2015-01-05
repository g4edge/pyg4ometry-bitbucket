import Input as _in

class Reader : 
    def __init__(self, fileName) : 
        self.fileName = fileName
        self.bodyDict  = {'RPP':['name','xmin','xmax','ymin','ymax','zmin','zmax'],
                          'BOX':['name','vx','vy','vz','hx1','hy1','hz1','hx2','hy2','hz2','hx3','hy3','hz3'],
                          'SPH':['name','vx','vy','vz','r'],
                          'RCC':['name','vx','vy','vz','hx','hy','hz','r'],
                          'REC':['name','vx','vy','vz','hx','hy','hz','rx1','ry1','rz1','rx2','ry2','rz2'],
                          'TRC':['name','vx','vy','vz','hx','hy','hz','r1','r2'],
                          'ELL':['name','fx1','fy1','fz1','fx2','fy2','fz2','l'],
                          'WED':['name','vx','vy','vz','hx1','hy1','hz1','hx2','hy2','hz2','hx3','hy3','hz3'],
                          'RAW':['name','vx','vy','vz','hx1','hy1','hz1','hx2','hy2','hz2','hx3','hy3','hz3'],
                          'ARB':['name',
                                 'vx1','vy1','vz1','vx2','vy2','vz2','vx3','vy3','vz3',
                                 'vx4','vy4','vz4','vx5','vy5','vz5','vx6','vy6','vz6',
                                 'vx7','vy7','vz7','vx8','vy8','vz8'],
                          'YZP':['name','x'],
                          'XZP':['name','y'],
                          'XYP':['name','z'],
                          'PLA':['name','hx','hy','hz','vx','vy','vz'],
                          'XCC':['name','ay','az','r'],
                          'YCC':['name','ax','az','r'],
                          'ZCC':['name','ax','ay','r'],
                          'XEC':['name','ay','az','ly','lz'],
                          'YEC':['name','ax','az','lx','lz'],
                          'ZEC':['name','ax','ay','lx','ly'],
                          'QUA':['name','axx','ayy','azz','axy','axz','ayz','ax','ay','az','a0']}
        self.flukaDict = {'*':['comment'],
                          'END':[],
                          'ROT-DEFI':[],
                          'ASSIGNMA':['material','body'],
                          'MATERIAL':[],
                          'COMPOUND':[],
                          'LOW-MAT':[],
                          'TITLE':[],
                          'Elements':[],
                          'GLOBAL':[],
                          'DEFAULTS':[],
                          'BEAM':[],
                          'BEAMPOS':[],
                          'GEOBEGIN':[],
                          'RANDOMIZ':[],
                          'START':[],
                          'STOP':[],
                          '$start_translat':['x','y','z'],
                          '$end_translat':[],
                          '$start_transform':['name'],
                          '$end_tranform':[]}

        # keyword list 
        self.bodyKw  = self.bodyDict.keys()
        self.flukaKw = self.flukaDict.keys()


        self.bodies    = {}
        self.csg       = {}
        self.placement = {}
        self.materials = {}

    def readFile(self, fileName): 
        f = open(fileName) 
        
        self.readFile = [] 
        for l in f : 
            self.readFile.append(l)

    def comprehend(self) : 
        # look at each line and find bodies, csg lines, placement and material 
        for l in self.readFile : 
            sl = l.split();
            print sl[0]
        

    
