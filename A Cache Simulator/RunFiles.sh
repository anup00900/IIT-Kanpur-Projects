gcc ReadTrace.c -o ReadTrace
./ReadTrace ./traces/bzip2.log_l1misstrace 2
./ReadTrace ./traces/gcc.log_l1misstrace 2
./ReadTrace ./traces/gromacs.log_l1misstrace 1
./ReadTrace ./traces/h264ref.log_l1misstrace 1
./ReadTrace ./traces/hmmer.log_l1misstrace 1
./ReadTrace ./traces/sphinx3.log_l1misstrace 2

python3 Q1-inclusive.py
python3 Q1-nine.py
python3 Q1-exclusive.py
python3 Q2-belady.py
python3 Q2-lru.py
