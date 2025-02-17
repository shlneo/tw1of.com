from flask_admin.contrib.fileadmin import FileAdmin
from flask_login import current_user
from flask import redirect, url_for
import os

class VideoView(FileAdmin):
    def __init__(self, *args, **kwargs):
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
        video_folder = os.path.join(base_path, 'video')

        if not os.path.exists(video_folder):
            os.makedirs(video_folder)
        
        super(VideoView, self).__init__(video_folder, '/static/video/', name='Video')

    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, 'is_admin', False)  

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))
