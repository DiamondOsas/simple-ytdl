import yt_dlp

def get_video_details(url) -> list[str] | None:

    options = {'quiet' : True}
    downloader = yt_dlp.YoutubeDL(options)

    try:
        video_info = downloader.extract_info(url ,download = False)

        title = video_info.get("title")
        thumbnail = video_info.get("thumbnail")
        creator = video_info.get("creator") or video_info.get("uploader")
        duration = video_info.get("duration")
        
        return [title, thumbnail, creator, duration]

    except Exception as e:
        print(f"Error: {e}")
        return None
