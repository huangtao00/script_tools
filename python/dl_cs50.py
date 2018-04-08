url="https://cdn.cs50.net/2016/fall/lectures/{}/week{}-720p.mp4?download"
import os
if False:
    for i in range(3,12):
        new_url= url.format(i,i)
        savename="week"+str(i)+"_720p.mp4"
        wgetstr="wget "+ new_url+" -O "+savename
        # print (wgetstr)
        os.system(wgetstr)


#download subtitles
url="https://cdn.cs50.net/2016/fall/lectures/{}/lang/en/week{}.srt"

#http://cdn.cs50.net/2016/fall/lectures/1/lang/en/week1.srt

for i in range(0,12):
    new_url= url.format(i,i)
    savename="week"+str(i)+".srt"
    wgetstr="wget "+ new_url+" -O "+savename
    # print (wgetstr)
    os.system(wgetstr)