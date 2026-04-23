#!/bin/bash

# Clear the file before starting (optional)
> timings.txt

for i in {0..3}; do
    (
        echo "Running iteration $i..."

        # Time and run the Python command
        { time -p python3 tasks.py --mcprod --version 1000_large_batch/run$i; } 2> temp_time_$i.txt

        # Extract real time and write to a temp output
        real_time=$(grep ^real temp_time_$i.txt | awk '{print $2}')
        echo "$i: $real_time seconds" >> timing_$i.txt

        # Clean up the timing output for this run
        rm temp_time_$i.txt
    ) &
done

# Wait for all background jobs to finish
wait

# Combine all individual timing logs into one
cat timing_*.txt >> timings.txt
rm timing_*.txt

#Calculate and append the average real time
avg=$(awk -F': ' '{sum += $2} END {if (NR > 0) printf "%.3f", sum/NR}' timings.txt)
echo "Average: $avg seconds" >> timings.txt