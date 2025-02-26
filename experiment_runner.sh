#!/bin/bash

# Default number of iterations
NUM_RUNS=${1:-50}
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

# Run recordings WITH CPU load
echo "Recording WITH CPU load..."
for i in $(seq 1 $NUM_RUNS); do
    echo "Run $i/$NUM_RUNS"

    # Start CPU stressor in the background
    python3 cpu_simple.py &  
    CPU_PID=$!

    # Record while CPU stress is active
    python3 record_audio.py $DURATION "recordings/with_cpu/recording_$i.wav"

    # Stop CPU stressor
    kill $CPU_PID
    sleep 2  # Short pause before next run
done

echo "Experiment complete. Recordings saved in 'recordings/' directory."
