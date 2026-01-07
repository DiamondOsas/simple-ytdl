import yt_dlp
print(yt_dlp.YoutubeDL.__doc__)
def download_video(url, quality):

    options = {'quiet' : True}
    downloader = yt_dlp.YoutubeDL(options)
    
    # try:
    #     download_video = downloader.download()