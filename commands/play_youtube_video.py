import pywhatkit
from base_command import BaseCommand

class CommandPlayYoutubeVideo(BaseCommand):
    def __init__(self):
        self.name = "play_youtube_video"
        self.metadata = {
                "name": f"{self.name}",
                "description": "Play a YouTube video",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "video_name": {
                            "type": "string",
                            "description": "The name of the video to play on YouTube",
                        },
                    },
                    "required": ["video_name"],
                },
            }
        
        super().__init__(f"{self.name}", self.metadata)

    def execute(self, video_name):
        """Opens a new tab in the default browser and plays a YouTube video."""
        pywhatkit.playonyt(video_name)
        return f"You have successfully started playing {video_name} on Youtube"