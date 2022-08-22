import math
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("\n\nRunning Q2-belady.py for Inclusive set associative L2 and fully associative L3 Cache Hierarchy Simulation")

FilesRequired = {
    'h264ref': ['L1Miss_h264ref.log_l1misstrace_0'],
    'gromacs': ['L1Miss_gromacs.log_l1misstrace_0'],
    'hmmer': ['L1Miss_hmmer.log_l1misstrace_0'],
    'bzip': ['L1Miss_bzip2.log_l1misstrace_0', 'L1Miss_bzip2.log_l1misstrace_1'],
    'sphinx': ['L1Miss_sphinx3.log_l1misstrace_0', 'L1Miss_sphinx3.log_l1misstrace_1'],
    'gcc': ['L1Miss_gcc.log_l1misstrace_0', 'L1Miss_gcc.log_l1misstrace_1'],
    
}

class L2Cache:
    def __init__(self, totalsize, associativity, blocksize):
        self.totalsize = totalsize
        self.associativity = associativity
        self.blocksize = blocksize
        self.totalblocks = totalsize//blocksize
        self.totalsets = self.totalblocks//associativity
        self.arr = [[[None, False] for i in range(associativity)] for j in range(self.totalsets)]
        self.lru = [[] for j in range(self.totalsets)]

    def GetSetNoTagNo(self, addr):
        binsetno = addr[int(-math.log2(self.totalsets)):]
        if len(binsetno)==0:
            setno = 0
        else:
            setno = int(binsetno, 2)

        bintagno = binaddr[:int(-math.log2(self.totalsets))]
        if len(bintagno)==0:
            tagno = 0
        else:
            tagno = int(bintagno, 2)
        return setno, tagno

    def CheckMiss(self, addr):
        setno, tagno = self.GetSetNoTagNo(addr)
        for blockno in range(self.associativity):
            if [tagno, True] == self.arr[setno][blockno]:
                self.ChangeLRU(blockno, setno) 
                return False #hit

        return True #miss

    def ChangeLRU(self, blockno, setno):
        for i in range(len(self.lru[setno])):
            if self.lru[setno][i] == blockno:
                self.lru[setno].pop(i)
                break
        self.lru[setno].append(blockno)


    def Evict(self, blkaddr):
        setno, tagno = self.GetSetNoTagNo(blkaddr)
        for blockno in range(self.associativity):
            if [tagno, True] == self.arr[setno][blockno]:
                self.arr[setno][blockno][1] = False
                
                for i in range(len(self.lru[setno])):
                    if self.lru[setno][i] == blockno:
                        self.lru[setno].pop(i)
                        break


    def Replacement(self, addr):
        setno, tagno = self.GetSetNoTagNo(addr)
        for blockno in range(self.associativity):
            if self.arr[setno][blockno][1] is False:
                self.arr[setno][blockno][0] = tagno
                self.arr[setno][blockno][1] = True
                self.ChangeLRU(blockno, setno)
                return None
        
        evict = self.lru[setno].pop(0) # evict has block number

        self.arr[setno][evict][0] = tagno
        self.arr[setno][evict][1] = True
        self.lru[setno].append(evict)

    
class L3Cache:
    def __init__(self, totalsize, associativity, blocksize):
        self.totalsize = totalsize
        self.associativity = associativity
        self.blocksize = blocksize
        self.totalblocks = totalsize//blocksize
        self.arr = set()
        self.cold = set()
        self.validlist = list()  #2d array [next index in trace of tag, tagno]
        self.NoFutureUse = set()

    def CheckMiss(self, tagno):
        if tagno in self.arr:  
            self.AddToValidList(tagno)    
            return False #hit

        if tagno not in self.cold:
            self.cold.add(tagno)
        return True #miss

    def bs(self, key):
        if len(self.validlist)==0:
            return 0

        low = 0
        high = len(self.validlist)-1

        while(low<high):
            mid = low +(high-low)//2
            if self.validlist[mid][0] < key:
                low = mid + 1
            else:
                high = mid
        return high

    def AddToValidList(self, tagno):
        if len(beladydict[tagno])>1:
            idx = self.bs(beladydict[tagno][1])  #find idx >= index
            
            if len(self.validlist) == idx:

                tmp = [beladydict[tagno][1], tagno]
                self.validlist.append(tmp)

            elif self.validlist[idx][0] == beladydict[tagno][1]:
                x = beladydict[tagno]
                self.validlist[idx][1] = tagno

            else:
                tmp = [beladydict[tagno][1], tagno]
                self.validlist.insert(idx, tmp)


    def Replacement(self, tagno):
        if len(self.arr) < self.associativity:
            self.arr.add(tagno)
            self.AddToValidList(tagno)
            return None

        if len(self.NoFutureUse)>=1:
            evict = self.NoFutureUse.pop()
        else:
            evict = self.validlist[-1][1]
            self.validlist.pop()

        if evict in self.arr:
            self.arr.remove(evict)
        
        self.arr.add(tagno)
        self.AddToValidList(tagno)
        return evict


    
        




for i in FilesRequired:
    addrlist = []
    beladydict = dict()
    L2 = L2Cache(524288, 8, 64)
    L3 = L3Cache(2097152, 32768, 64)
    print('\nExecuting the L1Miss Trace of : '+ i )
    fileNames=FilesRequired[i]
    L2misscount = 0
    L3misscount = 0
    L2hitcount = 0
    L3hitcount = 0
    index = 0
    for file_name in fileNames:
        with open(file_name) as fr:
            for line in fr.readlines():
                line = line.split()
                typ = line[0]

                if(int(typ)):
                    addr = int(line[1])
                    binaddr = bin(addr)[2:][:int(-math.log2(64))] #binary adress without block offset
                    
                    addrlist.append(binaddr)
                    if binaddr in beladydict:
                        beladydict[binaddr].append(index)
                    else:
                        beladydict[binaddr] = [index]
                    index+=1


    for index in range(len(addrlist)):
        binaddr = addrlist[index]
        l2miss = L2.CheckMiss(binaddr)
        if l2miss:
            L2misscount+=1
            l3miss = L3.CheckMiss(binaddr)
            
            if l3miss:
                L3misscount+=1
                evicted_blkAddr = L3.Replacement(binaddr)

                if evicted_blkAddr is not None:
                    L2.Evict(evicted_blkAddr)
            else:
                L3hitcount+=1

            L2.Replacement(binaddr)
        else:
            L3.AddToValidList(binaddr)
            L2hitcount+=1
        

        beladydict[binaddr].remove(index)
        if len(beladydict[binaddr])==0 and binaddr in L3.arr:
            L3.NoFutureUse.add(binaddr)
        
        for j in L3.validlist:
            if j[0]<=index:
                L3.validlist.remove(j)
            else:
                break

    print("L3cache Miss Count of ", i, " is : ", L3misscount)  
    print("L3cache Cold Miss Count of ", i, " is : ", len(L3.cold))
    print("L3cache Capacity Miss Count of ", i, " is : ", L3misscount-len(L3.cold))
