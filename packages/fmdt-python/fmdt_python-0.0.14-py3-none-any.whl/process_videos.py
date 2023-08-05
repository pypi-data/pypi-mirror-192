import fmdt

in_video = "Draco_0.avi"
# in_video = "demo.mp4"
tracks   = "Draco_0_tracks.txt"
bbs      = "Draco_0_bbs.txt"

# fmdt.detect(in_video, trk_bb_path=bbs, out_track_file=tracks)
# fmdt.detect(in_video, trk_bb_path=bbs, out_track_file=tracks)
# fmdt.detect(in_video, trk_bb_path=bbs, out_track_file=tracks)
# fmdt.detect(in_video, trk_bb_path=bbs, out_track_file=tracks)
# fmdt.detect(in_video, trk_bb_path=bbs, out_track_file=tracks)

k = 3 
out = []
for i in range(k):

    fmdt.detect(in_video, trk_bb_path=bbs, out_track_file=tracks)
    c = fmdt.count(trk_bb_path=tracks, meteors=True)
    out.append(c)

print(out)