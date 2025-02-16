from flask_admin.contrib.sqla import ModelView

class TovarView(ModelView):
    column_display_pk = True