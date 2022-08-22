import math
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("\n\nRunning Q1-inclusive.py for Inclusive L2 L3 Cache Hierarchy Simulation")

FilesRequired = {
    'h264ref': ['L1Miss_h264ref.log_l1misstrace_0'],
    'gromacs': ['L1Miss_gromacs.log_l1misstrace_0'],
    'hmmer': ['L1Miss_hmmer.log_l1misstrace_0'],
    'bzip': ['L1Miss_bzip2.log_l1misstrace_0', 'L1Miss_bzip2.log_l1misstrace_1'],
    'sphinx': ['L1Miss_sphinx3.log_l1misstrace_0', 'L1Miss_sphinx3.log_l1misstrace_1'],
    'gcc': ['L1Miss_gcc.log_l1misstrace_0', 'L1Miss_gcc.log_l1misstrace_1'],
    
}

class Cache:
    def __init__(self, totalsize, associativity, blocksize):
        self.totalsize = totalsize
        self.associativity = associativity
        self.blocksize = blocksize
        self.totalblocks = totalsize//blocksize
        self.totalsets = self.totalblocks//associativity
        self.arr = [[[None, False] for i in range(associativity)] for j in range(self.totalsets)]
        self.lru = [[] for j in range(self.totalsets)]

    def GetSetNoTagNo(self, addr):
        binaddr = bin(addr)[2:][:int(-math.log2(self.blocksize))]
        binsetno = binaddr[int(-math.log2(self.totalsets)):]
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

        # (Get evicted block address)
        evicttag = self.arr[setno][evict][0]
        binsetno = bin(setno)[2:].zfill(int(math.log2(self.totalsets)))
        blkaddr = int(bin(evicttag)[2:] + binsetno + '0'*int(math.log2(self.blocksize)),2)

        self.arr[setno][evict][0] = tagno
        self.arr[setno][evict][1] = True
        self.lru[setno].append(evict)

        return blkaddr

    

    
        




for i in FilesRequired:
    L2 = Cache(524288, 8, 64)
    L3 = Cache(2097152, 16, 64)
    print('\nExecuting the L1Miss Trace of : '+ i )
    fileNames=FilesRequired[i]
    L2misscount = 0
    L3misscount = 0
    L2hitcount = 0
    L3hitcount = 0
    for file_name in fileNames:
        with open(file_name) as fr:
            for line in fr.readlines():
                line = line.split()
                typ = line[0]

                if(int(typ)):
                    addr = int(line[1])
                    
                    l2miss = L2.CheckMiss(addr)
                    if l2miss:
                        L2misscount+=1
                        l3miss = L3.CheckMiss(addr)
                        
                        if l3miss:
                            L3misscount+=1
                            evicted_blkAddr = L3.Replacement(addr)

                            if evicted_blkAddr is not None:
                                L2.Evict(evicted_blkAddr)

                        else:
                            L3hitcount+=1

                        L2.Replacement(addr)
                    else:
                        L2hitcount+=1

    print("L2cache Miss Count of ", i, " is : " ,L2misscount, " and L2cache Hit Count of ", i, " is : ", L2hitcount)
    print("L3cache Miss Count of ", i, " is : ", L3misscount, "L3cache Hit Count of ", i, " is : ", L3hitcount)  

