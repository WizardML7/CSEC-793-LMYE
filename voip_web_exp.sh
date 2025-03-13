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

# Run the experiment
for i in $(seq 1 $NUM_RUNS); do
    for site in "${websites[@]}"; do
        echo "Run $i/$NUM_RUNS - Visiting $site"
        python3 simple_websites.py "$site"
        sleep 5  # Short pause between visits
    done
done

echo "Website browsing experiment complete."
