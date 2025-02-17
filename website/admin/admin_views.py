from flask_admin import AdminIndexView, expose
from flask_login import current_user
from flask import redirect, url_for
from ..models import Tovar, Order, Point, User
from sqlalchemy.exc import SQLAlchemyError
from flask_admin.contrib.sqla import ModelView

class MyMainView(AdminIndexView):
    @expose('/')
    def admin_stats(self):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))  # Перенаправляем на логин, если не авторизован

        if not self.is_accessible():
            return redirect(url_for('views.catalog'))  # Если нет доступа – на страницу каталога

        try:
            user_data = User.query.count()
            tovar_data = Tovar.query.count()
            point_data = Point.query.count()
            order_data = Order.query.count()
        except SQLAlchemyError:
            user_data = tovar_data = point_data = order_data = 0  # Если ошибка БД, данные по нулям

        return self.render('admin/stats.html', 
                           user_data=user_data,
                           order_data=order_data,
                           point_data=point_data,
                           tovar_data=tovar_data
                           )

    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, 'is_admin', False)  # Проверка на администратора

    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        return redirect(url_for('views.catalog'))


class BaseAdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, 'is_admin', False)  

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))  