"""
Script to read in the output of `fmdt-detect` (see https://github.com/alsoc/fmdt for details)
and split a video into small chunks where meteors have been detected

"""

import fmdt
fmdt.split_video_at_meteors("demo_visu.mp4", "ex1_detect_tracks.txt", 6, 0, True, True)