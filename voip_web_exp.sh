#!/bin/bash

# Default number of iterations
NUM_RUNS=${1:-100}

echo "Starting website browsing experiment with $NUM_RUNS iterations."

# List of websites
websites=(
    "https://www.reuters.com"
    "https://economictimes.indiatimes.com"
    "https://indianexpress.com"
    "https://www.news.com.au"
    "https://www.chinadaily.com.cn"
    "https://www.latimes.com"
    "https://www.nytimes.com"
    "https://www.forbes.com"
    "https://www.newsweek.com"
    "https://www.bloomberg.com/middleeast"
    "https://www.foxnews.com"
    "https://abcnews.go.com"
    "https://www.euronews.com"
    "https://www.nationalgeographic.com"
)

# Initial setup wait
echo "Waiting 15 seconds before starting to align with attacker..."
sleep 15

# Run the experiment
for ((i=1; i<=NUM_RUNS; i++)); do
    for site in "${websites[@]}"; do
        # Wait until the next full minute before starting
        current_second=$(date +%S)
        wait_time=$((60 - current_second))
        echo "Waiting $wait_time seconds for next minute sync..."
        sleep $wait_time

        echo "Run $i/$NUM_RUNS - Visiting $site"
        python3 simple_websites.py "$site"
        sleep 5  # Short pause between visits
    done
done

echo "Website browsing experiment complete."
