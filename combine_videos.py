"""
Video Combiner Script (Dual-Mode)

This script combines multiple video files into a single video file.
It will use moviepy if available, or fall back to binary concatenation if not.

For best results, install moviepy: pip install moviepy
"""

import os
import sys
import shutil
import subprocess
import platform
import logging
from pathlib import Path
from moviepy.editor import VideoFileClip, concatenate_videoclips

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Try to import moviepy, but don't fail if it's not available
try:
    from moviepy.editor import VideoFileClip, concatenate_videoclips
    HAVE_MOVIEPY = True
    print("MoviePy found! Will use it for proper video concatenation.")
except ImportError:
    HAVE_MOVIEPY = False
    print("MoviePy not found. Will use binary concatenation (limited compatibility).")
    print("For better results, install MoviePy: pip install moviepy")

def combine_videos_moviepy(input_files, output_file):
    """Combine videos using MoviePy (high quality)"""
    print("Using MoviePy to combine videos (high quality method)...")
    
    try:
        # Load all video clips
        clips = [VideoFileClip(file) for file in input_files]
        
        # Concatenate clips
        final_clip = concatenate_videoclips(clips)
        
        # Write output file
        print(f"Writing to output file {output_file}...")
        final_clip.write_videofile(output_file)
        
        # Close all clips to free resources
        for clip in clips:
            clip.close()
        final_clip.close()
        
        return True
    except Exception as e:
        print(f"Error using MoviePy: {str(e)}")
        return False

def combine_videos_binary(input_files, output_file):
    """Combine videos using binary concatenation (limited compatibility)"""
    print("Using binary concatenation (limited compatibility)...")
    
    try:
        # Open output file for binary writing
        with open(output_file, 'wb') as outfile:
            # Process each input file
            for i, file in enumerate(input_files):
                print(f"Adding file {i+1}/{len(input_files)}: {file}")
                
                # Open input file and copy its contents to the output file
                with open(file, 'rb') as infile:
                    # Copy in chunks to handle large files efficiently
                    while True:
                        chunk = infile.read(1024*1024)  # 1MB chunks
                        if not chunk:
                            break
                        outfile.write(chunk)
                
                print(f"Added {file} ({os.path.getsize(file) / (1024*1024):.2f} MB)")
        
        print("\nWARNING: Binary concatenation was used, which does not properly combine MP4 files.")
        print("         The resulting file may only play the first video in the sequence.")
        print("         For proper combination, please install MoviePy: pip install moviepy")
        
        return True
    except Exception as e:
        print(f"Error in binary concatenation: {str(e)}")
        return False

def combine_videos():
    try:
        # 1) Set up paths
        video_dir = Path("videos")
        if not video_dir.exists():
            logger.error(f"Directory {video_dir} does not exist!")
            return

        # Get all video files
        sources = sorted(video_dir.glob("*.mp4"))
        if not sources:
            logger.error("No .mp4 files found in the videos directory!")
            return

        logger.info(f"Found {len(sources)} video files to combine")

        # 2) Load clips
        logger.info("Loading video clips...")
        clips = []
        for f in sources:
            try:
                clip = VideoFileClip(str(f))
                clips.append(clip)
                logger.info(f"Loaded {f.name}")
            except Exception as e:
                logger.error(f"Error loading {f.name}: {str(e)}")
                continue

        if not clips:
            logger.error("No clips were successfully loaded!")
            return

        # 3) Concatenate clips
        logger.info("Concatenating video clips...")
        final = concatenate_videoclips(clips, method="compose")

        # 4) Export
        out = "combined.mp4"
        logger.info(f"Exporting to {out}...")
        final.write_videofile(
            out,
            codec="libx264",
            audio_codec="aac",
            logger=None  # Disable moviepy's logger to avoid duplicate messages
        )

        # 5) Clean up
        logger.info("Cleaning up resources...")
        for c in clips:
            c.close()
        final.close()

        logger.info("Video combination completed successfully!")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

def verify_file_size(file_path):
    """
    Verify the file size using system commands
    """
    try:
        # Get the absolute path to ensure the command works correctly
        abs_path = os.path.abspath(file_path)
        
        # Check if we're on Windows or Unix-like system
        if platform.system() == "Windows":
            # Use dir command on Windows
            dir_command = f'dir "{abs_path}"'
            process = subprocess.Popen(dir_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            print("Windows file information:")
            print(stdout.decode('utf-8', errors='ignore'))
        else:
            # Use ls command on Unix-like systems
            ls_command = f'ls -lh "{abs_path}"'
            process = subprocess.Popen(ls_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            print("Unix file information:")
            print(stdout.decode('utf-8', errors='ignore'))
    except Exception as e:
        print(f"Error getting file information from system: {str(e)}")

if __name__ == "__main__":
    combine_videos()
    
    print("\nPress Enter to exit...")
    input() 