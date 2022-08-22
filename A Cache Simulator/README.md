# Simulation-of-Inclusive-Exclusive-and-NINE-Cache
ReadTrace.c 

Language used: c
Header files required: stdio.h, assert.h, strlib.h, string.h
Input: trace file given by sir should be inside a folder 'traces' in the same path.
Output: trace file's hit/miss and their addresses in human readable format. Output is dumped in the same path as ReadTrace.c.

Command to run in terminal:
gcc ReadTrace.c -o ReadTrace
./ReadTrace ./traces/bzip2.log_l1misstrace 2
./ReadTrace ./traces/gcc.log_l1misstrace 2
./ReadTrace ./traces/gromacs.log_l1misstrace 1
./ReadTrace ./traces/h264ref.log_l1misstrace 1
./ReadTrace ./traces/hmmer.log_l1misstrace 1
./ReadTrace ./traces/sphinx3.log_l1misstrace 2

Time taken: A few seconds



Q1-inclusive.py, Q1-nine.py, Q1-exclusive.py, Q2-belady.py, Q3-lru.py:

Language used: Python 3.7.9
Python Libraries required: math, os (both are in-built libraries)
Input: All files obtained as output by running ReadTrace.c (should be in the same path as these python scripts).
Output: Hit/Miss count of L2 L3 Cache hierarchy as required to be reported.

Time taken:
Q1-inclusive.py: ~10 mins
Q1-nine.py: ~10 mins
Q1-exclusive.py: ~12 mins
Q2-belady.py: ~26 mins
Q3-lru.py: ~8 mins

Command to run in terminal:
python3 Q1-inclusive.py
python3 Q1-nine.py
python3 Q1-exclusive.py
python3 Q2-belady.py
python3 Q2-lru.py



RunFiles.sh:
RunFiles.sh can be used to run all the codes for the assignment all at once. 
Input: trace file given by sir should be inside a folder 'traces' in the same path, ReadTrace.c and python files should be in the same path.

Output of ReadTrace.c is dumped in the same path as ReadTrace.c. It can be run the way sir has said in the assignment.
They are input for the python files which simulate the cache hierarcy of question one and two. These files must remain in the same path as the python files.

Time taken: 60-70 minutes

Command to run in terminal:
bash RunFiles.sh

Output of RunFiles.sh has been attached as a seperate file named RunFilesTerminalOutput.txt
