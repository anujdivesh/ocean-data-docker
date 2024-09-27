#!/bin/bash
echo "-------------------------------------"
echo "| Welcome to Ocean Data Downloader! |"
echo "-------------------------------------"

#datasets_dir="/home/pop/ocean_portal/datasets"
cd /home/ubuntu/ocean-data-docker

datasets_dir="/mnt/data/ocean_portal/datasets"

docker run -v $(pwd)/code:/scripts \
-v ${datasets_dir}:/home/pop/ocean_portal/datasets -it --rm ocean-data-download -c 'python /scripts/main.py'
