#!/bin/bash

# Default number of iterations
NUM_RUNS=${1:-100}
DURATION=10  # Each recording duration in seconds

# Create directories for organization

echo "Starting experiment with $NUM_RUNS."

echo "CPU load alternating."
for i in $(seq 1 $NUM_RUNS); do
    echo "Run $i/$NUM_RUNS"
    python3 cpu_alternate.py &  
        CPU_PID1=$!
    sleep 2  # Short pause to prevent overlapping
    kill $CPU_PID1
done

echo "Experiment complete. Recordings saved in 'recordings/' directory."
