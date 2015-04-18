from flask_admin.contrib.peewee import ModelView
from flask.ext.admin import Admin
from flask_admin.contrib.peewee.form import CustomModelConverter
from flask_admin.form.widgets import DateTimePickerWidget
from playhouse.postgres_ext import ArrayField, DateTimeTZField
from wtforms import fields

from redash import models
from redash.permissions import require_permission


class PgModelConverter(CustomModelConverter):
    def __init__(self, view, additional=None):
        additional = {ArrayField: self.handle_array_field,
                      DateTimeTZField: self.handle_datetime_tz_field}
        super(CustomModelConverter, self).__init__(additional)
        self.view = view

    def handle_array_field(self, model, field, **kwargs):
        return field.name, fields.StringField(**kwargs)

    def handle_datetime_tz_field(self, model, field, **kwargs):
        kwargs['widget'] = DateTimePickerWidget()
        return field.name, fields.DateTimeField(**kwargs)


class PgModelView(ModelView):
    model_form_converter = PgModelConverter

    @require_permission('admin')
    def is_accessible(self):
        return True


def init_admin(app):
    admin = Admin(app, name='redash')

    for m in models.all_models:
        admin.add_view(PgModelView(m))