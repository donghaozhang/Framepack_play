#!/bin/bash

# Create a temporary file listing all videos to concatenate
echo "file 'coffe.mp4'" > videos_list.txt
echo "file 'Doraemon.mp4'" >> videos_list.txt
echo "file 'doge.mp4'" >> videos_list.txt
echo "file 'Lich King.mp4'" >> videos_list.txt
echo "file 'teddybear.mp4'" >> videos_list.txt
echo "file 'hearthstonev2.mp4'" >> videos_list.txt

# Use ffmpeg to concatenate all videos
ffmpeg -f concat -safe 0 -i videos_list.txt -c copy combined_gallery.mp4

# Clean up the temporary file
rm videos_list.txt

echo "All videos have been combined into combined_gallery.mp4" 