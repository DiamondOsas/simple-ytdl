from pytubefix import YouTube

from pytubefix import YouTube

def download_video(url: str, quality: str) -> str | None:
    try:
        yt = YouTube(url)

        # Filter streams by resolution and get the first matching video stream
        # we filter for video only, and then the specific resolution
        stream = yt.streams.filter(res=quality, only_video=True).first()
        
        if stream:
            print(f"Downloading {quality}...")
            stream.download()
            print("Download complete!")
            return "Success"
        else:
            print(f"No stream found for quality: {quality}")
            return None

    except Exception as e:
        print(f"Error {e}")
        return None