import yt_dlp

def get_video_details(url) -> list[str]:

    options = {'quiet' : True}
    downloader = yt_dlp.YoutubeDL(options)

    try:
        video_info = downloader.extract_info(url ,download = False)


        
        details = [title, thumbnail, creator, duration]
        return details

    except Exception as e:
        print(f"Error: {e}")
        return []

    