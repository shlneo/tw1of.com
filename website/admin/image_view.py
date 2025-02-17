from flask_admin.contrib.fileadmin import FileAdmin
import os
from flask_login import current_user
from flask import redirect, url_for

class ImageView(FileAdmin):
    def __init__(self, *args, **kwargs):
        base_path = os.path.abspath(os.path.join(os.path.dirname(__name__), 'website', 'static'))
        image_folder = os.path.join(base_path, 'img')

        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
        
        super(ImageView, self).__init__(image_folder, '/static/img/', name='Images')

    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, 'is_admin', False)  

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))
