from pytubefix import YouTube
import ffmpeg
import os

def download_video(url: str, quality: str) -> str | None:
    try:
        yt = YouTube(url)
        # Create a simple safe filename (no weird characters)
        safe_title = "".join([c for c in yt.title if c.isalnum() or c == " "]).strip()
        
        print(f"Starting process for: {safe_title} ({quality})")

        # 1. Select the Streams
        # We search specifically for adaptive streams (separate V/A)
        video_stream = yt.streams.filter(res=quality, only_video=True).first()
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

        if not video_stream:
            print(f"Error: No video stream found for {quality}")
            return None

        # 2. Setup Filenames
        video_tmp = f"v_tmp_{safe_title}.mp4"
        audio_tmp = f"a_tmp_{safe_title}.mp4"
        final_file = f"{safe_title}_{quality}.mp4"

        # 3. Download both parts
        print("Downloading video track...")
        video_stream.download(filename=video_tmp)
        
        if audio_stream:
            print("Downloading audio track...")
            audio_stream.download(filename=audio_tmp)
            
            # Check sizes
            v_size = os.path.getsize(video_tmp) / (1024 * 1024)
            a_size = os.path.getsize(audio_tmp) / (1024 * 1024)
            print(f"Downloaded: Video={v_size:.2f}MB, Audio={a_size:.2f}MB")

            # 4. Merge using FFmpeg
            print("Merging streams together...")
            if combine_audio_video(video_tmp, audio_tmp, final_file):
                print("Download and Merge Successful!")
                # Cleanup temporary files
                try:
                    os.remove(video_tmp)
                    os.remove(audio_tmp)
                except Exception as e:
                    print(f"Warning: Could not delete temp files: {e}")
                return "Success"
            else:
                print("Error: Merging failed.")
                return None
        else:
            # If no audio is found for some reason, just keep the video
            print("Warning: No audio found. Saving video only.")
            os.rename(video_tmp, final_file)
            return "Success (No Audio)"

    except Exception as e:
        print(f"Download Error: {e}")
        return None


def combine_audio_video(video_path: str, audio_path: str, output_path: str) -> bool:
    """Uses ffmpeg to combine a video and audio file into one."""
    try:
        # Define the input streams
        input_video = ffmpeg.input(video_path)
        input_audio = ffmpeg.input(audio_path)

        # Simple merge command: map both inputs to output
        # explicit mapping isn't strictly necessary if we just pass inputs, 
        # but passing them as arguments to output works well.
        # We use c='copy' to avoid re-encoding if possible (fastest), 
        # but if audio is improper format for mp4, this might fail.
        # Let's try 'copy' for video and 'aac' for audio to be safe.
        
        print("Running FFmpeg...")
        ffmpeg.output(
            input_video,
            input_audio,
            output_path,
            vcodec='copy',
            acodec='aac',
            strict='experimental'
        ).run(overwrite_output=True) # Removed quiet=True to see errors in console

        return True

    except ffmpeg.Error as e:
        print(f"FFmpeg Error: {e}")
        # If possible, print stderr to see what actually happened
        if hasattr(e, 'stderr') and e.stderr:
             print(f"FFmpeg Log: {e.stderr.decode('utf8')}")
        return False
