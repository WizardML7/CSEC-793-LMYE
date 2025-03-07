#!/bin/bash

# Default number of iterations
NUM_RUNS=${1:-300}
DURATION=10  # Each recording duration in seconds

# Create directories for organization
mkdir -p recordings/with_cpu
mkdir -p recordings/without_cpu

echo "Starting experiment with $NUM_RUNS runs each..."

# Run recordings WITHOUT CPU load
echo "Recording WITHOUT CPU load..."
for i in $(seq 1 $NUM_RUNS); do
    echo "Run $i/$NUM_RUNS"
    python3 record_audio.py $DURATION "recordings/without_cpu/recording_$i.wav"
    sleep 2  # Short pause to prevent overlapping
done

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

# Run recordings WITH CPU load
echo "Recording WITH CPU load..."
for i in $(seq 1 $NUM_RUNS); do
    echo "Run $i/$NUM_RUNS"


    # Record while CPU stress is active
    python3 record_audio.py $DURATION "recordings/with_cpu/recording_$i.wav"

    sleep 2  # Short pause before next run
done

kill $CPU_PID1
kill $CPU_PID2
kill $CPU_PID3
kill $CPU_PID4
kill $CPU_PID5

echo "Experiment complete. Recordings saved in 'recordings/' directory."
