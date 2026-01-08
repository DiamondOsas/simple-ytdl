from pytubefix import YouTube


def get_video_details(url : str) -> list | None:
    try:
        yt = YouTube(url)
        title = yt.title
        thumbnail = yt.thumbnail_url
        author = yt.author
        duration = yt.length
        
        # Get all available video qualities (including adaptive streams like 1080p)
        streams = yt.streams.filter(only_video=True)
        qualities = sorted(list(set([s.resolution for s in streams if s.resolution])))
        

        minutes, seconds = divmod(duration, 60)

        durationstr = str(minutes)+":"+str(seconds)
        return [title, thumbnail, author, durationstr, qualities]
    
    except Exception as e:
        print(f"Error: ", e)
        return None
