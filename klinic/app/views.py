# -*- coding: utf-8 -*-

from flask import render_template
# from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import (
    SimpleFormView
)
from flask_babel import lazy_gettext as _

from . import appbuilder, db
from .forms import UploadForm

"""
    Create your Model based REST API::

    class MyModelApi(ModelRestApi):
        datamodel = SQLAInterface(MyModel)

    appbuilder.add_api(MyModelApi)


    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(
        MyModelView,
        "My View",
        icon="fa-folder-open-o",
        category="My Category",
        category_icon='fa-envelope'
    )
"""


class UploadView(SimpleFormView):
    form = UploadForm
    form_title = '上传CSV文件'
    message = '上传成功'

    def form_get(self, form):
        form.field1.data = "This was prefilled"

    def form_post(self, form):
        # post process form
        # flash(self.message, "info")
        pass


appbuilder.add_view(
    UploadView,
    '数据导入',
    icon='fa-group',
    label=_('File Import'),
    category='设备管理',
    category_icon='fa-cogs',
)


"""
    Application wide 404 error handler
"""


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    return (
        render_template(
            "404.html",
            base_template=appbuilder.base_template,
            appbuilder=appbuilder
        ),
        404,
    )


db.create_all()
