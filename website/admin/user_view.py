from flask_admin.contrib.sqla import ModelView
from .admin_views import BaseAdminView

class UserView(BaseAdminView):
    column_display_pk = True
