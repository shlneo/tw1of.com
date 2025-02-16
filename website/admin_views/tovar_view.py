from flask_admin.contrib.sqla import ModelView
from wtforms import FloatField, IntegerField, StringField
from wtforms.validators import DataRequired, Optional

class TovarView(ModelView):
    column_display_pk = True  
    column_list = ('id', 'type', 'name', 'count', 'cost', 'status', 'color', 'size', 'thickness', 'material', 'base', 'info', 'img_name')
    form_columns = ('type', 'name', 'count', 'cost', 'status', 'color', 'size', 'thickness', 'material', 'base', 'info', 'img_name')

    form_overrides = {
        'cost': FloatField,
        'count': IntegerField,
        'name': StringField,
        'type': StringField,
        'status': StringField,
        'color': StringField,
        'size': StringField,
        'thickness': StringField,
        'material': StringField,
        'base': StringField,
        'info': StringField,
        'img_name': StringField,
    }

    form_args = {
        'type': {'validators': [DataRequired()]},
        'name': {'validators': [DataRequired()]},
        'count': {'validators': [Optional()], 'widget': IntegerField.widget},
        'cost': {'validators': [Optional()], 'widget': FloatField.widget},
        'status': {'validators': [Optional()]},
        'color': {'validators': [Optional()]},
        'size': {'validators': [Optional()]},
        'thickness': {'validators': [Optional()]},
        'material': {'validators': [Optional()]},
        'base': {'validators': [Optional()]},
        'info': {'validators': [Optional()]},
        'img_name': {'validators': [Optional()]},
    }

    column_filters = ('type', 'status', 'color', 'size', 'material', 'base')
    column_searchable_list = ('name', 'info', 'img_name')
