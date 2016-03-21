import numpy as np
from StringIO import StringIO
import matplotlib.pyplot as plt
import os

class SPara:
    def __init__(self,spfile):
        self.spfile = spfile
        self.dim = self.GetDimension()
        self.unit_line_cnt = self._get_unit_line(self.dim)
        self.info = self.GetInfo()
        self.unit = self.info[0].upper()
        self.format = self.info[2].upper()
        #self.data = self.GetData()


        

    def GetDimension(self):
        """Get dimension of SNP file, eg S4P return 4
        """
        return int(os.path.splitext(self.spfile)[-1][2:-1])

    def GetInfo(self):
        fin = open(self.spfile)
        for line in fin:
            if line[0] == "#":
                info = line.split()[1:]
                fin.close()
                return info
    
    


    def _get_unit_line(self,n):
        """Get the line count for each s paramters
        """
        # each line 4 items max
        linecnt  = n/4
        # other items will use another line, and need to be added
        if n%4 >0:
            linecnt = linecnt +1
        # the total line count for 1 frequency
        return linecnt*n

    def GetRawData(self):
        """Return data in a array 
        """
        tmpline = ""

        if self.dim < 3:
            fin = open(self.spfile)
            #tmpline = ""
            for line in fin:
                if line[0] != "#" and  line[0] != "!":
                    tmpline = tmpline + line
            fin.close()
            #return np.genfromtxt(StringIO(tmpline)).T
        else:
            fin = open(self.spfile)
            #print "dim is %s" %self.dim
            data_buf = []
            for line in fin:
                if line[0] != "#" and  line[0] != "!" and line.strip():
                    data_buf.append(line.strip("\n"))
        
            fin.close()
            ####################

            out_buf = []
            xlen = len(data_buf)/self.unit_line_cnt
            #tmpline = ""
            for i in range(xlen):
                for j in range(self.unit_line_cnt):
                    tmpline = tmpline + data_buf[i*self.unit_line_cnt+j] 
                tmpline = tmpline +"\n"

  
        return np.genfromtxt(StringIO(tmpline)).T

    def GetSeData(self, format="DB", frequnit="GHz"):
        """Convert all data to the format in DB and freq in GHz
        """
        data = self.GetRawData()

        #2 port sequence is different <frequency value>  <N11>, <N21>, <N12>, <N22>
        #so we need a pre-swap
        if self.dim == 2:
            data = data[[0,1,2,5,6,3,4,7,8]]
        
        # Convert Freq
        if self.unit == "HZ":
            data[0] /= 1.0e9
        elif self.unit == "KHZ":
            data[0] /= 1.0e6
        elif self.unit == "MHZ":
            data[0] /= 1.0e3

        #Convert Data to dB
        if format == "DB":
            if self.format == "DB": #nothing to do if it is Mag-Angle already
                pass
            elif self.format == "MA": #use 20*log10 to get dB
                for i in range(1,(self.dim**2)*2,2):
                    data[i] = 20*np.log10(data[i])
            elif self.format == "RI": #convert to image
                for i in range(1,(self.dim**2)*2,2):
                    a = data[i] + 1j*data[i+1]
                    data[i] = 20*np.log10(a)
                    data[i+1] = np.angle(a,deg=True)
            return data

        #Convert Data to MA
        elif format == "MA":
            if self.format == "DB": #nothing to do if it is Mag-Angle already
                for i in range(1,(self.dim**2)*2,2):
                    data[i] = np.power(10,data[i]/20.0)     
            elif self.format == "MA": #use 20*log10 to get dB
                pass
            elif self.format == "RI": #convert to image
                for i in range(1,(self.dim**2)*2,2):
                    a = data[i] + 1j*data[i+1]
                    data[i] = np.absolute(a)
                    data[i+1] = np.angle(a,deg=True)
            return data    

        #Convert Data to RI, RI need half of the size 
        elif format == "RI": 
            outdata = np.zeros(((data.shape[0]-1)/2+1,data.shape[1]),dtype="complex")
            outdata[0] = data[0]

            if self.format == "DB": #nothing to do if it is Mag-Angle already
                for i in range(1,self.dim**2+1):
                    theta = np.radians(data[2*i])
                    r = np.power(10,data[2*i-1]/20.0)
                    outdata[i] = r*np.cos(theta) + 1j * r*np.sin(theta)
                    
            elif self.format == "MA": #use 20*log10 to get dB
                for i in range(1,self.dim**2+1):
                    theta = np.radians(data[2*i])
                    r = data[2*i-1] 
                    outdata[i] = r*np.cos(theta) + 1j * r*np.sin(theta)
                    
            elif self.format == "RI": #convert to image
                for i in range(1,self.dim**2):
                    outdata[i] = data[2*i-1] + 1j*data[2*i]
            return outdata    

        else: # raise a exception if the format cannot be recognized
            raise Exception("unknow format %s" %self.format)


    def GetdBSe(self):
        data = self.GetSeData("DB")
        idx = [0]
        idx.extend(range(1,data.shape[0],2))
        return data[idx]

    def GetAngSe(self):
        dat = self.GetSeData("DB")
        idx = [0]
        idx.extend(range(2,dat.shape[0],2))
        return self.GetSeData("DB")[idx]

    # mix mod data calcaulate
    def GetMixData4P(self,portmap=[1,2,3,4]):
        def S(i,j):
            row = (p[i-1]-1)*self.dim +p[j-1]
            return data[row]
        p = portmap
        data = self.GetSeData("RI")

        #in CC,CD,DC,DD order
        co = 0.5*np.array([[1,1,1,1],
                          [1,1,-1,-1],
                          [1,-1,1,-1],
                          [1,-1,-1,1]])


        SPMatrix = np.array([[S(1,1),S(2,1),S(1,2),S(2,2)],
                            [S(1,3),S(2,3),S(1,4),S(2,4)],
                            [S(3,1),S(4,1),S(3,2),S(4,2)], 
                            [S(3,3),S(4,3),S(3,4),S(4,4)]])

        mix_dim = self.dim/2
        xshape = mix_dim**2*4 + 1 #CC,CD,DC,DD
        yshape = data.shape[1]
        outdata = np.zeros((xshape,yshape),dtype="complex")
        outdata[0] = data[0]


        for i in range(4): 
            for j in range(1,5):
                SP = SPMatrix[j-1]
                #outdata[i*mix_dim**2+j] = 20*np.log(co[i][0]*SP[0] + co[i][1]*SP[1] + co[i][2]*SP[2] + co[i][3]*SP[3])
                outdata[i*mix_dim**2+j] = co[i][0]*SP[0] + co[i][1]*SP[1] + co[i][2]*SP[2] + co[i][3]*SP[3]

        return outdata

    def GetMixdB4P(self,portmap=[1,2,3,4]):
        data = self.GetMixData4P(portmap)
        data[1:] = 20*np.log10(data[1:])
        return data

    def GetMixAng4P(self,portmap=[1,2,3,4]):
        data = self.GetMixData4P(portmap)
        data[1:] = np.angle(data[1:],deg=True)
        return data


    ############TDR
    def TDR(self):
        data = self.GetSeData("RI")
        freq = np.absolute(data[0])*1e9
        S11 = data[1]
        fvec_sim,fdelta = np.linspace(0,5e9,2048,endpoint=False,retstep=True)
        #print S11.shape
        #print fvec_sim
        number_rows = S11.shape[0]
        #print number_rows
        #print step

        tsim = 1/5e9 
        #print 1/fdelta,tsim,1/fdelta-tsim
        time = np.arange(0,1/fdelta,tsim)
        #print time.shape

        S11 = np.interp(fvec_sim,S11,freq)
        print S11.shape
        print  freq.shape
        print fvec_sim.shape

if __name__ == "__main__":
    s = SPara(r"D:\study_docs\open course\ECE EE720\lab\peters_01_0605_B12_thru.s4p")
    print s.GetInfo()
    print s.format
    data = s.GetMixData4P(portmap=[1,3,2,4]) 


    S21 = data[15]
    #print S21
    plt.plot(np.abs(S21))
    plt.show()
