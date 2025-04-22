@echo off
ECHO Creating combined video file from all gallery videos...

REM Create a PowerShell script to combine videos
ECHO $outputVideo = "combined_gallery.mp4" > combine_videos.ps1
ECHO $inputVideos = @("coffe.mp4", "Doraemon.mp4", "doge.mp4", "Lich King.mp4", "teddybear.mp4", "hearthstonev2.mp4") >> combine_videos.ps1
ECHO >> combine_videos.ps1

ECHO # Check if output file already exists and delete it >> combine_videos.ps1
ECHO if (Test-Path $outputVideo) { >> combine_videos.ps1
ECHO     Remove-Item $outputVideo >> combine_videos.ps1
ECHO } >> combine_videos.ps1
ECHO >> combine_videos.ps1

ECHO # Use Copy-Item with binary mode to combine the videos >> combine_videos.ps1
ECHO $writer = [System.IO.File]::OpenWrite($outputVideo) >> combine_videos.ps1
ECHO foreach ($video in $inputVideos) { >> combine_videos.ps1
ECHO     if (Test-Path $video) { >> combine_videos.ps1
ECHO         Write-Host "Adding $video to combined video..." >> combine_videos.ps1
ECHO         $content = [System.IO.File]::ReadAllBytes($video) >> combine_videos.ps1
ECHO         $writer.Write($content, 0, $content.Length) >> combine_videos.ps1
ECHO     } else { >> combine_videos.ps1
ECHO         Write-Host "Warning: $video not found, skipping" >> combine_videos.ps1
ECHO     } >> combine_videos.ps1
ECHO } >> combine_videos.ps1
ECHO $writer.Close() >> combine_videos.ps1
ECHO >> combine_videos.ps1

ECHO Write-Host "Video creation complete! File saved as $outputVideo" >> combine_videos.ps1

ECHO Running PowerShell script to combine videos...
PowerShell -ExecutionPolicy Bypass -File combine_videos.ps1

DEL combine_videos.ps1

ECHO Combined video has been saved as combined_gallery.mp4
ECHO NOTE: This is a simple binary concatenation which may or may not work properly
ECHO       depending on your video formats. For the best results, consider installing
ECHO       ffmpeg which is designed for proper video processing.
PAUSE 