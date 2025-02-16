from flask_admin.contrib.sqla import ModelView

class UserView(ModelView):
    column_display_pk = True
