from flask_admin.contrib.sqla import ModelView

class PointView(ModelView):
    column_display_pk = True
