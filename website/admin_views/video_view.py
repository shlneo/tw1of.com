from flask_admin.contrib.fileadmin import FileAdmin
import os
from urllib.parse import quote, unquote

class VideoView(FileAdmin):
    def __init__(self, *args, **kwargs):
        base_path = os.path.abspath(os.path.join(os.path.dirname(__name__), 'website', 'static'))
        video_folder = os.path.join(base_path, 'video')

        if not os.path.exists(video_folder):
            os.makedirs(video_folder)
        
        super(VideoView, self).__init__(video_folder, '/static/video/', name='Video')
