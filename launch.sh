#!/bin/bash
echo "-------------------------------------"
echo "| Welcome to Ocean Data Downloader! |"
echo "-------------------------------------"

#datasets_dir="/home/pop/ocean_portal/datasets"

datasets_dir="/mnt/data/ocean_portal/datasets"

docker run -v $(pwd)/code:/scripts \
-v ${datasets_dir}:/home/pop/ocean_portal/datasets \
-ti --rm ocean-data -c 'python /scripts/main.py'