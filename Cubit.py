import pylab as pl 


class createJou:
    def __init__(self,fileName):
        self.f=open(fileName,'w')
        self.f.write('reset\n')

    def MakeModel(self,mod):
        self.f.write(mod)

    def exportSTL(self,exportName,reset=True):
        self.f.write('export stl ascii "'+exportName+'"\n')
        if reset==True:
            self.f.write('reset\n')
    
    def exportSAT(self,exportName,reset=True):
        self.f.write('export acis "'+exportName+'" overwrite\n')
        if reset==True:
            self.f.write('reset\n')


    def close(self):
        self.f.close()

class Primitives(object):

    def __init__(self):
        self.Inf=1e6

    def translation(self,array):
        x=array[0]
        y=array[1]
        z=array[2]
        s=''
        s+='move volume 1 x '+str(x)+' y '+str(y)+' z '+str(z)+' include_merged\n'
        return s

    def RPP(self,array):
        s=''
        xmin=array[0]
        xmax=array[1]
        ymin=array[2]
        ymax=array[3]
        zmin=array[4]
        zmax=array[5]
        s+='brick x '+str(xmax-xmin)+' y '+str(ymax-ymin)+' z '+str(zmax-zmin)+ '\n' 
        s+='move volume 1 x '+str((xmax-xmin)/2.0 + xmin)+' y '+str((ymax-ymin)/2.0 + ymin)+' z '+str((zmax-zmin)/2.0 + zmin)+' include_merged\n'
        return s

    def BOX(self,array):
        s=''
        vx=array[0]
        vy=array[1]
        vz=array[2]
        Hx1=array[3]
        Hy1=array[4]
        Hz1=array[5]
        Hx2=array[6]
        Hy2=array[7]
        Hz2=array[8]
        Hx3=array[9]
        Hy3=array[10]
        Hz3=array[11]
        xLength = pl.sqrt(Hx1**2 + Hy1**2 + Hz1**2)
        yLength = pl.sqrt(Hx2**2 + Hy2**2 + Hz2**2)
        zLength = pl.sqrt(Hx3**2 + Hy3**2 + Hz3**2)
        s+='create curve location '+str(vx) + ' ' +str(vy)+ ' '+str(vz)+'  direction '+str(Hx1) + ' ' +str(Hy1)+ ' '+str(Hz1)+' length '+str(xLength)+' \n'
        s+='create curve location '+str(vx) + ' ' +str(vy)+ ' '+str(vz)+'  direction '+str(Hx2) + ' ' +str(Hy2)+ ' '+str(Hz2)+' length '+str(yLength)+' \n'
        s+='create curve location '+str(vx) + ' ' +str(vy)+ ' '+str(vz)+'  direction '+str(Hx3) + ' ' +str(Hy3)+ ' '+str(Hz3)+' length '+str(zLength)+' \n'
        s+='sweep curve 1 along curve 2 \n'
        s+='sweep surface 1 along curve 3 \n'
        s+='delete curve all\n'
        s+='delete vertex all\n'
        return s

    def SPH(self,array):
        s=''
        Vx=array[0]
        Vy=array[1]
        Vz=array[2]
        R=array[3]
        s+='create sphere radius '+str(R)+'\n' 
        s+='move Volume 1 location '+str(Vx)+' '+str(Vy)+' '+str(Vz)+' include_merged\n'
        return s

    def RCC(self,array):
        s=''
        vx=array[0]
        vy=array[1]
        vz=array[2]
        Hx=array[3]
        Hy=array[4]
        Hz=array[5]
        R=array[6]
        Length = pl.sqrt(Hx**2 + Hy**2 + Hz**2)
        s+='create curve location '+str(vx)+' '+str(vy)+' '+str(vz)+' direction '+str(Hx)+' '+str(Hy)+' '+str(Hz)+' length '+ str(Length)+' \n'
        s+='create curve arc center vertex 1 radius '+str(R)+' normal '+str(Hx)+' '+str(Hy)+' '+str(Hz)+' full \n'
        s+='create surface curve 2 \n'
        s+='sweep surface 1 along curve 1 \n'
        s+='delete curve all\n'
        s+='delete vertex all\n'
        return s

    def ZCC(self,array):
        s=''
        Ax = array[0]
        Ay = array[1]
        R = array[2]
        s+='create surface circle radius '+str(R)+' zplane\n'
        s+='move surface 1 x '+str(Ax)+' y '+str(Ay)+' include_merged\n'
        s+='sweep surface 1 perpendicular distance '+str(self.Inf)+'\n'
        s+='sweep surface 3 perpendicular distance '+str(self.Inf)+'\n'
        return s

    def XCC(self,array):
        s=''
        Ay = array[0]
        Az = array[1]
        R = array[2]
        s+='create surface circle radius '+str(R)+' xplane\n'
        s+='move surface 1 y '+str(Ay)+' z '+str(Az)+' include_merged\n'
        s+='sweep surface 1 perpendicular distance '+str(self.Inf)+'\n'
        s+='sweep surface 3 perpendicular distance '+str(self.Inf)+'\n'
        return s

    def YCC(self,array):
        s=''
        Az = array[0]
        Ax = array[1]
        R = array[2]
        s+='create surface circle radius '+str(R)+' yplane\n'
        s+='move surface 1 x '+str(Ax)+' z '+str(Az)+' include_merged\n'
        s+='sweep surface 1 perpendicular distance '+str(self.Inf)+'\n'
        s+='sweep surface 3 perpendicular distance '+str(self.Inf)+'\n'
        return s

    def YZP(self,array):
        s=''
        Vx = array[0]
        s+='brick x '+str(2*self.Inf)+' y '+str(2*self.Inf)+' z '+str(2*self.Inf)+'\n'
        s+='move Volume 1 x '+str(-self.Inf+Vx)+ 'include_merged\n' 
        return s

    def XZP(self,array):
        s=''
        Vy = array[0]
        s+='brick x '+str(2*self.Inf)+' y '+str(2*self.Inf)+' z '+str(2*self.Inf)+'\n'
        s+='move Volume 1 y '+str(-self.Inf+Vy)+ 'include_merged\n' 
        return s

    def XYP(self,array):
        s=''
        Vz = array[0]
        s+='brick x '+str(2*self.Inf)+' y '+str(2*self.Inf)+' z '+str(2*self.Inf)+'\n'
        s+='move Volume 1 z '+str(-self.Inf+Vz)+ 'include_merged\n' 
        return s

    def PLA(self, array):
        s=''
        Hx = array[0]
        Hy = array[1]
        Hz = array[2]
        Vx = array[3]
        Vy = array[4]
        Vz = array[5]
        s+='create curve location '+str(Vx)+' '+str(Vy)+' '+str(Vz)+' direction '+str(-Hx)+' '+str(-Hy)+' '+str(-Hz)+' length '+str(self.Inf)+'\n' 
        s+='create curve arc center vertex 1 radius '+str(self.Inf)+' normal '+str(Hx)+' '+str(Hy)+' '+str(Hz)+'full\n'
        s+='create surface curve 2\n'
        s+='sweep surface 1 along curve 1\n'
        s+='delete curve all\n'
        s+='delete vertex all\n'
        return s

    def TRC(self,array):
        s=''
        Vx = array[0]
        Vy = array[1]
        Vz = array[2]
        Hx = array[3]
        Hy = array[4]
        Hz = array[5]
        R1 = array[6]
        R2 = array[7]
        Length=pl.sqrt(Hx**2 + Hy**2 + Hz**2)
        s+='create curve location '+str(Vx)+' '+str(Vy)+' '+str(Vz)+' direction '+str(Hx)+' '+str(Hy)+' '+str(Hx)+' length '+str(Length)+'\n'
        s+='create curve arc center vertex 1 radius '+str(R1)+' normal '+str(Hx)+' '+str(Hy)+' '+str(Hz)+'\n'
        s+='create curve arc center vertex 2 radius '+str(R2)+' normal '+str(Hx)+' '+str(Hy)+' '+str(Hz)+'\n'
        s+='create surface curve 2\n' 
        s+='create surface curve 3\n'
        s+='create volume loft surface 1 2\n'
        s+='delete body 1 2\n'
        s+='delete curve 1\n'
        s+='compress ids\n'
        s+='delete curve all\n'
        s+='delete vertex all\n'
        return s

    def WED(self,array):
        s=''
        vx=array[0]
        vy=array[1]
        vz=array[2]
        Hx1=array[3]
        Hy1=array[4]
        Hz1=array[5]
        Hx2=array[6]
        Hy2=array[7]
        Hz2=array[8]
        Hx3=array[9]
        Hy3=array[10]
        Hz3=array[11]
        xLength = pl.sqrt(Hx1**2 + Hy1**2 + Hz1**2)
        yLength = pl.sqrt(Hx2**2 + Hy2**2 + Hz2**2)
        zLength = pl.sqrt(Hx3**2 + Hy3**2 + Hz3**2)
        s+='create curve location '+str(vx) + ' ' +str(vy)+ ' '+str(vz)+'  direction '+str(Hx1) + ' ' +str(Hy1)+ ' '+str(Hz1)+' length '+str(xLength)+' \n'
        s+='create curve location '+str(vx) + ' ' +str(vy)+ ' '+str(vz)+'  direction '+str(Hx2) + ' ' +str(Hy2)+ ' '+str(Hz2)+' length '+str(yLength)+' \n'
        s+='create curve location '+str(vx) + ' ' +str(vy)+ ' '+str(vz)+'  direction '+str(Hx3) + ' ' +str(Hy3)+ ' '+str(Hz3)+' length '+str(zLength)+' \n'
        s+='create curve vertex 2 4\n'
        s+='create surface curve 2 1 4\n'
        s+='sweep surface 1 along curve 3\n'
        s+='delete curve all\n'
        s+='delete vertex all\n'

        return s

    def ZEC(self,array):
        s=''
        Ax = array[0]
        Ay = array[1]
        Lx = array[2]
        Ly = array[3]
        s+='create surface ellipse major radius '+str(Lx)+' minor radius '+str(Ly)+' zplane\n'
        s+='move surface 1 x '+str(Ax)+' y '+str(Ay)+' include_merged\n'
        s+='sweep surface 1 perpendicular distance '+str(self.Inf)+'\n'
        s+='sweep surface 3 perpendicular distance '+str(self.Inf)+'\n'
        s+='delete curve all\n'
        s+='delete vertex all\n'
        return s

    def XEC(self,array):
        s=''
        Ay = array[0]
        Az = array[1]
        Ly = array[2]
        Lz = array[3]
        s+='create surface ellipse major radius '+str(Lz)+' minor radius '+str(Ly)+' xplane\n'
        s+='move surface 1 y '+str(Ay)+' z '+str(Az)+' include_merged\n'
        s+='sweep surface 1 perpendicular distance '+str(self.Inf)+'\n'
        s+='sweep surface 3 perpendicular distance '+str(self.Inf)+'\n'
        s+='delete curve all\n'
        s+='delete vertex all\n'
        return s

    def YEC(self,array):
        s=''
        Az = array[0]
        Ax = array[1]
        Lz = array[2]
        Lx = array[3]
        s+='create surface ellipse major radius '+str(Lx)+' minor radius '+str(Lz)+' yplane\n'
        s+='move surface 1 x '+str(Ax)+' z '+str(Az)+' include_merged\n'
        s+='sweep surface 1 perpendicular distance '+str(self.Inf)+'\n'
        s+='sweep surface 3 perpendicular distance '+str(self.Inf)+'\n'
        s+='delete curve all\n'
        s+='delete vertex all\n'
        return s

    def ARB(self, array):
        s=''
        Vx1=array[0]
        Vy1=array[1]
        Vz1=array[2]
        Vx2=array[3]
        Vy2=array[4]
        Vz2=array[5]
        Vx3=array[6]
        Vy3=array[7]
        Vz3=array[8]
        Vx4=array[9]
        Vy4=array[10]
        Vz4=array[11]
        Vx5=array[12]
        Vy5=array[13]
        Vz5=array[14]
        Vx6=array[15]
        Vy6=array[16]
        Vz6=array[16]
        Vx7=array[18]
        Vy7=array[19]
        Vz7=array[20]
        Vx8=array[21]
        Vy8=array[22]
        Vz8=array[23]
        Face1=str(array[24])
        Face2=str(array[25])
        Face3=str(array[26])
        Face4=str(array[27])
        Face5=str(array[28])
        Face6=str(array[29])
        s+='create vertex '+str(Vx1)+' '+str(Vy1)+' '+str(Vz1)+'\n' 
        s+='create vertex '+str(Vx2)+' '+str(Vy2)+' '+str(Vz2)+'\n' 
        s+='create vertex '+str(Vx3)+' '+str(Vy3)+' '+str(Vz3)+'\n' 
        s+='create vertex '+str(Vx4)+' '+str(Vy4)+' '+str(Vz4)+'\n' 
        s+='create vertex '+str(Vx5)+' '+str(Vy5)+' '+str(Vz5)+'\n' 
        s+='create vertex '+str(Vx6)+' '+str(Vy6)+' '+str(Vz6)+'\n' 
        s+='create vertex '+str(Vx7)+' '+str(Vy7)+' '+str(Vz7)+'\n' 
        s+='create vertex '+str(Vx8)+' '+str(Vy8)+' '+str(Vz8)+'\n' 
        s+='create curve vertex '+str(Face1[0])+' '+str(Face1[1])+'\n'
        s+='create curve vertex '+str(Face1[1])+' '+str(Face1[2])+'\n'
        s+='create curve vertex '+str(Face1[2])+' '+str(Face1[3])+'\n'
        s+='create curve vertex '+str(Face1[3])+' '+str(Face1[0])+'\n'
        s+='create curve vertex '+str(Face2[0])+' '+str(Face2[1])+'\n'
        s+='create curve vertex '+str(Face2[1])+' '+str(Face2[2])+'\n'
        s+='create curve vertex '+str(Face2[2])+' '+str(Face2[3])+'\n'
        s+='create curve vertex '+str(Face2[3])+' '+str(Face2[0])+'\n'
        s+='create curve vertex '+str(Face3[0])+' '+str(Face3[1])+'\n'
        s+='create curve vertex '+str(Face3[1])+' '+str(Face3[2])+'\n'
        s+='create curve vertex '+str(Face3[2])+' '+str(Face3[3])+'\n'
        s+='create curve vertex '+str(Face3[3])+' '+str(Face3[0])+'\n'
        s+='create curve vertex '+str(Face4[0])+' '+str(Face4[1])+'\n'
        s+='create curve vertex '+str(Face4[1])+' '+str(Face4[2])+'\n'
        s+='create curve vertex '+str(Face4[2])+' '+str(Face4[3])+'\n'
        s+='create curve vertex '+str(Face4[3])+' '+str(Face4[0])+'\n'
        s+='create curve vertex '+str(Face5[0])+' '+str(Face5[1])+'\n'
        s+='create curve vertex '+str(Face5[1])+' '+str(Face5[2])+'\n'
        s+='create curve vertex '+str(Face5[2])+' '+str(Face5[3])+'\n'
        s+='create curve vertex '+str(Face5[3])+' '+str(Face5[0])+'\n'
        s+='create curve vertex '+str(Face6[0])+' '+str(Face6[1])+'\n'
        s+='create curve vertex '+str(Face6[1])+' '+str(Face6[2])+'\n'
        s+='create curve vertex '+str(Face6[2])+' '+str(Face6[3])+'\n'
        s+='create curve vertex '+str(Face6[3])+' '+str(Face6[0])+'\n'
        s+='create surface curve 1 2 3 4\n' 
        s+='create surface curve 5 6 7 8\n' 
        s+='create surface curve 9 10 11 12\n' 
        s+='create surface curve 13 14 15 16\n' 
        s+='create surface curve 17 18 19 20\n' 
        s+='create surface curve 21 22 23 24\n' 
        s+='create volume surface 1 to 6\n'
        s+='compress ids\n'
        return s

    def ELL(self, array):
        s=''
        Fx1 = array[0]
        Fy1 = array[1]
        Fz1 = array[2]
        Fx2 = array[3]
        Fy2 = array[4]
        Fz2 = array[5]
        L = array[6]
        f = pl.sqrt(Fx1**2 + Fy1**2 + Fz1**2)
        a=L/2.0
        b = pl.sqrt(a**2 - f**2)
        dx = Fx1-Fx2
        dy = Fy1-Fy2
        dz = Fz1-Fz2
        mx = (Fx1+Fx2)/2.0
        my = (Fy1+Fy2)/2.0
        mz = (Fz1+Fz2)/2.0
        s+='create curve location '+str(mx)+' '+str(my)+' '+str(mz)+' direction '+str(dx)+' '+str(dy)+' '+str(dz)+' length '+str(a)+'\n'
        s+='create curve location '+str(mx)+' '+str(my)+' '+str(mz)+' direction '+str(-dx)+' '+str(-dy)+' '+str(-dz)+' length '+str(a)+'\n'
        s+='create curve location '+str(mx)+' '+str(my)+' '+str(mz)+' direction '+str(dy)+' '+str(dx)+' '+str(dz)+' length '+str(b)+'\n'
        s+='create surface ellipse vertex 4 6 3\n'
        s+='webcut volume 1 with plane normal to curve 3 fraction 0\n'
        s+='delete body 2\n'
        s+='sweep surface 2 axis '+str(mx)+' '+str(my)+' '+str(mz)+' '+str(dx)+' '+str(dy)+' '+str(dz)+' angle 360\n'
        return s

    def REC(self,array):
        s=''
        vx=array[0]
        vy=array[1]
        vz=array[2]
        Hx=array[3]
        Hy=array[4]
        Hz=array[5]
        Rx1=array[6]
        Ry1=array[7]
        Rz1=array[8]
        Rx2=array[9]
        Ry2=array[10]
        Rz2=array[11]
        Length = pl.sqrt(Hx**2 + Hy**2 + Hz**2)
        L1 = pl.sqrt(Rx1**2 + Ry1**2 + Rz1**2)
        L2 = pl.sqrt(Rx2**2 + Ry2**2 + Rz2**2)
        s+='create curve location '+str(vx)+' '+str(vy)+' '+str(vz)+' direction '+str(Hx)+' '+str(Hy)+' '+str(Hz)+' length '+ str(Length)+' \n'
        s+='create curve arc center vertex 1 radius '+str(10)+' normal '+str(Hx)+' '+str(Hy)+' '+str(Hz)+' full \n'
        s+='create surface curve 2 \n'
        s+='create curve location '+str(vx)+' '+str(vy)+' '+str(vz)+' direction '+str(Rx1)+' '+str(Ry1)+' '+str(Rz1)+' length '+str(L1)+'\n'
        s+='create curve location '+str(vx)+' '+str(vy)+' '+str(vz)+' direction '+str(Rx2)+' '+str(Ry2)+' '+str(Rz2)+' length '+str(L2)+'\n'
        s+='create surface ellipse vertex 5 7 4\n'
        s+='align Volume 2  surface 2  with surface 1 \n'
        s+='delete body 1\n'
        s+='sweep surface 2 along curve 1\n'
        s+='delete curve all\n'
        s+='delete vertex all\n'
        return s

