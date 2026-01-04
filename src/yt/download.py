import yt_dlp

def download_video(url, quality):

    options = {'quiet' : True}
    downloader = yt_dlp.YoutubeDL(options)

    # try:
    #     download_video = downloader.download()