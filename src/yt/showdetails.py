from pytubefix import AsyncYouTube

async def get_video_details(url) -> list[str] | None:
    try:
        yt = AsyncYouTube(url)
        
        # In AsyncYouTube, fetching attributes usually requires awaiting
        title = await yt.title
        thumbnail = await yt.thumbnail_url
        creator = await yt.author
        duration = await yt.length  # duration in seconds

        # Convert duration from seconds to a more readable format (e.g., mm:ss)
        minutes, seconds = divmod(duration, 60)
        duration_str = f"{minutes}:{seconds:02d}"

        return [title, thumbnail, creator, duration_str]

    except Exception as e:
        print(f"Error fetching details: {e}")
        return None
