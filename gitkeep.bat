#!/bin/bash

# Find all empty directories
empty_dirs=$(find . -type d -empty)

# Loop through each empty directory and add a .gitkeep file
for dir in $empty_dirs; do
  touch "$dir/.gitkeep"
  echo "Added .gitkeep to $dir"
done

# Stage the new .gitkeep files
git add .

echo "All empty folders now have .gitkeep files added and staged for commit."

