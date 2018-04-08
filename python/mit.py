import os


vtt=[file  for file in os.listdir(".") if "srt" in file]
videos=[file  for file in os.listdir(".") if "mp4" in file]
# vtt.sort()
# for a,b in zip(vtt,video):
# 	print a,b
# 	# print " "
# 	newvtt=b[:b.rindex(".")]+".vtt"

for video  in videos:
	name=video[video.index("-")+1:video.rindex("-")]
	# print name
	for sub in vtt:
		if name in sub:
			# print video,sub
			newvtt=video[:video.rindex(".")]+".vtt"
			os.rename(sub,newvtt)

	#os.rename(a,newvtt)
	# if a.index('.')==1:
	# 	os.rename(a,"0"+a)