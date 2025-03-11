

python3 cpu_simple.py &  
    CPU_PID1=$!

python3 cpu_simple.py &  
    CPU_PID2=$!

python3 cpu_simple.py &  
    CPU_PID3=$!

python3 cpu_simple.py &  
    CPU_PID4=$!

python3 cpu_simple.py &  
    CPU_PID5=$!


sleep 60


kill $CPU_PID1
kill $CPU_PID2
kill $CPU_PID3
kill $CPU_PID4
kill $CPU_PID5