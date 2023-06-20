import pywhatkit

def play_youtube_video(self, video_name):
        """Opens a new tab in the default browser and plays a YouTube video."""
        pywhatkit.playonyt(video_name)
        return f"You have successfully started playing {video_name} on Youtube"