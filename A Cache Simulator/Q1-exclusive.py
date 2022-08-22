import math
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("\n\nRunning Q1-exclusive.py for Exclusive L2 L3 Cache Hierarchy Simulation")

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
        self.totalblocks = totalsize // blocksize
        self.totalsets = self.totalblocks // associativity
        self.arr = [[[None, False] for i in range(associativity)] for j in range(self.totalsets)]
        self.lru = [[] for j in range(self.totalsets)]

    def GetSetNoTagNo(self, addr):
        binaddr = addr[:int(-math.log(self.blocksize, 2))]
        setno = int(binaddr[int(-math.log(self.totalsets, 2)):], 2)
        bintagno = binaddr[:int(-math.log(self.totalsets, 2))]
        tagno = int(bintagno, 2)
        return setno, tagno

    def CheckMiss(self, addr):
        setno, tagno = self.GetSetNoTagNo(addr)
        for blockno in range(self.associativity):
            if (self.arr[setno][blockno][0] == tagno and self.arr[setno][blockno][1] == True):
                self.ChangeLRU(blockno, setno)
                return False  # hit

        return True  # miss

    def ChangeLRU(self, blockno, setno):
        if blockno in self.lru[setno]:
            self.lru[setno].remove(blockno)
        self.lru[setno].append(blockno)

    def CacheInvalidate(self, addr):
        setno, tagno = self.GetSetNoTagNo(addr)
        for blockno in range(self.associativity):
            if (self.arr[setno][blockno][0] == tagno and self.arr[setno][blockno][1] == True):
            		self.arr[setno][blockno][1] = False
            		if blockno in self.lru[setno]:
            			self.lru[setno].remove(blockno)
            			return


   

    def Replacement(self, addr):
        setno, tagno = self.GetSetNoTagNo(addr)
        for blockno in range(self.associativity):
            if self.arr[setno][blockno][1] == False:
                self.arr[setno][blockno][0] = tagno
                self.arr[setno][blockno][1] = True
                self.ChangeLRU(blockno, setno)
                return False,None

        evict = self.lru[setno].pop(0)
        evicttag = self.arr[setno][evict][0]
        binsetno = bin(setno)[2:].zfill(int(math.log2(self.totalsets)))
        blkaddr = int(bin(evicttag)[2:] + binsetno + '0'*int(math.log2(self.blocksize)),2)
        self.arr[setno][evict][0] = tagno
        self.arr[setno][evict][1] = True
        
        self.ChangeLRU(evict, setno)
        
        return True,blkaddr




for i in FilesRequired:
    print('\nExecuting the L1Miss Trace of : ' + i)
    fileNames = FilesRequired[i]
    L2misscount = 0
    L3misscount = 0
    L2hitcount = 0
    L3hitcount = 0
    L2 = Cache(524288, 8, 64)
    L3 = Cache(2097152, 16, 64)
    for file_name in fileNames:

        with open(file_name) as fr:
            for line in fr.readlines():
                line = line.split(' ')
                typ = line[0]
                if (int(typ)):
                    addr = int(line[1])
                    addr = bin(addr)[2:].zfill(64)
                    l2miss = L2.CheckMiss(addr)
                    if l2miss:
                        L2misscount += 1
                        l3miss = L3.CheckMiss(addr)
                        if l3miss:
                            L3misscount += 1
                            evict_flag,evict_addr=L2.Replacement(addr)
                            
                            if evict_flag:
                            	evict_addr=bin(evict_addr)[2:].zfill(64)
                            	evict_flag,evict_addr=L3.Replacement(evict_addr)
                            	
                        else:
                            L3hitcount += 1
                            L3.CacheInvalidate(addr)
                            evict_flag,evict_addr = L2.Replacement(addr)
                            if evict_flag:
                            	evict_addr=bin(evict_addr)[2:].zfill(64)
                            	evict_flag,evict_addr=L3.Replacement(evict_addr)
                    else:
                        L2hitcount += 1
    print("L2cache Miss Count of ", i, " is : ", L2misscount, " and L2cache Hit Count of ", i, " is : ", L2hitcount)
    print("L3cache Miss Count of ", i, " is : ", L3misscount, "L3cache Hit Count of ", i, " is : ", L3hitcount)     


