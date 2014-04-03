import pylab as pl
import flukaCubit as fc 
import os

class reader :
    def __init__(self, fileName) : 
        # need to relabel this body Dict 
        self.geoDict  = {'RPP':['name','xmin','xmax','ymin','ymax','zmin','zmax'],
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
        # fluka cmd dict 
        self.cmdDict = {'*':[]} 

        self.bodyDict = {}
        self.regiDict = {}
        self.rotnDict = {}

#        self.readFlukaGeometry(fileName)
        f = open(fileName) 
        self.readFile = f.read()
        self.readFlukaGeometryToken()
        self.readFlukaRegion()
        self.readFlukaRotnToken()

        f.close()

    def readTranformations(self,fileName) :
        f = open(fileName) 
        
        for l in f : 
            self.lineTransCheck(l) 

        f.close()

    def readFlukaGeometry(self,fileName) : 
        f = open(fileName) 
        
        # loop over lines in files 
        for l in f : 
            self.lineTypeCheck(l) 

        f.close()

    def readFlukaGeometryToken(self) :        
        rfs = self.readFile.split()

        translat = [0., 0., 0.] 
        transform = '' 

        for i in range(0,len(rfs),1) : 
            # ########################
            # Get the transform associated with the geometric object 
            # ########################
            if rfs[i] == '$start_translat' : 
                translat = [float(rfs[i+1]), float(rfs[i+2]), float(rfs[i+3])]
            if rfs[i] == '$start_transform' : 
                transform = rfs[i+1]
            if rfs[i] == '$end_translat' :
                translat = [0., 0., 0.] 
            if rfs[i] == '$end_transform' : 
                transform = ''
            try : 
                geoDictInd = self.geoDict.keys().index(rfs[i])
                geoType    = self.geoDict.keys()[geoDictInd]
#                print geoType, len(self.geoDict[geoType])
                data = []
            
                name = rfs[i+1]
                data.append(geoType)
                for j in range(i+2,i+len(self.geoDict[geoType])+1,1) : 
                    data.append(float(rfs[j]))
                self.bodyDict[name] = [data,translat,transform]
            except ValueError :
                continue

    def readFlukaRotnToken(self) : 
        rfs = self.readFile.split() 

        for i in range(0,len(rfs),1) : 
            if rfs[i] == 'ROT-DEFI' :
                rdata = []
                for j in range(0,6,1) : 
                    rdata.append(float(rfs[i+j+1]))
                self.rotnDict[rfs[i+7]] = rdata
            
    def readFlukaRegion(self) :
        '''Does a seach for a leading 'END' token to 'GEOEND' to find regions''' 

        rfs = self.readFile.split('\n')

        geoBegin = False
        iRegion  = -1
        regionDef = '' 
        regionName = '' 

        for l in rfs : 
            t = l.split() 
            if len(t) ==  0 : 
                continue 
            if l[0] == '*' : 
                continue
            if l[0] == '#' : 
                continue 
            if l[0] == '$' : 
                continue
            if t[0] == 'LATTICE' : 
                continue
            if t[0] == 'END' :
                geoBegin = True
                continue
            if t[0] == 'GEOEND' : 
                geoBegin = False



            if geoBegin : 
                try : 
                    self.geoDict.keys().index(t[0])
                    continue 
                except ValueError :
                    if l[0:3] != '   ' : 
                        iRegion = iRegion+1 

                        # remove the init case 
                        if regionName != '' : 
                            self.regiDict[regionName] = regionDef

                        regionName = t[0] 
                        regionDef  = l 
#                        print regionName+':'+l
                    else : 
#                        print regionName+':'+l
                        regionDef = regionDef+l

    def makeCubitFile(self, region) : 
        geo = self.regiDict[region] 
        t = geo.split() 

        f = open('region.jou','w') 

        transList   = []
        bodyOpList  = [] 
        bodyList    = []

        v1 = fc.createJou('main.jou')
        for i in range(3,len(t),1) : 
            op     = t[i][0]
            name   = t[i][1:]
            if name=='':
               continue 
            data   = self.bodyDict[name] 
            vdata  = data[0][1:]
            type   = data[0][0]
            trans  = data[1]

            bodyOpList.append(op)
            bodyList.append(name)
            transList.append(trans)

            print name,type,vdata,trans

            stlFile = name+'.stl'
            satFile = name+'.sat'

            #v1 = fc.createJou(jouFile)
            pr = fc.Primitives() 

            if type == 'RPP' :             
                v1.MakeModel(pr.RPP(vdata))
                v1.MakeModel(pr.translation(trans))
            elif type == 'RCC' : 
                v1.MakeModel(pr.RCC(vdata))    
                v1.MakeModel(pr.translation(trans))            
            elif type == 'XYP' : 
                v1.MakeModel(pr.XYP(vdata))
                v1.MakeModel(pr.translation(trans))
            elif type == 'ZCC' : 
                v1.MakeModel(pr.ZCC(vdata))
                v1.MakeModel(pr.translation(trans))                
                
            print data[1]
        
            #v1.exportSTL(stlFile)
            v1.exportSAT(satFile)


            # make 
            #f.write('import stl "/Users/robertainsworth/bdsim/utils/pyFluka/pyFluka/'+stlFile+'" merge\n')
            f.write('import acis "/Users/robertainsworth/bdsim/utils/pyFluka/pyFluka/'+satFile+'" attributes_on separate_bodies\n')
        v1.close()
        f.close()
        os.system('/Applications/Cubit-13.1/Cubit.app/Contents/MacOS/cubitcl -input main.jou -nographics -nojournal -batch > /dev/null')

        transList = pl.array(transList)

    def makeFinal(self):
        i=1
        fin = fc.createJou('final.jou')
        for reg in self.regiDict.keys():
            #fin.f.write('import acis "/Users/robertainsworth/bdsim/utils/pyFluka/pyFluka/'+reg+'.sat" attributes_on separate_bodies\n')
            fin.f.write('import acis "/Users/robertainsworth/bdsim/utils/pyFluka/pyFluka/'+reg+'.sat" attributes_on\n')
            fin.f.write('body '+str(i)+' name "'+reg+'"\n')
            i+=1
        fin.close()

    def makeGeometry(self):
        for reg in self.regiDict.keys():
           print 'building region: '+reg
           SRL,SROL=self.makeCubitBodies(reg)
           self.makeCubitRegions(reg,SRL,SROL)
        
    def makeCubitBodies(self, region) : 
        geo = self.regiDict[region] 
        t = geo.split() 

        transList   = []
        bodyOpList  = [] 
        bodyList    = []
        subRegionList=[]
        subRegionOpList=[]

        v1 = fc.createJou('main.jou')
        for i in range(3,len(t),1) : 
            op     = t[i][0]
            name   = t[i][1:]
            if name=='':
                subRegionList.append(bodyList)    
                subRegionOpList.append(bodyOpList)
                bodyOpList=[]
                bodyList=[]
                continue 
            data   = self.bodyDict[name] 
            vdata  = data[0][1:]
            type   = data[0][0]
            trans  = data[1]

            bodyOpList.append(op)
            bodyList.append(name)
            transList.append(trans)

            #print name,type,vdata,trans
            #print data, bodyOpList 
            stlFile = name+'.stl'
            satFile = name+'.sat'

            pr = fc.Primitives() 

            if type == 'RPP' :             
                v1.MakeModel(pr.RPP(vdata))
                v1.MakeModel(pr.translation(trans))
            elif type == 'RCC' : 
                v1.MakeModel(pr.RCC(vdata))    
                v1.MakeModel(pr.translation(trans))            
            elif type == 'XYP' : 
                v1.MakeModel(pr.XYP(vdata))
                v1.MakeModel(pr.translation(trans))
            elif type == 'ZCC' : 
                v1.MakeModel(pr.ZCC(vdata))
                v1.MakeModel(pr.translation(trans))                
            elif type == 'PLA' : 
                v1.MakeModel(pr.PLA(vdata))
                v1.MakeModel(pr.translation(trans))                
   
        
            #v1.exportSTL(stlFile)
            v1.exportSAT(satFile)

        v1.close()
        subRegionList.append(bodyList)    
        subRegionOpList.append(bodyOpList)    
        os.system('/Applications/Cubit-13.1/Cubit.app/Contents/MacOS/cubitcl -input main.jou -nographics -nojournal -batch > /dev/null')
        transList = pl.array(transList)
        return subRegionList,subRegionOpList

    def makeCubitRegions(self,region,subRegionList,subRegionOpList):
        regJ = fc.createJou('region.jou')
        for i in xrange(len(subRegionList)):
            for j in xrange(len(subRegionList[i])):
                satFile=subRegionList[i][j]+'.sat'
                regJ.f.write('import acis "/Users/robertainsworth/bdsim/utils/pyFluka/pyFluka/'+satFile+'" attributes_on separate_bodies\n')
                regJ.f.write('volume '+str(j+1)+' name "'+subRegionList[i][j]+'"\n')
            for j in xrange(1,len(subRegionList[i])):
                if subRegionOpList[i][j]=='+':
                    regJ.f.write('intersect '+subRegionList[i][j]+' '+subRegionList[i][0]+'\n')
                elif subRegionOpList[i][j]=='-':
                    regJ.f.write('subtract '+subRegionList[i][j]+' from '+subRegionList[i][0]+'\n')
            regJ.exportSAT('subRegion'+str(i+1)+'.sat')
        for i in xrange(len(subRegionList)):
            regJ.f.write('import acis "/Users/robertainsworth/bdsim/utils/pyFluka/pyFluka/subRegion'+str(i+1)+'.sat" attributes_on separate_bodies\n')
        regJ.f.write('unite all\n')
        regJ.exportSAT(region+'.sat')
        regJ.close()
        os.system('/Applications/Cubit-13.1/Cubit.app/Contents/MacOS/cubitcl -input region.jou -nographics -nojournal -batch > /dev/null')
