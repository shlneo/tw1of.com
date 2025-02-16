from flask_admin.contrib.sqla import ModelView


class OrderView(ModelView):
    column_display_pk = True
    
 